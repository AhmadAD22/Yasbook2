from utils.sms import SmsSender
from ..models import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _


class ForgetPasswordRequestAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        
        phone=request.data['phone']
        try:
            user=MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            return Response({"error":_("the account not found")},status=status.HTTP_404_NOT_FOUND)
        if OTPRequest.checkRateLimitReached(phone=phone):
            return Response({'error': _('MANY OTP REQUESTS')}, status=status.HTTP_409_CONFLICT)
        otp=OTPRequest.objects.create(phone=phone,type=OTPRequest.Types.FORGET_PASSWORD)  
        sms = SmsSender()
        if sms.send_otp(phone.replace('0', '966', 1), f"Your OTP for Update Your Password is: {otp}"):
                return Response({'result': _('Wait to recive OTP message')}, status=status.HTTP_201_CREATED)
        else:
                return Response({'error': _('Failed to send OTP')}, status=status.HTTP_502_BAD_GATEWAY)
        
class VerifyPhoneAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.FORGET_PASSWORD).first()
        if otp:
            # deactivate otp code
            otp.isUsed=True
            otp.save()
            return Response({"result":"OTP is correct"},status.HTTP_200_OK)
        else:
            return Response({"error":_("OTP is not correct!")},status.HTTP_404_NOT_FOUND)



class UpdateForgottenPasswordAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        try:
            phone=request.data['phone']
            new_password=request.data['password']
            user=MyUser.objects.get(phone=phone)
            # Update the password
            user.set_password(new_password)
            user.save()
            return Response({"result":"Password updated"},status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({"erorr":_("user does not found")},status.HTTP_404_NOT_FOUND)
            

        
        
    
    