
from rest_framework import serializers
from provider_details.models import Store, StoreSpecialist, StoreOpening, StoreGallery, Service, Product
from rest_framework import serializers
from auth_login.serializers import CustomerSerializer
from auth_login.models import ProviderSubscription
from order_cart.models import *
from django.db.models import Q,Sum
from ..models import *




class ServiceSerializer(serializers.ModelSerializer):
    specialists = serializers.SerializerMethodField()
    price_after_offer = serializers.SerializerMethodField()
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

class ProductASerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['store']

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
    
class ReviewsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Reviews
            exclude = ['customer']
class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = ['id','question', 'answer',]
        read_only_fields = ['id',]
    

class StoreADetailSerializer(serializers.ModelSerializer):
    specialists = serializers.SerializerMethodField()
    openings = serializers.SerializerMethodField()
    main_services=serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    address=serializers.CharField(source='provider.address', read_only=True)
    phone=serializers.CharField(source='provider.phone', read_only=True)
    common_question = serializers.SerializerMethodField()
    

    def get_common_question(self, obj):
        # Customize the serialization of 'common_question' field here
        return CommonQuestionSerializer(CommonQuestion.objects.filter(store=obj), many=True).data
    def get_specialists(self, obj):
        # Customize the serialization of 'specialists' field here
        return StoreASpecialistSerializer(obj.storespecialist_set.all(), many=True).data

    def get_openings(self, obj):
        # Customize the serialization of 'openings' field here
        return StoreAOpeningSerializer(obj.storeopening_set.all(), many=True).data

    def get_main_services(self, obj):
        main_services=StoreAdminServices.objects.filter(store=obj)
        
        return [ {'id':main_service.main_service.id,'name':main_service.main_service.name}  for main_service in main_services ]

    def get_services(self, obj):
        # Customize the serialization of 'services' field here
        return ServiceSerializer(obj.service_set.all(), many=True,context={'request': self.context['request']}).data

    def get_products(self, obj):
        # Customize the serialization of 'products' field here
        return ProductSerializer(obj.product_set.all(), many=True,context={'request': self.context['request']}).data

    def get_reviews(self, obj):
        reviews_data = ReviewsSerializer(obj.reviews_set.all(), many=True).data
        ratings = [review['rating'] for review in reviews_data]
        average = sum(ratings) / len(ratings) if ratings else 0
        return {'reviews_data':reviews_data,"count":len(reviews_data),'average':average}

    class Meta:
        model = Store
        fields = ['id','image','name','en_name','address','phone','about','created_at','openings', 'main_services', 'products', 'services', 'specialists','reviews','common_question']
