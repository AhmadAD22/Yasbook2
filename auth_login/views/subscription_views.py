from ..models import *
from django.shortcuts import render
from order_cart.models import *

def get_statistics(orders,subscription):
    #count the sevice or product orders 
    orders_counts = orders.count()
    profit=subscription.profit_ratio* orders_counts
    return {'orders_counts':orders_counts,'profit':profit}

def subscription(request,id):
    providersubscription=ProviderSubscription.objects.get(id=id)
    store=Store.objects.get(provider=providersubscription.provider)
    # Get Producta and Services that related with Store
    products=Product.objects.filter(store=store)
    services=Service.objects.filter(store=store)
    # Get accepted Product and Service orders that related with Store
    productorders = ProductOrder.objects.filter(product__in=products,accept=True)
    servicesorders = ServiceOrder.objects.filter(service__in=services,accept=True)
    #Calclate the count and price for orders that related with Store
    productorders_statistics=get_statistics(productorders,providersubscription)
    servicesorders_statistics=get_statistics(servicesorders,providersubscription)
    #Calclate Total  price and coutn for product and service orders that related with Store
    total_count=productorders_statistics.get('orders_counts')+ servicesorders_statistics.get('orders_counts')
    total_profit=productorders_statistics.get('profit')+ servicesorders_statistics.get('profit')
    total_statistics={
        'total_counts':total_count,
        'total_profit':total_profit
    }
    return render(request,'subscription.html',{'providersubscription':providersubscription,
                                         'store':store,
                                         'products':products,
                                         'productorders_statistics': productorders_statistics,
                                        'servicesorders_statistics':servicesorders_statistics,
                                        'total_statistics':total_statistics
                                        })
    
def subscription_details(request,id):
    product_orders = ProductOrder.objects.all()
    service_orders = ServiceOrder.objects.all()
    context = {
        'product_orders': product_orders,
        'service_orders': service_orders,
    }
    return render(request,'subscription_details.html',context)
    