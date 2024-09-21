from django.urls import path
from .views.store import *
from .views.service import *
from .views.product import *
from .views.favorate import *
urlpatterns = [
        #Store
        path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
        
        
        path('service-filter/', ServiceFilterAPIView.as_view(), name='service-filter'),
        path('service-search/', ServiceSearchAPIView.as_view(), name='service-search'),
        path('service/<int:category_id>/', ServicesByCategoryAPIView.as_view(), name='service-by-category'),
        path('service/<int:category_id>/<int:main_service_id>/', ServicesByCategoryAndMAinServiceAPIView.as_view(), name='service-by-category'),
        path('service-details/<int:service_id>/', ServiceDetailsAPIView.as_view(), name='service-by-category'),
        path('add-service-to-favorate/', AddServiceToFavorate.as_view(), name='add-service-to-favorate'),
        path('delete-service-from-favorate/', DeleteServiceFromFavorate.as_view(), name='delete-service-from-favorate'),
        path('add-product-to-favorate/', AddproductToFavorate.as_view(), name='add-product-to-favorate'),
        path('delete-product-from-favorate/', DeleteproductFromFavorate.as_view(), name='delete-product-from-favorate'),
        path('favorate/', FavoriteAPIView.as_view(), name='delete-product-from-favorate'),
        
        

]