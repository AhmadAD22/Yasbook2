from rest_framework.response import Response
from rest_framework.views import APIView
from provider_details.models import Service
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from ..serializers.store import *
from ..serializers.service import *
from utils.subscriptions import active_stores
from utils.geographic import distance
from auth_login.models import Customer
from ..models import FavorateService
from django.utils.translation import gettext_lazy as _

class ServiceSearchAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('query', '')
        stores=active_stores()
        # Get the services from the stores with active subscriptions
        services = Service.objects.filter(store__in=stores)
        services = services.filter(name__icontains=query)
        serializer = ServiceListSerializer(services, many=True,context={'request': request})
        return Response(serializer.data)


class ServiceFilterAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        minimum_price = request.query_params.get('minimum_price')
        maximum_price = request.query_params.get('maximum_price')
        rating = request.query_params.get('rating')
        category_id = request.query_params.get('category_id')

            
        stores=active_stores()
        # Get the services from the stores with active subscriptions
        services = Service.objects.filter(store__in=stores)

        if category_id is not None:
            services = services.filter(main_service__category__id=category_id)

        if minimum_price is not None and maximum_price is not None:
            services = services.filter(price__gte=minimum_price, price__lte=maximum_price)

        if rating is not None:
            services = services.annotate(store_avg_rating=Avg('store__reviews__rating')).filter(store_avg_rating__gte=rating)

        serializer = ServiceListSerializer(services, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServicesByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        stores = active_stores()
        # Get the services from the stores with active subscriptions
        services = Service.objects.filter(store__in=stores)
        services = services.filter(main_service__category__id=category_id)
        serializer = ServiceListSerializer(services, many=True,context={'request': request})
        return Response(serializer.data)
    
class ServicesByCategoryAndMAinServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id,main_service_id):
        stores = active_stores()
        # Get the services from the stores with active subscriptions
        services = Service.objects.filter(store__in=stores)
        services = services.filter(main_service__category__id=category_id)
        services = services.filter(main_service__id=main_service_id)
        serializer = ServiceListSerializer(services, many=True,context={'request': request})
        return Response(serializer.data)
    
class ServiceDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"error":_("service does not found!")}, status=status.HTTP_404_NOT_FOUND)

        customer = Customer.objects.get(phone=request.user.phone)
        store_distance = distance(customer.latitude, customer.longitude, service.store.provider.latitude, service.store.provider.longitude)
        print(store_distance)

        serializer = ServiceSerializer(service)
        data = serializer.data
        data['store_distance'] = store_distance

        return Response(data)
    
class AddServiceToFavorate(APIView):
     def post(self,request):
         try:
            service=Service.objects.get(id=request.data['service_id'])
         except Service.DoesNotExist:
             return Response({"error": _("service does not found!")}, status=status.HTTP_404_NOT_FOUND)
         customer=Customer.objects.get(phone=request.user.phone)
         try:
            favorate_service=FavorateService.objects.create(service=service,customer=customer)
            favorate_service.save()
         except :
             return Response({"error": _("service Already Added!")}, status=status.HTTP_409_CONFLICT)
         return Response({"result":"Service Adedd to favorate"},status=status.HTTP_200_OK)
     
class DeleteServiceFromFavorate(APIView):
     def post(self,request):
         try:
            service=Service.objects.get(id=request.data['service_id'])
         except Service.DoesNotExist:
             return Response({"error": _("service does not found!")}, status=status.HTTP_404_NOT_FOUND)
         customer=Customer.objects.get(phone=request.user.phone)
         try:
            favorate_service=FavorateService.objects.get(service=service,customer=customer)
            favorate_service.delete()
         except :
             return Response({"error": _("service Already Deleted!")}, status=status.HTTP_409_CONFLICT)
         return Response({"result":"Service deleted from favorate"},status=status.HTTP_200_OK)
     
     

             
         