

from rest_framework import serializers
from provider_details.models import  Product
from rest_framework import serializers
from order_cart.models import *
from ..models import *


class ProductSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.SerializerMethodField()
    favorate=serializers.SerializerMethodField()
    def get_favorate(self, obj):
        user = self.context['request'].user
        
        try:
            favorate_service = FavorateProduct.objects.get(product=obj, customer__phone=user.phone)
            return True
        except FavorateProduct.DoesNotExist:
            return False
    
    class Meta:
        model = Product
        exclude = ['store',]
    def get_price_after_offer(self, obj):
            if obj.offers is not None:
                return obj.price_after_offer
            return obj.price