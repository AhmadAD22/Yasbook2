from django.shortcuts import render,get_object_or_404,redirect
from auth_login.models import Provider
from order_cart.models import ServiceOrder ,Status
from django.contrib.auth.decorators import login_required
from utils.notifications import NotificationsHelper,OrdersUpdates


@login_required(login_url='provider-login')
def service_orders_view(request):
    provider = Provider.objects.get(phone=request.user.phone)
    service_orders = ServiceOrder.objects.filter(service__store__provider=provider)
    accepted_orders=service_orders.filter(status=Status.IN_PROGRESS)
    new_orders=service_orders.filter(status=Status.PENDING)
    canceled_oreders=service_orders.filter(status=Status.CANCELLED)
    rejected_orders=service_orders.filter(status=Status.REJECTED)
    complated_orders=service_orders.filter(status=Status.COMPLETED)
    
    context={
        'accepted_orders':accepted_orders,
        'new_orders':new_orders,
        'canceled_oreders':canceled_oreders,
        'rejected_orders':rejected_orders,
        'complated_orders':complated_orders,
        
    }
    
    return render(request, 'provider/orders/service.html',context=context)


@login_required(login_url='provider-login')

def service_order_details(request, id):
    service_order = get_object_or_404(ServiceOrder, id=id)

    context = {
        'service_order': service_order
    }

    return render(request, 'provider/orders/service_details.html', context)

@login_required(login_url='provider-login')
def accept_service_order(request, id):
    service_order = get_object_or_404(ServiceOrder, id=id)
    service_order.status=Status.IN_PROGRESS
    service_order.save()
    client=service_order.customer
    NotificationsHelper.sendServiceOrderUpdates(OrdersUpdates.PROVIDER_ACCEPTED_PRODUCT_ORDER,service_order,client)
    return redirect('provider-service-orders')

@login_required(login_url='provider-login')
def reject_service_order(request, id):
    service_order = get_object_or_404(ServiceOrder, id=id)
    service_order.status=Status.REJECTED
    service_order.save()
    client=service_order.customer
    NotificationsHelper.sendServiceOrderUpdates(OrdersUpdates.PROVIDER_REJECTED_SERVICE_ORDER,service_order,client)
    return redirect('provider-service-orders')

@login_required(login_url='provider-login')
def complate_service_order(request, id):
    service_order = get_object_or_404(ServiceOrder, id=id)
    service_order.status=Status.COMPLETED
    service_order.save()
    client=service_order.customer
    NotificationsHelper.sendServiceOrderUpdates(OrdersUpdates.PRODUCT_COMPLATED,service_order,client)
    return redirect('provider-service-orders')



