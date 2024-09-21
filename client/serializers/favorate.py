from .product import ProductSerializer
from .service import ServiceListSerializer
from rest_framework import serializers
from ..models import FavorateProduct,FavorateService

class FavorateProductSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=FavorateProduct
        fields=['product']
        
class FavorateServiceSerializer(serializers.ModelSerializer):
    service=ServiceListSerializer(read_only=True)
    class Meta:
        model=FavorateService
        fields=['service']