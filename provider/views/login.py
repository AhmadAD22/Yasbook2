from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from auth_login.models import Provider,OTPRequest,MyUser
from ..forms.profile import AddProviderForm,PendingProviderForm
from categroy.models import Category
from utils.sms import SmsSender


def provider_signup(request):
    categories=Category.objects.all()
    return render(request, 'provider/provider_signup.html',{'categories':categories})

def reset_forgotten_password(request, phone):
    str_phone=str(phone)
    formatted_phone = '0' + str_phone if not str_phone.startswith('0') else phone
    if request.method == 'POST':
        try:
            
            if 'password' in request.POST:
                new_password = request.POST['password']
                user = MyUser.objects.get(phone=formatted_phone)
                # Update the password
                user.set_password(new_password)
                user.save()
                return redirect('provider-login')
            else:
                error = "Password is required."
                return render(request, 'provider/password/reset_password.html', {'phone': formatted_phone, 'error': error})
        except MyUser.DoesNotExist:
            error = "User not found!"
            return render(request, 'provider/password/reset_password.html', {'phone': formatted_phone, 'error': error})
    return render(request, 'provider/password/reset_password.html', {'phone': formatted_phone})

def provider_verify_otp(request,phone):
    
    if request.method == 'POST':
        otp=OTPRequest.objects.filter(phone=phone,
                                        code=request.POST['otp'],
                                        isUsed=False,
                                        type=OTPRequest.Types.FORGET_PASSWORD).first()
        if otp:
            # deactivate otp code
            otp.isUsed=True
            otp.save()
            return redirect('reset_forgotten_password',phone)
        else:
            error="The Code is not correct!"
            render(request, 'provider/password/verify_otp.html',{'phone':phone,'error':error})
    return render(request, 'provider/password/verify_otp.html',{'phone':phone})

def provider_send_otp(request,phone):
    if request.method == 'POST':
        str_phone=str(phone)
        formatted_phone = '0' + str_phone if not str_phone.startswith('0') else phone
        try:
            user=MyUser.objects.get(phone=formatted_phone)
        except MyUser.DoesNotExist:
            error="There is no Account with this number!"
            return render(request, 'provider/password/send_otp.html',{'phone':formatted_phone,'error':error})
        if OTPRequest.checkRateLimitReached(phone=phone):
            error='MANY_OTP_REQUESTS'
            return render(request, 'provider/password/send_otp.html',{'phone':formatted_phone,'error':error})
        otp=OTPRequest.objects.create(phone=phone,type=OTPRequest.Types.FORGET_PASSWORD)  
        sms = SmsSender()
        if sms.send_otp(formatted_phone.replace('0', '966', 1), f"Your OTP for Update Your Password is: {otp}"):
                return redirect("provider_verify_otp",int(phone))
        else:
            error='Failed to send OTP", "SMS_SEND_FAILED'
            return render(request, 'provider/password/send_otp.html',{'phone':formatted_phone,'error':error})
        
    return render(request, 'provider/password/send_otp.html',{'phone':phone})


def login_view(request):
    if request.user.is_authenticated:
             if Provider.objects.filter(phone=request.user.phone):
                return redirect('provider-main-dashboard')
        
            
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        fcm_token = request.POST.get('fcm_token')
        print(fcm_token)
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            try:
                provider=Provider.objects.get(phone=user.phone)
            except Provider.DoesNotExist:
                error_message = 'Is Not a provider account'
                return render(request, 'provider/provider_login.html', {'error_message': error_message})
            login(request, user)
            provider.fcm_token=fcm_token
            provider.save()
            return redirect('provider-main-dashboard')
        else:
            error_message = 'Invalid phone number or password'
            return render(request, 'provider/provider_login.html', {'error_message': error_message})
    else:
        return render(request, 'provider/provider_login.html')
    
    
def provider_logout_view(request):
    logout(request)
    return redirect('provider-login')


