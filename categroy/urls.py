from django.urls import path
from .views import *

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='main-category-list-create'),
    path('main-service',MainServiceListView.as_view(),name='facility-get-request'),
    path('main-service/<int:category_id>/',MainServiceByCategoryListView.as_view(),name='facility-get-request'),

]