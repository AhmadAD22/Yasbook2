from rest_framework import serializers
from .models import *
from auth_login.serializers import CustomerSerializer
from auth_login.models import ProviderSubscription
from order_cart.models import *
from django.db.models import Q,Sum

#Order Reports
class ServiceOrderReportSerializer(serializers.ModelSerializer):
    customer=serializers.CharField(source='customer.name', read_only=True)
    app_fees = serializers.SerializerMethodField()
    service=serializers.CharField(source='service.name', read_only=True)
    service_price=serializers.SerializerMethodField()
    class Meta:
        model = ServiceOrder
        fields = ['id','customer', 'service','date','service_price','collected','app_fees']
    def get_app_fees(self, obj):
        provider_subscription =ProviderSubscription.objects.get(provider=obj.service.store.provider) 
        if provider_subscription:
            return provider_subscription.service_profit
        return None
    def get_service_price(self, obj):
        return obj.price_with_coupon()
    
class SpecialistServiceOrderReportSerializer(serializers.ModelSerializer):
    app_fees = serializers.SerializerMethodField()
    service=serializers.CharField(source='service.name', read_only=True)
    main_service=serializers.CharField(source='service.main_service.name', read_only=True)
    service_price=serializers.SerializerMethodField()
    class Meta:
        model = ServiceOrder
        fields = ['id','main_service', 'service','date','service_price','status','app_fees']
    def get_app_fees(self, obj):
        provider_subscription =ProviderSubscription.objects.get(provider=obj.service.store.provider) 
        if provider_subscription:
            return provider_subscription.service_profit
        return None
    def get_service_price(self, obj):
        return obj.price_with_coupon()

class ProductOrderReportSerializer(serializers.ModelSerializer):
    app_fees = serializers.SerializerMethodField()
    customer = serializers.CharField(source='customer.name', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.SerializerMethodField()
    def get_product_price(self, obj):
        return obj.price_with_coupon()
    def get_app_fees(self, obj):
        provider_subscription =ProviderSubscription.objects.get(provider=obj.product.store.provider) 
        if provider_subscription:
            return provider_subscription.service_profit
        return None

    class Meta:
        model = ProductOrder
        fields = ['id', 'customer', 'product', 'quantity', 'product_price', 'status', 'collected', 'date', 'app_fees']
        
class warehouseReportSerializer(serializers.ModelSerializer):
    remaining_quantity = serializers.SerializerMethodField(read_only=True)
    reserved_quantity=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name',  'remaining_quantity','reserved_quantity']

    def get_remaining_quantity(self, obj):
        
        return obj.quantity
    def get_reserved_quantity(self, obj):
        product_orders = ProductOrder.objects.filter(Q(product=obj) &
            (Q(status=Status.COMPLETED) | Q(status=Status.IN_PROGRESS)))
        total_quantity = product_orders.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return total_quantity

    


## for provider app
class StoreStorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = StoreStory
        fields = ['image', ]
        
class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = ['id','question', 'answer',]
        read_only_fields = ['id',]
        
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['image', 'name', 'about','whatsapp_link']
        
class StoreDetailsSerializer(serializers.ModelSerializer):
    latitude = serializers.CharField(source='provider.latitude',read_only=True)
    longitude = serializers.CharField(source='provider.longitude',read_only=True)
    address = serializers.CharField(source='provider.address',read_only=True)
    openings = serializers.SerializerMethodField()
    common_question = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['image', 'name', 'about','whatsapp_link', 'latitude', 'longitude','address','openings','common_question']
    def get_openings(self, obj):
        # Customize the serialization of 'openings' field here
        return StoreAOpeningSerializer(obj.storeopening_set.all(), many=True).data
    def get_common_question(self, obj):
        # Customize the serialization of 'common_question' field here
        return CommonQuestionSerializer(CommonQuestion.objects.filter(store=obj), many=True).data


    

class StoreForProviderWhenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['provider']

class MainServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainService
        fields = ['id','name']
        read_only_fields = ['name']
        
class StoreSpecialistSerializer(serializers.ModelSerializer):
    specialistworks = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    class Meta:
        model = StoreSpecialist
        fields = ['id', 'name', 'phone', 'image', 'specialistworks']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].required = False
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialistworks'] = MainServiceSerializer(instance.specialistworks.all(), many=True).data
        return representation
    # def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()

        # # Add your custom delete logic here
        # # For example, you can perform additional checks or actions before deleting the instance

        # self.perform_destroy(instance)
        
    
class StoreOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreOpening
        fields = ['id','day', 'time_start', 'time_end']


class StoreGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreGallery
        exclude = ['store']

class ServiceSerializer(serializers.ModelSerializer):
    specialists = serializers.SerializerMethodField()
    price_after_offer = serializers.SerializerMethodField()
    class Meta:
        model = Service
        exclude = ['store']

    def get_specialists(self, instance):
        specialists = instance.specialists.all()
        return [{'id': specialist.id, 'name': specialist.name} for specialist in specialists]
    
    def get_price_after_offer(self, obj):
            if obj.offers is not None:
                return obj.price_after_offer
            return obj.price
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialists'] = self.get_specialists(instance)
        return representation
    
class ProductSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.SerializerMethodField()
    class Meta:
        model = Product
        exclude = ['store',]
    def get_price_after_offer(self, obj):
            if obj.offers is not None:
                return obj.price_after_offer
            return obj.price

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        exclude = ['customer']


#### store ui fpr customer

from rest_framework import serializers
from .models import Store, StoreSpecialist, StoreOpening, StoreGallery, Service, Product

class StoreASpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSpecialist
        exclude = ['store']

class StoreAOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreOpening
        exclude = ['store']

class StoreAGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreGallery
        exclude = ['store']

class ServiceASerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['store']
        
from client.models import *
from client.serializers.service import StoreForServiceListSerializer
class ProductASerializer(serializers.ModelSerializer):
    store=StoreForServiceListSerializer(read_only=True)
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
        fields='__all__'

class ReviewsStorSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    class Meta:
        model = Reviews
        exclude = ['store']
        
class StoreAdminServicesSerializer(serializers.ModelSerializer):
    main_service=serializers.CharField(source='main_service.name', read_only=True)
    class Meta:
        model = StoreAdminServices
        fields = ["main_service"]
    
class NearbyFeaturedStoreOrderSerializer(serializers.ModelSerializer):
    address=serializers.CharField(source='provider.address', read_only=True)
    reviews = serializers.SerializerMethodField()
    main_services=serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = ['id','image', 'name', 'about','address','reviews','main_services']
        
    def get_reviews(self, obj):
        reviews_data = ReviewsStorSerializer(obj.reviews_set.all(), many=True).data
        ratings = [review['rating'] for review in reviews_data]
        average = sum(ratings) / len(ratings) if ratings else 0
        return {"count":len(reviews_data),'average':average}
    def get_main_services(self, obj):
        main_services=StoreAdminServices.objects.filter(store=obj)
        
        return [ main_service.main_service.name  for main_service in main_services ]
    

class StoreADetailSerializer(serializers.ModelSerializer):
    specialists = serializers.SerializerMethodField()
    openings = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    address=serializers.CharField(source='provider.address', read_only=True)
    phone=serializers.CharField(source='provider.phone', read_only=True)
    


    def get_specialists(self, obj):
        # Customize the serialization of 'specialists' field here
        return StoreASpecialistSerializer(obj.storespecialist_set.all(), many=True).data

    def get_openings(self, obj):
        # Customize the serialization of 'openings' field here
        return StoreAOpeningSerializer(obj.storeopening_set.all(), many=True).data

    def get_gallery(self, obj):
        # Customize the serialization of 'gallery' field here
        return StoreAGallerySerializer(obj.storegallery_set.all(), many=True).data

    def get_services(self, obj):
        # Customize the serialization of 'services' field here
        return ServiceSerializer(obj.service_set.all(), many=True).data

    def get_products(self, obj):
        # Customize the serialization of 'products' field here
        return ProductSerializer(obj.product_set.all(), many=True).data

    def get_reviews(self, obj):
        reviews_data = ReviewsSerializer(obj.reviews_set.all(), many=True).data
        ratings = [review['rating'] for review in reviews_data]
        average = sum(ratings) / len(ratings) if ratings else 0
        return {'reviews_data':reviews_data,"count":len(reviews_data),'average':average}

    class Meta:
        model = Store
        fields = ['id','image','name','address','phone','about','created_at','openings', 'gallery', 'products', 'services', 'specialists','reviews']

class StoreFollowingListSerializer(serializers.ModelSerializer):
    store=StoreSerializer(read_only=True)

    class Meta:
        model = FollowingStore
        fields = '__all__'
        read_only_fields=['customer']

class StoreFollowingSerializer(serializers.ModelSerializer):
    # store=StoreSellerSerializer(read_only=True)
    class Meta:
        model = FollowingStore
        fields = '__all__'
        read_only_fields=['customer']
        
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        exclude=['provider']