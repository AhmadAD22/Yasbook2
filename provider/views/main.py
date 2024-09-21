from django.shortcuts import render,redirect,get_object_or_404
from auth_login.models import ProviderSubscription,Provider
from auth_login.models import *
from order_cart.models import *
from provider_details.models import * 

from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import Extract,ExtractMonth


def get_service_orders_by_month(provider):
    # Assuming you have a ServiceOrder model
    orders = ServiceOrder.objects.filter(service__store__provider=provider,status=Status.COMPLETED).annotate(month=Extract('date', 'month')).values('month').annotate(count=Count('id')).order_by('month')

    labels = []
    data = []
    for order in orders:
        labels.append(datetime(2023, order['month'], 1).strftime('%b'))
        data.append(order['count'])

    return labels, data

def get_product_orders_by_month(provider):
    orders = ProductOrder.objects.filter(product__store__provider=provider,status=Status.COMPLETED).annotate(month=ExtractMonth('date')).values('month').annotate(count=Count('id')).order_by('month')

    labels = []
    data = []
    for order in orders:
        labels.append(datetime(2023, order['month'], 1).strftime('%b'))
        data.append(order['count'])

    return labels, data


def get_services_statistics(orders,subscription):
    #count the sevice or product orders 
    orders_counts = orders.count()
    profit=subscription.service_profit* orders_counts
    return {'orders_counts':orders_counts,'profit':profit}

def get_product_statistics(orders, subscription):
    # Count the total quantity of products in the orders
    total_quantity = orders.exclude(quantity__isnull=True).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
    profit = subscription.product_profit * total_quantity if total_quantity is not None else 0
    if total_quantity is None:
        total_quantity=0
    else:
        total_quantity=int(total_quantity)
    
    return {'orders_counts':total_quantity, 'profit': profit}

def provider_main_dashboard(request):
    try:
        provider=Provider.objects.get(phone=request.user.phone)
    except Provider.DoesNotExist:
        return redirect('provider-login')
    
    service_count=Service.objects.filter(store__provider__id=request.user.id).count()
    product_count=Product.objects.filter(store__provider__id=request.user.id).count()
    specialist_count=StoreSpecialist.objects.filter(store__provider__id=request.user.id).count()
    product_order_count=ProductOrder.objects.filter(product__store__provider__id=request.user.id,status=Status.COMPLETED).count()
    service_order_count=ServiceOrder.objects.filter(service__store__provider__id=request.user.id,status=Status.COMPLETED).count()
    subscription=ProviderSubscription.objects.filter(provider__id=request.user.id)
    if subscription:
        subscription=subscription.first()
        subscription=subscription.remaining_duration()
    else:
        subscription=0
        
    service_labels, service_data = get_service_orders_by_month(provider)
    product_labels, product_data = get_product_orders_by_month(provider)
    
    
    providersubscription=ProviderSubscription.objects.get(provider__phone=request.user.phone)
    store=Store.objects.get(provider=providersubscription.provider)
    # Get Producta and Services that related with Store
    products=Product.objects.filter(store=store)
    services=Service.objects.filter(store=store)
    # Get accepted Product and Service orders that related with Store
    productorders = ProductOrder.objects.filter(product__in=products,status=Status.COMPLETED,collected=False)
    servicesorders = ServiceOrder.objects.filter(service__in=services,status=Status.COMPLETED,collected=False)
    #Calclate the count and price for orders that related with Store
    productorders_statistics=get_product_statistics(productorders,providersubscription)
    servicesorders_statistics=get_services_statistics(servicesorders,providersubscription)
    #Calclate Total  price and coutn for product and service orders that related with Store
    total_count=productorders_statistics.get('orders_counts')+ servicesorders_statistics.get('orders_counts')
    total_profit=productorders_statistics.get('profit')+ servicesorders_statistics.get('profit')
    total_statistics={
        'total_counts':total_count,
        'total_profit':total_profit
    }
    
    context={
        'service_count':service_count,
        'product_count':product_count,
        'specialist_count':specialist_count,
        'product_order_count':product_order_count,
        'service_order_count':service_order_count,
        'subscription':subscription,
        'service_labels':service_labels,
        'service_data':service_data,
        'product_labels':product_labels,
        'product_data':product_data,
        'total_statistics':total_statistics,
        'productorders_statistics': productorders_statistics,
        'servicesorders_statistics':servicesorders_statistics,
        
        
    }
    
    
    
    
    
    return render(request,'provider/provider_main.html',context=context)