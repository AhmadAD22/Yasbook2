from rest_framework import serializers
from provider_details.models import Service,Store
from ..models import *
from auth_login.models import Customer


class StoreForServiceListSerializer(serializers.ModelSerializer):
    latitude=serializers.CharField(source='provider.latitude')
    longitude=serializers.CharField(source='provider.longitude')
    address=serializers.CharField(source='provider.address')
    reviews=serializers.SerializerMethodField()
    def get_reviews(self, obj):
        reviews_data = obj.reviews_set.all()
        ratings = [review.rating for review in reviews_data]
        average = sum(ratings) / len(ratings) if ratings else 0
        return {"count":len(reviews_data),'average':average}
    
    class Meta:
        model=Store
        fields=['id','name','en_name','latitude','longitude','address','reviews']
        
class ServiceListSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.SerializerMethodField()
    store=StoreForServiceListSerializer(read_only=True)
    main_service=serializers.CharField(source='main_service.name')
    en_main_service=serializers.CharField(source='main_service.en_name')
    favorate=serializers.SerializerMethodField()
    def get_favorate(self, obj):
        user = self.context['request'].user
        
        try:
            favorate_service = FavorateService.objects.get(service=obj, customer__phone=user.phone)
            return True
        except FavorateService.DoesNotExist:
            return False
    
    class Meta:
        model = Service
        fields = ['id','image','en_name','name','price','price_after_offer','duration','main_service','en_main_service','store','favorate']
        
    def get_price_after_offer(self, obj):
            if obj.offers is not None:
                return obj.price_after_offer
            return obj.price
    

class ServiceSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.SerializerMethodField()
    store=StoreForServiceListSerializer(read_only=True)
    class Meta:
        model = Service
        fields=['id','image','name','price','price_after_offer','main_service','store']

    
    def get_price_after_offer(self, obj):
            if obj.offers is not None:
                return obj.price_after_offer
            return obj.price
   
    
