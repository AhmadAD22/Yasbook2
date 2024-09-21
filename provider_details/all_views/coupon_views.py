from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Coupon
from ..serializers import CouponSerializer
from utils.error_handle import error_handler
from datetime import datetime


class CouponListCreateAPIView(APIView):
    def get(self, request):
        expired_coupons = Coupon.objects.filter(expired__lt=datetime.now())
        non_expired_coupons = Coupon.objects.filter(expired__gte=datetime.now())
        expired_coupons_serializer = CouponSerializer(expired_coupons, many=True)
        non_expired_coupons_serializer=CouponSerializer(non_expired_coupons, many=True)
        coupons={
            "expired":expired_coupons_serializer.data,
            "non_expired":non_expired_coupons_serializer.data
        }
        
        return Response(coupons)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class CouponRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Coupon.objects.get(pk=pk)
        except Coupon.DoesNotExist:
            return Response({"error":"Coupon Does Not Exist!"})

    def get(self, request, pk):
        coupon = self.get_object(pk)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    def put(self, request, pk):
        coupon = self.get_object(pk)
        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        coupon = self.get_object(pk)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ExpiredAndNonExpiredCouponsAPIView(APIView):
    def get(self, request):
        expired_coupons = Coupon.objects.filter(expired__lt=datetime.now())
        non_expired_coupons = Coupon.objects.filter(expired__gte=datetime.now())
        expired_coupons_serializer = CouponSerializer(expired_coupons, many=True)
        non_expired_coupons_serializer=CouponSerializer(non_expired_coupons, many=True)
        coupons={
            "expired":expired_coupons_serializer.data,
            "non_expired":non_expired_coupons_serializer.data
        }
        
        return Response(coupons)