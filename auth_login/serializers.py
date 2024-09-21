from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from provider_details.models import Store
from .models import *
from rest_framework import fields
from utils.validators import phoneValidator

class PhoneVitrifactionSerializer(serializers.Serializer):
    phone=fields.CharField()
    code=fields.CharField()

class MyAuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phoneValidator])
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            # Perform any additional validation if needed
            return attrs
        raise serializers.ValidationError('Phone and password are required.')

###### customer serializers

class PendingClientSerializer(serializers.ModelSerializer):
    phone=fields.CharField(validators=[phoneValidator])
    class Meta:
        model=PendingClient
        exclude=['otp']
        
class PendingProviderSerializer(serializers.ModelSerializer):
    phone=fields.CharField(validators=[phoneValidator])
    class Meta:
        model=PendingProvider
        exclude=['otp']
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','image','email','name', 'phone']
        
class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','image','email','name',]


class CustomerCreateAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'password']
        extra_kwargs = {
            'username': {'required': False}
        }

class CustomerPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['latitude','longitude','address']

#### end customer


###### provider serializers
class ProviderSerializer(serializers.ModelSerializer):
    remaining_duration = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Provider
        fields = ['id','username','name', 'phone','remaining_duration']
    def get_remaining_duration(self, obj):
        try:
             provider_subscription =ProviderSubscription.objects.get(provider=obj) 
        except ProviderSubscription.DoesNotExist:
            return 0
        
        return provider_subscription.remaining_duration()
        


class   ProviderCreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id','name','category','username','email','phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password field is write-only
        }
           
  

class ProviderPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class ProviderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['latitude','longitude','address']

#### end customer
class ProviderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['name','email',]
        
        
class PromotionSubscriptionSerializer(serializers.ModelSerializer):
    store=serializers.SerializerMethodField()
    class Meta:
        model = PromotionSubscription
        fields = ['image','store']
    def get_store(self,instance):
        store = Store.objects.filter(provider=instance.provider).first()  # Retrieve the first store instance from the queryset
        if store:
            return {'id': store.id, 'name': store.name}
        return None
   