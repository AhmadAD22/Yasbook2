from django.urls import path
from .views import *
 
urlpatterns = [
    
    #Customer Services
    path('customer-book-service/', ServiceOrderCreateView.as_view(), name='service-order-create'),
    path('service-order-details/<int:pk>/', ServiceOrderDetails.as_view(), name='service-order-details'),
    path('service-orders/<int:pk>/checkout/', ServiceOrderCheckoutView.as_view(), name='service-order-checkout'),
    path('customer-get-book-service/', ServiceOrderListView.as_view(), name='service-order-create'),
    path('cancel-service/<int:pk>/', CustomertServiceCancelOrder.as_view(), name='customer-cancel-service'),
    path('customer-book-product/', ProductOrderCreateView.as_view(), name='product-order-create'),
    path('follow-service-order/<int:pk>/', ServiceOrderFollow.as_view(), name='follow-service-order'),
    path('complate-service/<int:pk>/', CustomertServiceComplateOrder.as_view(), name='customer-cancel-service'),
    #Customer Products
    path('customer-book-product/', ProductOrderCreateView.as_view(), name='product-order-create'),
    path('product-orders/<int:pk>/checkout/', ProductOrderCheckoutView.as_view(), name='product-order-checkout'),
    path('follow-product-order/<int:pk>/', ProductOrderFollow.as_view(), name='follow-product-order'),
    path('product-order-details/<int:pk>/', ProductOrderDetails.as_view(), name='product-order-details'),
    path('complate-product/<int:pk>/', CustomertProductComplateOrder.as_view(), name='customer-cancel-product'),
    path('cancel-product/<int:pk>/', CustomertProductCancelOrder.as_view(), name='customer-cancel-product'),
    
    
    path('customer-current-service/', CurrentOrderCustomerListView.as_view(), name='customer-current-service'),
    path('customer-previous-service/', PreviousOrderCustomerListView.as_view(), name='customer-previous-service'),
    # path('favorate/')
    ## provider

    path('provider-get-current-book-service/', CurrentServiceOrderProviderListView.as_view(), name='service-order-create'),
    path('provider-get-previous-book-service/', PreviousServiceOrderProviderListView.as_view(), name='service-order-create'),
    path('provider-put-accept-service/<int:pk>/', ServiceOrderProviderAcceptView.as_view(), name='service-order-provider-accept'),
    path('provider-put-Accomplished-service/<int:pk>/', ServiceOrderProviderAccomplishedView.as_view(), name='service-order-provider-Accomplished'),
    path('provider-put-Accomplished-product/<int:pk>/', ProductOrderProviderAccomplishedclassView.as_view(), name='provider-put-Accomplished-product'),

    path('provider-get-current-book-product/',CurrentProductOrderProviderListView .as_view(), name='product-order'),
    path('provider-get-previous-book-product/',PreviousProductOrderProviderListView .as_view(), name='product-order'),
    path('provider-put-accept-product/<int:pk>/', ProductOrderProviderAcceptView.as_view(), name='service-order-provider-accept'),
    path('service-product-order-List/', ServiceAndProductListView.as_view(), name='product-order-create'),
    ######Cart
    path('cart/item/', CartItemAPIView.as_view(), name='cart-item-api'),
    path('cart/item/<int:item_id>/', CartItemAPIView.as_view(), name='cart-item-delete-api'),
    path('cart/service/', ServiceCartItemAPIView.as_view(), name='service-cart-item-api'),
    path('cart/service/<int:item_id>/', ServiceCartItemAPIView.as_view(), name='service-cart-item-delete-api'),
    #path('cart/checkout/', CartCheckoutAPIView.as_view(), name='cart-checkout'),
    path('cart/', CartAPIView.as_view(), name='cart'),
 ########Specialist-availability
    path('specialist-availability/<int:service_id>', SpecialistAvailabilityView.as_view(), name='specialist-availability'),
 
]