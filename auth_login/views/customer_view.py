
from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from utils.error_handle import error_handler
from utils.sms import SmsSender
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _




#########  for customer views

class RegisterView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
    def post(self,request,*args,**kwargs):
        serialized=PendingClientSerializer(data=request.data)
          # check if user exists
        if MyUser.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
            return Response({'error': _('Phone number or email already exists')}, status=status.HTTP_409_CONFLICT)
        
        if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
            return Response({'error': _('MANY OTP REQUESTS')}, status=status.HTTP_409_CONFLICT)
        otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.REGISTER)
        if serialized.is_valid():
            serialized.save(otp=otp) 
            sms = SmsSender()
            if sms.send_otp(request.data['phone'].replace('0', '966', 1), f"Your OTP for registration is: {otp}"):
                return Response({'result': 'Wait to recive OTP message'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': _('Failed to send OTP')}, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)


class PhoneVerifyView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
    def post(self,request,*args,**kwargs):
    
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.REGISTER).first()
            if otp:
                # deactivate otp code
                otp.isUsed=True
                otp.save()
                return Response({"result":"OTP is correct"})
            else:
                return Response({"error":_("OTP is not correct!")},status.HTTP_404_NOT_FOUND)
       
                
            

class CustomerDataAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.request.user.pk)


        

class CustomerCreateAccountAPIView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self, request):
            if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
                otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                            code=request.data['code'],                                            
                                            type=OTPRequest.Types.REGISTER).first()
                pendingClient=otp.pendingClient    
                if MyUser.objects.filter(Q(phone=pendingClient.phone)|Q(email=pendingClient.email)).exists():
                    return Response({'error': _('IDENTIFIER EXISTS')})
                new_customer=Customer.objects.create(name=pendingClient.fullName,phone=pendingClient.phone,
                                            email=pendingClient.email)
               
                new_customer.password=make_password(request.data['password'])
                new_customer.save()
                
                return Response({"result":"created"}, status=status.HTTP_201_CREATED)
            return Response({'error': _('The phone is not verified')}, status=status.HTTP_409_CONFLICT)
      




class CustomerAuthToken(ObtainAuthToken):
    serializer_class = MyAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        
        User = get_user_model()
        try:
            user = MyUser.objects.get(phone=phone)
            customer = Customer.objects.get(phone=user.phone)
            
        except User.DoesNotExist:
            return Response({'error': _('not a customer account')}, status=status.HTTP_404_NOT_FOUND)
        
        if check_password(password, user.password):
            if customer.phone == user.phone:
                user.fcm_token=request.data['fcm_token']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': {
                        'id': customer.id,
                        'phone': customer.phone,
                        'email': customer.email,
                        
                    }
                })
            
        return Response({'error': _('Invalid phone or password')}, status=status.HTTP_409_CONFLICT)
    
    
class ForgetPasswordAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(request,*args, **kwargs):
        try:
            phone=request.data['phone']
            try:
                customer=Customer.objects.get(phone=phone)
            except Customer.DoesNotExist:
                return Response({"error":_("the account not found")},status=status.HTTP_404_NOT_FOUND)
            if OTPRequest.checkRateLimitReached(phone=phone):
                return Response({'error': _('MANY OTP REQUESTS')}, status=status.HTTP_409_CONFLICT)
            otp=OTPRequest.objects.create(phone=phone,type=OTPRequest.Types.FORGET_PASSWORD)
            sms = SmsSender()
            if sms.send_otp(phone.replace('0', '966', 1), f"Your OTP for Update Your Password is: {otp}"):
                    return Response({'result': _('Wait to recive OTP message')}, status=status.HTTP_201_CREATED)
            else:
                    return Response({'error': _('Failed to send OTP')}, status=status.HTTP_502_BAD_GATEWAY)
        except: 
             return Response({"error":_("Can not change password try agin")},status=status.HTTP_400_BAD_REQUEST)
            

        
class CustomerPasswordUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomerPasswordUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            customer = self.request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
        except:
             return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        # Check if the old password is correct
        if not customer.check_password(old_password):
            return Response({'error': _('Invalid old password')}, status=status.HTTP_400_BAD_REQUEST)

        # Update the password
        customer.set_password(new_password)
        customer.save()

        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
    

class CustomerAddressRetrieveUpdateDestroyAPIView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        customer = Customer.objects.get(pk=self.request.user.id)
        return customer
    
class CustomerUpdateAPIView(APIView):
    def put(self, request, pk):
        customer = Customer.objects.get(pk=self.request.user.id)
        serializer = CustomerUpdateSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)