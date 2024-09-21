from rest_framework.response import Response
from rest_framework.views import APIView
from provider_details.models import Service,Product
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from ..serializers.service import ServiceListSerializer
from ..serializers.product import ProductSerializer

from ..models import *
from auth_login.models import Customer
from ..models import FavorateService

class FavoriteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        # Get the customer from the request
        customer = Customer.objects.get(phone=request.user.phone)

        # Get the favorite products and services for the customer
        favorite_products = FavorateProduct.objects.filter(customer=customer).values_list('product_id', flat=True)
        favorite_services = FavorateService.objects.filter(customer=customer).values_list('service_id', flat=True)
        products=Product.objects.filter(id__in=favorite_products)
        services=Service.objects.filter(id__in=favorite_services)


        # Serialize the data
        product_serializer = ProductSerializer(products, many=True,context={'request': request})
        service_serializer =ServiceListSerializer (services, many=True,context={'request': request})

        # Combine the data and return it
        data = {
            'favorite_products': product_serializer.data,
            'favorite_services': service_serializer.data
        }
        return Response(data=data)