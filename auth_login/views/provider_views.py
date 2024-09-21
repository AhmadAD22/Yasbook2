
from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.authentication import TokenAuthentication
from provider_details.serializers import StoreForProviderWhenCreateSerializer
from rest_framework.views import APIView
from utils.error_handle import error_handler
from utils.sms import SmsSender

class ProviderRegisterView(APIView):
    def post(self,request,*args,**kwargs):
        serialized=PendingProviderSerializer(data=request.data)
          # check if user exists
        if Provider.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
            return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
        
        if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
            return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
        otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.REGISTER)
        if serialized.is_valid():
            serialized.save(otp=otp) 
            sms = SmsSender()
            if sms.send_otp(request.data['phone'].replace('0', '966', 1), f"Your OTP for registration is: {otp}"):
                return Response({'result': 'Wait to recive OTP message'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
            
class ProviderPhoneVerifyView(APIView):
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
                return Response({"error":"OTP is not correct!"},status.HTTP_404_NOT_FOUND)


#########  for Provider views
from django.http import HttpResponse

class ProviderDataAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProviderSerializer

    def get_object(self):
        return Provider.objects.get(id=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return HttpResponse(serializer.data, content_type='application/json; charset=utf-8')
    


class ProviderCreateAccountAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        
        phone = request.data['phone']
        code = request.data['code']
        print(phone)
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp=OTPRequest.objects.filter(phone=phone,
                                        code=code,                                            
                                        type=OTPRequest.Types.REGISTER).first()
            pendingProvider=otp.pendingProvider    

            # Check if phone or email already exist
            if pendingProvider.email:
                if  MyUser.objects.filter(email=pendingProvider.email).exists():
                    return Response({'error': 'email already exists'}, status=status.HTTP_409_CONFLICT)
            if MyUser.objects.filter(phone=phone).exists():
                return Response({'error': 'Phone number already exists'}, status=status.HTTP_409_CONFLICT)
            new_provider=Provider.objects.create(name=pendingProvider.fullName,phone=pendingProvider.phone,
                                                email=pendingProvider.email,category=pendingProvider.category)
            new_provider.password=make_password(request.data["password"])
            new_provider.save()
            
            # Create the associated store
            store_data = {
                'provider': new_provider,
            }
            store_serializer = StoreForProviderWhenCreateSerializer(data=store_data)
            store_serializer.is_valid()
            store_serializer.save()

            return Response({"result":"created"}, status=status.HTTP_201_CREATED)
        return Response({'error': 'The phone is not verified'})
        

        
      



class ProviderAuthToken(ObtainAuthToken):
    serializer_class =MyAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({'error': 'Unable to log in with provided credentials'}, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        
        User = get_user_model()
        try:
            user = MyUser.objects.get(phone=phone)
            provider = Provider.objects.get(phone=user.phone)

        except User.DoesNotExist:
            return Response({'error': 'not a provider account'}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_password(password, user.password):
            if provider.username == user.username:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': {
                        'id': provider.id,
                        'email': provider.email,
                        'phone': provider.phone,
                    }
                })
            
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class ProviderPasswordUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProviderPasswordUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        provider = self.request.user
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        # Check if the old password is correct
        if not provider.check_password(old_password):
            return Response({'detail': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the password
        provider.set_password(new_password)
        provider.save()

        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
    

class ProviderAddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderAddressSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        provider = Provider.objects.get(pk=self.request.user.id)
        return provider
########### end customer

class ProviderInfoRetrieveUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        provider = Provider.objects.get(pk=request.user.id)
        serializer = ProviderInfoSerializer(provider)
        return Response(serializer.data)

    def put(self, request):
        provider = Provider.objects.get(pk=request.user.id)
        
        serializer = ProviderInfoSerializer(provider, data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # Check if email already exist
            if email:
                if  Provider.objects.filter(email=email).exists():
                    return Response({'error': 'email already exists'}, status=status.HTTP_409_CONFLICT)
            
            serializer.save()
            return Response(serializer.data)
        return Response(error_handler(serializer.errors))
    
    
class PromotionSubscriptionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        subscriptions = [
                        subscription for subscription in PromotionSubscription.objects.all()
                        if not subscription.is_duration_finished()
                        ]
        serializer = PromotionSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
