from django.db import models
from django.contrib.auth.models import AbstractUser
from categroy.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone,date
from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import BaseUserManager
import random 
from django.core.exceptions import ValidationError
from django.db.models import Q,Avg



class UserManager(BaseUserManager):
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractUser):
    last_name = None
    first_name = None
    username=models.CharField(max_length=255, blank=False,null=True)
    name = models.CharField(max_length=255, blank=False, verbose_name='الاسم الكامل')
    email = models.EmailField(null=True, blank=True, verbose_name='البريد الإلكتروني',)
    phone = models.CharField(max_length=10,unique=True, verbose_name='رقم الهاتف',)
    is_active=models.BooleanField(default=True,blank=True,verbose_name='نشاط الحساب')
    is_staff=models.BooleanField(default=False,blank=True,verbose_name='دخول لوحة التحكم')
    is_superuser=models.BooleanField(default=False,blank=True,verbose_name='سوبر أدمن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء',blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث',blank=True,null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)  # Store FCM token
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()
    


class Customer(MyUser):
    image = models.ImageField(upload_to='media/customers/',null=True,blank=True,)
    latitude = models.CharField(max_length=255, verbose_name='Latitude', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='Longitude', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Provider(MyUser):
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    latitude = models.CharField(max_length=255, verbose_name='Latitude', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='Longitude', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'


class AdminUser(MyUser):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

def expireDefault():
    return datetime.now() + timedelta(minutes=5)


def otpCodeDefault():
    rand=random.Random()
    code=''
    for _ in range(4):
        code+=str(rand.randint(0,9))
    return code     
from datetime import datetime, timedelta

class OTPRequest(models.Model):
    class Types(models.TextChoices):
        REGISTER='REGISTER'
        RESET_PHONE='RESET_PHONE'
        FORGET_PASSWORD='FORGET_PASSWORD'

    phone=models.CharField(max_length=15,null=True,blank=True)
    code=models.CharField(max_length=4,default=otpCodeDefault)
    expireAt=models.DateTimeField(default=expireDefault)
    createdAt=models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=18,choices=Types.choices)
    isUsed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    def is_expired(self):
        current_time = datetime.now()
        print(current_time > self.expireAt)
        return current_time > self.expireAt

    def identifier(self):
        return self.phone 

    def clean(self):
        if  self.phone in ('',None):
            raise ValidationError("should provide phone")
        return super().clean()

    def save(self, **kwargs):
        self.full_clean()
        if not self.isUsed:
            pass
        return super().save(**kwargs)
    
    def checkRateLimitReached(phone=None, **kwargs):
        current_datetime = datetime.now()
        fifteen_minutes_ago = current_datetime - timedelta(minutes=15)
        return OTPRequest.objects.filter(
            Q(phone=phone)& Q(createdAt__lt=fifteen_minutes_ago)
        ).count() >= 5
    
        
class PendingClient(models.Model):
    fullName=models.CharField(max_length=60)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    otp=models.OneToOneField(OTPRequest,on_delete=models.CASCADE,related_name='pendingClient')
    
class PendingProvider(models.Model):
    fullName=models.CharField(max_length=60)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    otp=models.OneToOneField(OTPRequest,on_delete=models.CASCADE,related_name='pendingProvider')




from django.db import models
from datetime import timedelta, datetime
from provider_details.models import Provider

class ProviderSubscription(models.Model):
    DURATION_CHOICES = (
        (30, '30 days'),
        (60, '60 days'),
        (90, '90 days'),
        (180, '180 days'),
        (365, '365 days'),
        (730, '730 days'),
    )

    provider = models.OneToOneField(Provider, verbose_name="provider", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Subscription date")
    duration_days = models.IntegerField(choices=DURATION_CHOICES, verbose_name="Duration")
    service_profit = models.IntegerField(default=0, blank=False, verbose_name='service profit')
    store_subscription = models.BooleanField(verbose_name='Store subscription', default=False)
    product_profit = models.IntegerField(default=0, blank=True, verbose_name='product profit')

    @property
    def duration(self):
        return timedelta(days=self.duration_days)

    def remaining_duration(self):
        current_date = datetime.now().date()
        subscription_end_date = self.date + self.duration
        remaining_days = (subscription_end_date - current_date).days
        return max(remaining_days, 0)

    def is_duration_finished(self):
        current_date = datetime.now().date()
        end_date = self.date + self.duration
        return current_date > end_date
    
    
    def __str__(self):
        return self.provider.name + " Remaining:  "+str(self.remaining_duration())+ " Days, Finished: " + str(self.is_duration_finished())






class PromotionSubscription(models.Model):
    DURATION_CHOICES = (
        (3, '3 days'),
        (7, '7 days'),
        (15, '15 days'),
        (30, '30 days'),
        (45, '45 days'),
        
    )
    
    provider = models.OneToOneField(Provider, verbose_name="provider", on_delete=models.CASCADE)
    promotion_date = models.DateField(blank=True, null=True, verbose_name="Promotion start date")
    promotion_duration_days = models.IntegerField(choices=DURATION_CHOICES, verbose_name="Promotion Duration", blank=True, null=True)
    profit = models.IntegerField(default=0, blank=True, verbose_name='product profit')
    image = models.ImageField(upload_to='media/provider/',null=True,blank=True, verbose_name='رفع الصورة')

    @property
    def promotion_duration(self):
        if self.promotion_duration_days:
            return timedelta(days=self.promotion_duration_days)
        return None

    def remaining_duration(self):
        if self.promotion_date and self.promotion_duration:
            current_date = date.today()
            promotion_end_date = self.promotion_date + self.promotion_duration
            remaining_days = (promotion_end_date - current_date).days
            return max(remaining_days, 0)
        return None

    def is_duration_finished(self):
        remaining_duration = self.remaining_duration()
        return remaining_duration == 0
    
    def __str__(self):
        return self.provider.name + " Remaining:  "+str(self.remaining_duration())+ " Days, Finished: " + str(self.is_duration_finished())
    
    def delete(self, *args, **kwargs):
        # Delete the associated image
        if self.image:
            default_storage.delete(self.image.path)
        
        super().delete(*args, **kwargs)
    
class Notification(models.Model):
    title=models.CharField(max_length=70)
    titleArgs=models.JSONField(default=list)
    body=models.TextField()
    bodyArgs=models.JSONField(default=list)
    sentAt=models.DateTimeField(auto_now_add=True)
    localized=models.BooleanField(default=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product_order=models.ForeignKey('order_cart.ProductOrder',on_delete=models.CASCADE,blank=True, null=True)
    service_order=models.ForeignKey('order_cart.ServiceOrder',on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        ordering=['-sentAt']    
