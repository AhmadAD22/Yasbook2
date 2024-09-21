from django.shortcuts import render,redirect,get_object_or_404
from provider_details.models import StoreSpecialist

def service_order_report(request):
    return render(request,'provider/reports/sevice.html')

def product_order_report(request):
    return render(request,'provider/reports/product.html')

def specialist_order_report(request):
    store_specialists=StoreSpecialist.objects.filter(store__provider__phone=request.user.phone)
    return render(request,'provider/reports/specialist.html',{'store_specialists':store_specialists})


def warehouse_order_report(request):
    return render(request,'provider/reports/warehouse.html')


