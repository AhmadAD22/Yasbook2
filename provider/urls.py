from django.urls import path
from.views.login import *
from .views.main import *
from .views.products import *
from .views.service import *
from .views.coupon import *
from .views.specialist import *
from .views.question import *
from .views.opening import *
from .views.store import *
from .views.service_order import *
from .views.product_order import *
from .views.reports import *
from .views.profile import *
urlpatterns = [
    path('login',login_view,name="provider-login"),
    path('logout',provider_logout_view,name="provider-logout"),
    path('provider_signup/', provider_signup, name='provider_signup'),
    path('update/', provider_update, name='provider_update'),
    path('profile/', provider_profile, name='provider_profile'),
    path('password-send-otp/<int:phone>', provider_send_otp, name='provider_send_otp'),
    path('password-verify-otp/<int:phone>', provider_verify_otp, name='provider_verify_otp'),
    path('reset-forgotten-password/<int:phone>', reset_forgotten_password, name='reset_forgotten_password'),
    
    path('',provider_main_dashboard,name="provider-main-dashboard"),
    # Products
    path('product/create/', create_product, name='provider-create_product'),
    path('product/list/',product_list, name='provider-product_list'),
    path('product/update/<int:id>/', update_product, name='provider-update_product'),
    path('product/delete/<int:id>/', delete_product, name='provider-delete_product'),
    #Services
    path('services/', service_list, name='provider-service_list'),
    path('services/create/', create_service, name='provider-create_service'),
    path('services/update/<int:id>/',update_service, name='provider-update_service'),
    path('services/delete/<int:id>/',delete_service, name='provider-delete_service'),
    #Coupon
    path('coupons/', coupon_list, name='provider-coupon_list'),
    path('coupons/create/', create_coupon, name='provider-create_coupon'),
    path('coupons/update/<int:id>/',update_coupon, name='provider-update_coupon'),
    path('coupons/delete/<int:id>/',delete_coupon, name='provider-delete_coupon'),
    
    path('specialists/', store_specialist_list, name='store-specialist-list'),
    path('specialists/create/',store_specialist_create, name='store-specialist-create'),
    path('specialists/<int:pk>/update/', store_specialist_update, name='store-specialist-update'),
    path('specialists/<int:pk>/delete/',store_specialist_delete, name='store-specialist-delete'),
    
    path('common-questions/', common_question_list, name='common_question_list'),
    path('common-questions/create/', common_question_create, name='common_question_create'),
    path('common-questions/<int:question_id>/edit/',common_question_edit, name='common_question_edit'),
    path('common-questions/<int:question_id>/delete/',common_question_delete, name='common_question_delete'),
    
    path('store-openings/', store_opening_list, name='store_opening_list'),
    path('store-openings/create/', store_opening_create, name='store_opening_create'),
    path('store-openings/<int:opening_id>/edit/', store_opening_edit, name='store_opening_edit'),
    path('store-openings/<int:opening_id>/delete/', store_opening_delete, name='store_opening_delete'),
    
    path('store-settings/',store_update_view, name='store_update-settings'),
    
    
     path('service-orders/',service_orders_view, name='provider-service-orders'),
     path('service-orders/<int:id>',service_order_details, name='provider-service-orders-details'),
     path('service-orders/<int:id>/accept',accept_service_order, name='accept_service_order'),
     path('service-orders/<int:id>/reject',reject_service_order, name='reject_service_order'),
     path('service-orders/<int:id>/compalte',complate_service_order, name='compalte_service_order'),
     
    path('product-orders/', product_orders_view, name='provider-product-orders'),
    path('product-orders/<int:id>/', product_order_details, name='productorder-details'),
    path('product-orders/<int:id>/accept/', accept_product_order, name='accept-product-order'),
    path('product-orders/<int:id>/reject/', reject_product_order, name='reject-product-order'),
    path('product-orders/<int:id>/complate/', complate_product_order, name='complate-product-order'),
    
    path('report/service',service_order_report,name="service_order_report"),
    path('report/product',product_order_report,name="product_order_report"),
    path('report/specialist',specialist_order_report,name="specialist_order_report"),
    path('report/warehouse',warehouse_order_report,name="warehouse_report"),
    
    
    
    
             ]   