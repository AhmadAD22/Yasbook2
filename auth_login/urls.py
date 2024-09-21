from django.urls import path
from .views.provider_views import *
from .views.subscription_views import *
from .views.customer_view import *
from .views.common_views import *
urlpatterns = [
    ##  for customer links
    path('request_register',RegisterView.as_view()),
    path('phone_verify',PhoneVerifyView.as_view()),
    path('customer-info-profile',CustomerDataAPIView.as_view(),name='customer-data-get-request'),
    path('customer-create-account',CustomerCreateAccountAPIView.as_view(),name='customer-data-post-request'),
    path('customer-login', CustomerAuthToken.as_view()),
    path('customer-set-address', CustomerAddressRetrieveUpdateDestroyAPIView.as_view(), name='customer-addresses-list-create'),
    path('customer-password-update', CustomerPasswordUpdateAPIView.as_view(), name='customer-password-update'),
    path('customers/<int:pk>/update/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    ### end customer



    ## for provider links
    path('provider-request-register',ProviderRegisterView.as_view()),
    path('provider-phone_verify',ProviderPhoneVerifyView.as_view()),
    path('provider-info-profile',ProviderDataAPIView.as_view(),name='customer-data-get-request'),
    path('provider-create-account',ProviderCreateAccountAPIView.as_view(),name='provider-data-post-request'),
    path('provider-login', ProviderAuthToken.as_view()),
    path('provider-set-address', ProviderAddressRetrieveUpdateDestroyAPIView.as_view(), name='customer-addresses-list-create'),
    path('provider-info-update', ProviderInfoRetrieveUpdateAPIView.as_view(), name='provider-info-update-retrive'),
    ### end provider
    
    ###subscription details //admin panal
    path('subscription/<int:id>',subscription,name="subscription details"),
    path('subscription_details/<int:id>',subscription_details,name="subscription details"),
    path('promotion-subscriptions/', PromotionSubscriptionAPIView.as_view(), name='promotion-subscription-list'),
    
    #Common
    path('forget-password-request',ForgetPasswordRequestAPIView.as_view()),
    path('forget-pssword-verify-phone',VerifyPhoneAPIView.as_view()),
    
]   