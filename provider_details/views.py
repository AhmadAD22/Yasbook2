from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from auth_login.models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import status
from utils.geographic import get_nearest_store
from django.db.models import Count
from utils.error_handle import error_handler
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_login.serializers import PromotionSubscriptionSerializer
from client.serializers.service import ServiceListSerializer
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.utils.translation import gettext_lazy as _


class ServiceOrderReportAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    def get(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        store = Store.objects.get(provider=provider)
        services = Service.objects.filter(store=store)
        service_orders = ServiceOrder.objects.filter(service__in=services,status=Status.COMPLETED)

        if request.GET.get('collected_filter') == 'collected':
            service_orders = service_orders.filter(collected=False)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            service_orders = service_orders.filter(date__range=(start_date, end_date))

        total_service = service_orders.count()
        total_app_fee=total_service * subscription.service_profit
        total_service_price = sum(order.price_with_coupon() for order in service_orders)
        serializer = ServiceOrderReportSerializer(service_orders, many=True)

        context = {
            'service_orders': serializer.data,
            'total_service_price': total_service_price,
            'total_app_fee':total_app_fee   
        }
        return Response(context)
    
class SpecialistServiceOrderReportAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    def get(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        specialist_id=request.GET.get('specialist_id')
        specialist_orders = ServiceOrder.objects.filter(specialist__id=specialist_id)
        if request.GET.get('collected_filter') == 'collected':
            specialist_orders = specialist_orders.filter(collected=False)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            specialist_orders = specialist_orders.filter(date__range=(start_date, end_date))

        total_complated_service = specialist_orders.filter(status=Status.COMPLETED).count()
        total_app_fee=total_complated_service * subscription.service_profit
        serializer = SpecialistServiceOrderReportSerializer(specialist_orders, many=True)

        context = {
            'service_orders': serializer.data,
            'total_complated_service': total_complated_service,
            'total_app_fee':total_app_fee
        }
        return Response(context)

class ProductOrderReportAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    def get(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
          if not subscription.store_subscription:
               return Response({'error':'Your have not Products  subscription'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        store = Store.objects.get(provider=provider)
        products = Product.objects.filter(store=store)
        product_orders = ProductOrder.objects.filter(product__in=products,status=Status.COMPLETED)

        if request.GET.get('collected') == 'false':
            product_orders = product_orders.filter(collected=False)

        # Check if start_date and end_date are provided
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            product_orders = product_orders.filter(date__range=[start_date, end_date])

        total_products = product_orders.count()
        total_app_fee=total_products*subscription.product_profit
        total_product_price = sum(order.price_with_coupon() for order in product_orders)
        serializer = ProductOrderReportSerializer(product_orders, many=True)

        context = {
            'product_orders': serializer.data,
            'total_app_fee': total_app_fee,
            'total_product_price':total_product_price
        }
        return Response(context)

class warehouseReportAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication,SessionAuthentication]  
    def get(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
          if not subscription.store_subscription:
               return Response({'error':'Your have not Products  subscription'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        store = Store.objects.get(provider=provider)
        products = Product.objects.filter(store=store)
        product_orders = ProductOrder.objects.filter(Q(product__in=products) &
            (Q(status=Status.COMPLETED) | Q(status=Status.IN_PROGRESS)))
        

        # Check if start_date and end_date are provided
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            product_orders = product_orders.filter( date__range=[start_date, end_date])
            
            products = products.filter(id__in=product_orders.values('product_id').distinct())

        
        total_remaining_quantity = sum(product.quantity for product in products)
        total_reserved_quantity= sum(order.quantity for order in product_orders)
        
        serializer = warehouseReportSerializer(products, many=True)

        context = {
    
            'product': serializer.data,
            'total_remaining_quantity': total_remaining_quantity,
            'total_reserved_quantity':total_reserved_quantity
        }
        return Response(context)


### for provider app
class StoreUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        provider = Provider.objects.get(phone=self.request.user.phone)
        return Store.objects.get(provider=provider)

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        serializer = StoreDetailsSerializer(store)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        store = self.get_object()
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

    
class StoreSpecialistListCreateView(APIView):
    serializer_class = StoreSpecialistSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        queryset = StoreSpecialist.objects.filter(store__provider=provider)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        store = Store.objects.get(provider=provider)
        specialistworks = request.data.get("specialistworks")
        
        specialistworks_list = specialistworks.split(',')
        converted_list = [int(item) for item in specialistworks_list if item.strip()]
        
        # Create a mutable copy of request.data
        mutable_data = request.data.copy()
        mutable_data.setlist("specialistworks", converted_list)
        
        serializer = self.serializer_class(data=mutable_data)
        if serializer.is_valid():
            serializer.save(store=store, specialistworks=converted_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class StoreSpecialistRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(StoreSpecialist, pk=pk)

    def get(self, request, pk, format=None):
        specialist = self.get_object(pk)
        serializer = StoreSpecialistSerializer(specialist)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        specialist = self.get_object(pk)
        serializer = StoreSpecialistSerializer(specialist, data=request.data)
        specialistworks = request.data.get("specialistworks")
        specialistworks_list = specialistworks.split(',')
        converted_list = [int(item) for item in specialistworks_list]
        if serializer.is_valid():
            serializer.save(specialistworks=converted_list)
            return Response(serializer.data)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        specialist = self.get_object(pk)
        specialist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoreOpeningListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreOpeningSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider=Provider.objects.get(phone=self.request.user.phone)

        return StoreOpening.objects.filter(store__provider=provider)

    def perform_create(self, serializer):
        provider=Provider.objects.get(phone=self.request.user.phone)
        store=Store.objects.get(provider=provider)
        serializer.save(store=store)

class StoreOpeningRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoreOpening.objects.all()
    serializer_class = StoreOpeningSerializer
    permission_classes = [IsAuthenticated]



class StoreGalleryListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreGallerySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider = Provider.objects.get(phone=self.request.user.phone)
        return StoreGallery.objects.filter(store__provider=provider)

    def perform_create(self, serializer):
        provider = Provider.objects.get(phone=self.request.user.phone)
        store = Store.objects.get(provider=provider)
        serializer.save(store=store)

class StoreGalleryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoreGallery.objects.all()
    serializer_class = StoreGallerySerializer
    permission_classes = [IsAuthenticated]


class ServiceListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return ServiceSerializer
    
    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        # Check if the provider have subscription or not  
        try:
            provider_subscription=ProviderSubscription.objects.get(provider=provider)
            if (provider_subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            return Response({'error':'You do not have subscription'})
        services = Service.objects.filter(store__provider=provider)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        store = Store.objects.get(provider=provider)
        # Check if the provider have subscription or not  
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        specialists = request.data.get("specialists")
        converted_list =[]
        if specialists:
            specialists_list = specialists.split(',')
            converted_list = [int(item) for item in specialists_list]
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
                if(request.data.get('price')):
                    price = request.data.get('price')  # Assuming price is in the request data
                    calculated_price = float(price) + subscription.service_profit
                    serializer.save(store=store, price=calculated_price,specialists=converted_list)
                else:
                    calculated_price=float(subscription.service_profit)
                    serializer.save(store=store, price=calculated_price,specialists=converted_list)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class ServiceRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Service, pk=pk)

    def get(self, request, pk, format=None):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        specialists = request.data.get("specialists")
        if not specialists:
            return Response({"error":"You must add least one specialist!"})
        specialists_list = specialists.split(',')
        converted_list = [int(item) for item in specialists_list]
        serializer = ServiceSerializer(data=request.data)
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save(specialists=converted_list)
            return Response(serializer.data)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        # Check if the provider have subscription or not  
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        # Check if the provider have a products subscription or not 
        if subscription.store_subscription:
            products = Product.objects.filter(store__provider=provider)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        error_messages={"error":"You do not have a product subscription"}
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        provider = Provider.objects.get(phone=request.user.phone)
        store = Store.objects.get(provider=provider)
        # Check if the provider have subscription or not  
        try:
          subscription=ProviderSubscription.objects.get(provider=provider)
          if (subscription.is_duration_finished()):
                return Response({'error':'Your subscription duration is finished'})
        except:
            error_messages={"error":"You do not have a subscription"}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        # Check if the provider have a products subscription or not 
        if subscription.store_subscription:# Store here is products subscription
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                if(request.data.get('price')):
                    price = request.data.get('price')  # Assuming price is in the request data
                    calculated_price = float(price) + subscription.product_profit
                    serializer.save(store=store, price=calculated_price)
                else:
                    calculated_price=float(subscription.product_profit)
                    serializer.save(store=store, price=calculated_price)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            
            return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        error_messages={"error":"You do not have a product subscription"}
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)




class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]




class ReviewsListCreateAPIView(APIView):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Assuming you want reviews related to the authenticated user's store
        customer = Customer.objects.get(phone=request.user.phone)
        reviews = Reviews.objects.filter(customer=customer)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Assuming you want to associate the review with the authenticated user's store
        customer = Customer.objects.get(phone=request.user.phone)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class ReviewsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]


### for store ui



class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreADetailSerializer
    permission_classes = []
    authentication_classes=[]



class ServiceListByStoreAndMainServiceView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = []
    authentication_classes=[]
    def get_queryset(self):
        store_id = self.kwargs['store_id']
        main_service_id = self.kwargs['main_service_id']
        return Service.objects.filter(store_id=store_id, main_service=main_service_id)
    
class ServiceListByMainServiceView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider = Provider.objects.get(phone=self.request.user.phone)
        store = Store.objects.get(provider=provider)
        main_service_id = self.kwargs['main_service_id']
        return Service.objects.filter(store=store, main_service=main_service_id)



class StoreListByMainServiceView(generics.ListAPIView):
    serializer_class = StoreADetailSerializer
    permission_classes = []
    authentication_classes=[]
    def get_queryset(self):
        main_service_id = self.kwargs['main_service_id']
        store_ids = StoreAdminServices.objects.filter(main_service=main_service_id).values_list('store_id', flat=True)
        return Store.objects.filter(id__in=store_ids)

class FollowingStoreListView(generics.ListAPIView):
    serializer_class = StoreFollowingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer=Customer.objects.get(phone=self.request.user.phone)
        return FollowingStore.objects.filter(customer=customer)
               
class FollowingStoreCreateView(generics.CreateAPIView):
    serializer_class = StoreFollowingSerializer
    permission_classes = [IsAuthenticated]


    
    def perform_create(self, serializer):
        customer=Customer.objects.get(phone=self.request.user.phone)
        store = serializer.validated_data['store']
        try:
            FollowingStore.objects.create(customer=customer, store=store)
        except IntegrityError:
            raise serializers.ValidationError("You are already following this store.")


class FollowingStoreDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer=Customer.objects.get(phone=self.request.user.phone)

        return FollowingStore.objects.filter(customer=customer)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, store_id=self.kwargs['store_id'])
    
#Salon page 
class FeaturedStoreNearbyStoreOrderAndStoryView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        provider_subscripted_ids=[]
        subscriptions=ProviderSubscription.objects.all()
        for subscription in subscriptions:
            if(not subscription.is_duration_finished()):
                provider_subscripted_ids.append(subscription.provider.id)
        subscripted_stores=Store.objects.filter(provider__id__in=provider_subscripted_ids).values_list('id', flat=True)
        promotion=PromotionSubscription.objects.all()
        promotion_serializer=PromotionSubscriptionSerializer(promotion,many=True)
        # Get the most ordered services for the customer
        most_ordered_services = ServiceOrder.objects\
                                  .values('service')\
                                  .annotate(order_count=Count('service'))\
                                  .order_by('-order_count')[:10]
        most_ordered_products =ProductOrder.objects.values('product').annotate(order_count=Count('id')).order_by('-order_count')[:5]
        product_ids = [product['product'] for product in most_ordered_products]
        products = Product.objects.filter(id__in=product_ids) 
        products_serializer = ProductASerializer(products, many=True,context={'request': request})          

        # Serialize the service data
        service_ids = [service['service'] for service in most_ordered_services]
        services = Service.objects.filter(id__in=service_ids)
        service_serializer = ServiceListSerializer(services, many=True,context={'request': request})
        ####nearest_stores######
        #Get nearest_stores by customer location and stores ids that have the main_service_id
        customer=Customer.objects.get(phone=self.request.user.phone)
        try:
        #Get customer for nearby stores
            nearbystores=get_nearest_store(customer_latitude=customer.latitude,customer_longitude=customer.longitude,store_ids=subscripted_stores)
        except:
            return Response({'error': _('Yor location undefined')}, status=status.HTTP_400_BAD_REQUEST)
        

        # Get the new services with offers that are not null
        new_services_with_offers = Service.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30),
            offers__isnull=False
        )
        service_offer_serializer = ServiceListSerializer(services, many=True,context={'request': request})
        customer=Customer.objects.get(phone=request.user.phone)
        customer_serializer=CustomerSerializer(customer)
        

        return Response({'promotion':promotion_serializer.data,'nearby_stores':nearbystores,'services':service_serializer.data,'products':products_serializer.data,'service_offer':service_offer_serializer.data,'customer':customer_serializer.data})
    

class NearbyStoreOrderByMainServiceView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        main_service_ids=request.data.get('main_service_ids')
        customer=Customer.objects.get(phone=self.request.user.phone)
        provider_subscripted_ids=[]
        subscriptions=ProviderSubscription.objects.all()
        for subscription in subscriptions:
            if(not subscription.is_duration_finished()):
                provider_subscripted_ids.append(subscription.provider.id)
        subscripted_stores=Store.objects.filter(provider__id__in=provider_subscripted_ids).values_list('id', flat=True)
        ####featured stores by number of followes######
        #list stores ids that have the main_service_id
        stores_have_selected_main_service_ides=[]
        if main_service_ids:
            stores_have_selected_main_service_ides = StoreAdminServices.objects.filter(main_service__in=main_service_ids).values_list('store_id', flat=True)
        else:
            stores_have_selected_main_service_ides=StoreAdminServices.objects.all().values_list('store_id', flat=True)
        # Convert the QuerySet to a set for intersection
        stores_have_selected_main_service_ides = set(stores_have_selected_main_service_ides)
        subscripted_stores=set(subscripted_stores)
        # Perform the intersection that ensures that Fetch subscripted stores that have the indicated main_service
        filtered_stores = subscripted_stores.intersection(stores_have_selected_main_service_ides)
        #Get ordered featured stores by number of followes
        try:
        #Get customer for nearby stores
            nearbystores=get_nearest_store(customer_latitude=customer.latitude,customer_longitude=customer.longitude,store_ids=filtered_stores)
        except:
            return Response({'error': 'Yor location undefined'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(nearbystores)   
    
class FeaturedStoreFollowersOrderView(generics.ListAPIView):

    serializer_class = NearbyFeaturedStoreOrderSerializer

    def get_queryset(self):
        main_service_id = self.kwargs['main_service_id']
        store_ids = StoreAdminServices.objects.filter(main_service=main_service_id).values_list('store_id', flat=True)
        customer=Customer.objects.get(id=self.request.user.id)
        return  Store.objects.filter(id__in=store_ids).annotate(num_followers=models.Count('followingstore')).order_by('-num_followers')
    
class EmailSendingView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        user=MyUser.objects.get(id=request.user.id)
        message="from: "+str( user.email)+"\n" + message
        if not (message and subject):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_mail(subject, message,"", ["yasafco@gmail.com"], fail_silently=False)
            
            return Response({'success': 'Email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class CommonQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        common_questions = CommonQuestion.objects.filter(store__provider__phone=request.user.phone  )
        serializer = CommonQuestionSerializer(common_questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        store = Store.objects.get(provider__phone=request.user.phone)
        serializer = CommonQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(store=store)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class CommonQuestionDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, format=None):
        common_question = CommonQuestion.objects.get(pk=pk)
        serializer = CommonQuestionSerializer(common_question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    
    
    #######Coupon
    
from django.utils import timezone

class CouponAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        current_datetime = timezone.now()
        expired_coupons = Coupon.objects.filter(provider__phone=request.user.phone, expired__lt=current_datetime)
        non_expired_coupons = Coupon.objects.filter(provider__phone=request.user.phone, expired__gte=current_datetime)

        expired_serializer = CouponSerializer(expired_coupons, many=True)
        non_expired_serializer = CouponSerializer(non_expired_coupons, many=True)

        response_data = {
            'expired_coupons': expired_serializer.data,
            'non_expired_coupons': non_expired_serializer.data
        }
        return Response(response_data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        provider = Provider.objects.get(phone=request.user.phone)
        if serializer.is_valid():
            expired = serializer.validated_data['expired']
            if expired < timezone.now():
                print(timezone.now())
                print(expired)
                return Response({'error': 'Coupon has already expired'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(provider=provider)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    
class CouponDeleteUpdateAPIView(APIView):
    # ...
    def get(self, request, coupon_id):
        try:
            coupon = Coupon.objects.get(id=coupon_id, provider__phone=request.user.phone)
        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon does not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    def put(self, request, coupon_id):
        try:
            coupon = Coupon.objects.get(id=coupon_id, provider__phone=request.user.phone)
        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon does not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            expired = serializer.validated_data['expired']
            if expired < timezone.now():
                return Response({'error': 'Coupon has already expired'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, coupon_id):
        try:
            coupon = Coupon.objects.get(id=coupon_id, provider__phone=request.user.phone)
        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon does not found'}, status=status.HTTP_400_BAD_REQUEST)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)