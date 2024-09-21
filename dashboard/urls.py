from django.urls import path
from .views import *
from .users import *
from .store import*
from . import category
from django.contrib.auth import views as auth_views


urlpatterns = [
path('test', test, name='test'),
path('config/update/', update_config, name='config_update'),
path('', login_view, name='login'),
path('logout/',logout_view, name='logout'),
path('main_dashboard/',main_dashboard,name="main_dashboard"),
###Provider subscription //admin panal
path('subscriptions/', provider_subscription_list, name='subscription_list'),
path('subscriptions/add/', add_provider_subscription, name='add_subscription'),
path('edit-provider-subscription/<int:provider_subscription_id>/', edit_provider_subscription, name='edit_provider_subscription'),
path('subscriptions/delete/<int:subscription_id>/', delete_provider_subscription, name='delete_subscription'),
path('subscription_details/<int:id>',subscription_details,name="subscription_details"),
path('subscription_product_order_details/<int:id>/', subscription_product_order_details, name='subscription_product_order_details'),
path('collect_product_order/<int:id>/', collect_product_order_details, name='collect_product_order'),
path('collect_servce_order/<int:id>/', collect_service_order_details, name='collect_service_order'),

path('subscription_service_order_details/<int:id>/', subscription_order_details, name='subscription_service_order_details'),
#services
path('service_create/<int:provider_id>/', create_service, name='create_service'),
path('services_list/<int:provider_id>/',service_list, name='service_list'),
path('update_services/<int:id>/', update_service, name='update_service'),
path('delete_services/<int:id>/', delete_service, name='delete_service'),
#####Products
path('product/create/<int:provider_id>/', create_product, name='create_product'),
path('product/list/<int:provider_id>/',product_list, name='product_list'),
path('product/update/<int:id>/', update_product, name='update_product'),
path('product/delete/<int:id>/', delete_product, name='delete_product'),
#Gallery
path('gallery/<int:provider_id>/', store_gallery_list, name='store_gallery_list'),
path('gallery/create/<int:provider_id>/', create_store_gallery, name='create_store_gallery'),
path('gallery/update/<int:id>/', update_store_gallery, name='update_store_gallery'),
path('gallery/delete/<int:id>/', delete_store_gallery, name='delete_store_gallery'),
path('reviews/<int:provider_id>/', review_list, name='review_list'),
#Reviews
path('reviews/<int:provider_id>/', review_list, name='review_list'),
path('reviews/create/<int:provider_id>/', create_review, name='create_review'),
path('reviews/update/<int:id>/', update_review, name='update_review'),
path('reviews/delete/<int:id>/', delete_review, name='delete_review'),
# Store and min services
path('store_admin_services/<int:provider_id>/', store_admin_services_list, name='store_admin_services_list'),
path('store_admin_services/create/<int:provider_id>/',create_store_admin_service, name='create_store_admin_service'),
path('store_admin_services/update/<int:id>/',update_store_admin_service, name='update_store_admin_service'),
path('store_admin_services/delete/<int:id>/',delete_store_admin_service, name='delete_store_admin_service'),
#promotion subscription
path('promotion-subscription/create/', create_promotion_subscription, name='create-promotion-subscription'),
path('promotion-subscription/update/<int:pk>/', update_promotion_subscription, name='update-promotion-subscription'),
path('promotion-subscription/delete/<int:pk>/', delete_promotion_subscription, name='delete-promotion-subscription'),
path('promotion-subscription/list/', list_promotion_subscriptions, name='promotion-subscription-list'),

####Customer
path('customer-list/', customer_list, name='customer_list'),
path('add-customer/', add_customer, name='add_customer'),
path('update-customer/<int:customer_id>/', update_customer, name='update_customer'),
path('delete-customer/<int:customer_id>/', delete_customer, name='delete_customer'),
####Provider
path('provider-list/', provider_list, name='provider_list'),
path('add-provider/', add_provider, name='add_provider'),
path('update-provider/<int:provider_id>/', update_provider, name='update_provider'),
path('delete-provider/<int:provider_id>/', delete_provider, name='delete_provider'),
####Admin
path('admins/', admins_list, name='admin_list'),
path('admins/add/', add_admin, name='add_admin'),
path('admins/update/<int:admin_id>/',update_admin, name='update_admin'),
path('admins/delete/<int:admin_id>/',delete_admin, name='delete_admin'),
########Store
path('store', store_list, name='store_list'),
path('store/create/', store_create, name='store_create'),
path('store/update/<int:pk>/', store_update, name='store_update'),
path('store/delete/<int:pk>/', store_delete, name='store_delete'),
###############Category
path('categories/create/', category.create_category, name='create_category'),
path('categories/', category.category_list, name='category_list'),
path('categories/<int:category_id>/update/', category.update_category, name='update_category'),
path('categories/<int:category_id>/delete/', category.delete_category, name='delete_category'),
###Main Service
path('main_service/create/', category.create_main_service, name='create_main_service'),
path('main_service/list/', category.main_service_list, name='main_service_list'),
path('main_service/update/<int:main_service_id>/', category.update_main_service, name='update_main_service'),
path('main_service/delete/<int:main_service_id>/', category.delete_main_service, name='delete_main_service'),
]
