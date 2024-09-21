from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from auth_login.models import Provider



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes=[]
    permission_classes = []


class MainServiceListView(generics.ListAPIView):

    serializer_class = MainServiceSerializer
    # authentication_classes=[]
    # permission_classes = []

    def get_queryset(self):
        provider=Provider.objects.get(username=self.request.user.username)
        return MainService.objects.filter(category_id=provider.category.id)
    
class MainServiceByCategoryListView(generics.ListAPIView):

    serializer_class = MainServiceSerializer
    authentication_classes=[]
    permission_classes = []

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return MainService.objects.filter(category_id=category_id)