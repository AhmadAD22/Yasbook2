from rest_framework import serializers
from.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MainServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MainService
        exclude =['created_at','updated_on']
        
