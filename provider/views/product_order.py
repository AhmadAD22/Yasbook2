from django.shortcuts import render, get_object_or_404, redirect
from auth_login.models import Provider
from order_cart.models import ProductOrder, Status
from django.contrib.auth.decorators import login_required
from utils.notifications import NotificationsHelper,OrdersUpdates

@login_required(login_url='provider-login')
def product_orders_view(request):
    provider = Provider.objects.get(phone=request.user.phone)
    product_orders = ProductOrder.objects.filter(product__store__provider=provider)
    pending_orders = product_orders.filter(status=Status.PENDING)
    accepted_orders = product_orders.filter(status=Status.IN_PROGRESS)
    canceled_orders = product_orders.filter(status=Status.CANCELLED)
    rejected_orders = product_orders.filter(status=Status.REJECTED)
    completed_orders = product_orders.filter(status=Status.COMPLETED)

    context = {
        'pending_orders': pending_orders,
        'accepted_orders': accepted_orders,
        'canceled_orders': canceled_orders,
        'rejected_orders': rejected_orders,
        'completed_orders': completed_orders,
    }

    return render(request, 'provider/orders/product.html', context)

@login_required(login_url='provider-login')
def product_order_details(request, id):
    product_order = get_object_or_404(ProductOrder, id=id)

    context = {
        'product_order': product_order
    }

    return render(request, 'provider/orders/product_details.html', context)

@login_required(login_url='provider-login')

def accept_product_order(request, id):
    product_order = get_object_or_404(ProductOrder, id=id)
    product_order.status = Status.IN_PROGRESS
    product_order.save()
    client=product_order.customer
    NotificationsHelper.sendProductOrderUpdates(OrdersUpdates.PROVIDER_ACCEPTED_PRODUCT_ORDER,product_order,client)
    return redirect('provider-product-orders')

@login_required(login_url='provider-login')
def reject_product_order(request, id):
    product_order = get_object_or_404(ProductOrder, id=id)
    product_order.status = Status.REJECTED
    product_order.save()
    client=product_order.customer
    NotificationsHelper.sendProductOrderUpdates(OrdersUpdates.PROVIDER_REJECTED_PRODUCT_ORDER,product_order,client)
    return redirect('provider-product-orders')
@login_required(login_url='provider-login')

def complate_product_order(request, id):
    product_order = get_object_or_404(ProductOrder, id=id)
    product_order.status = Status.COMPLETED
    product_order.save()
    client=product_order.customer
    NotificationsHelper.sendProductOrderUpdates(OrdersUpdates.PRODUCT_COMPLATED,product_order,client)
    return redirect('provider-product-orders')