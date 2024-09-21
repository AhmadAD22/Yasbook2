from rest_framework.response import Response
from rest_framework.views import APIView
from provider_details.models import Product
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from ..serializers.store import *
from ..serializers.product import *
from utils.subscriptions import active_stores
from utils.geographic import distance
from auth_login.models import Customer
from ..models import FavorateProduct
from django.utils.translation import gettext_lazy as _



class AddproductToFavorate(APIView):
     permission_classes=[IsAuthenticated]
     def post(self,request):
         try:
            product=Product.objects.get(id=request.data['product_id'])
         except Product.DoesNotExist:
             return Response({"error": _("product does not found!")}, status=status.HTTP_404_NOT_FOUND)
         customer=Customer.objects.get(phone=request.user.phone)
         try:
            favorate_product=FavorateProduct.objects.create(product=product,customer=customer)
            favorate_product.save()
         except :
             return Response({"error":_("product Already Added!")}, status=status.HTTP_409_CONFLICT)
         return Response({"result":"product Adedd to favorate"},status=status.HTTP_200_OK)
     
class DeleteproductFromFavorate(APIView):
     def post(self,request):
         try:
            product=Product.objects.get(id=request.data['product_id'])
         except Product.DoesNotExist:
             return Response({"error": _("product does not found!")}, status=status.HTTP_404_NOT_FOUND)
         customer=Customer.objects.get(phone=request.user.phone)
         try:
            favorate_product=FavorateProduct.objects.get(product=product,customer=customer)
            favorate_product.delete()
         except :
             return Response({"error": _("product Already Deleted!")}, status=status.HTTP_409_CONFLICT)
         return Response({"result":"product deleted from favorate"},status=status.HTTP_200_OK)
     
     