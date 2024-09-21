from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from auth_login.models  import *
from order_cart.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count,Sum
from datetime import datetime


def update_config(request):
    # Get the Config object or return a 404 if not found
    config = Config.objects.first()

    if request.method == 'POST':
        # Bind form to POST data
        form = ConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()  # Save the updated config
            return redirect('config_update')  # Redirect to a success page or another view
    else:
        form = ConfigForm(instance=config)  # Load existing data into the form

    return render(request, 'config_update.html', {'form': form, 'config': config})


def test (request):
    return render(request,'test.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main_dashboard')
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
            return redirect('main_dashboard')
        else:
            error_message = 'Invalid phone number or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@staff_member_required(login_url='login')
def main_dashboard (request):
    total_customers=Customer.objects.all().count()
    total_providers=Provider.objects.all().count()
    total_subscribed_providers=ProviderSubscription.objects.all().count()
    most_user_ordered_products = Customer.objects.annotate(order_count=Count('productorder')).order_by('-order_count')[:3]
    most_user_ordered_services = Customer.objects.annotate(order_count=Count('serviceorder')).order_by('-order_count')[:3]
    most_ordered_products = ProductOrder.objects.values('product__store__provider__name','product__name').annotate(total_orders=Sum('quantity')).order_by('-total_orders')[:3]
    most_ordered_services= ServiceOrder.objects.values('service__store__provider__name','service__name').annotate(total_orders=Count('service')).order_by('-total_orders')[:3]
    print(most_ordered_services)

    context={
        'total_customers':total_customers,
        'total_providers':total_providers,
        'total_subscribed_providers':total_subscribed_providers,
        'most_user_ordered_products':most_user_ordered_products,
        'most_user_ordered_services':most_user_ordered_services,
        'most_ordered_products':most_ordered_products,
        'most_ordered_services':most_ordered_services,
    }
    return render(request,'main_dashboard.html',context)


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

@staff_member_required(login_url='login')
def subscription_details(request,id):
    providersubscription=ProviderSubscription.objects.get(id=id)
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
    return render(request,'provider_subscription/subscription_details.html',{'providersubscription':providersubscription,
                                         'store':store,
                                         'products':products,
                                         'productorders_statistics': productorders_statistics,
                                        'servicesorders_statistics':servicesorders_statistics,
                                        'total_statistics':total_statistics
                                        })
@staff_member_required(login_url='login')
def subscription_product_order_details(request, id):
    providersubscription = ProviderSubscription.objects.get(id=id)
    store = Store.objects.get(provider=providersubscription.provider)
    products = Product.objects.filter(store=store)
    product_orders = ProductOrder.objects.filter(product__in=products)

    # Check if the filter checkbox is selected
    if request.GET.get('product_filter') == 'accepted':
        product_orders = product_orders.filter(accept=True)
    if request.GET.get('collected_filter') == 'collected':
        product_orders = product_orders.filter(collected=False)

    # Check if start_date and end_date are provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        product_orders = product_orders.filter(date__range=[start_date, end_date])

    total_products = product_orders.count()

    context = {
        'product_orders': product_orders,
        'providersubscription': providersubscription,
        'total_products': total_products,
    }
    return render(request, 'provider_subscription/order/subscription_product_order_details.html', context)

@staff_member_required(login_url='login')
def collect_product_order_details(request, id):
    if request.method == 'POST':
        selected_product_orders = request.POST.getlist('collected_product_orders')
        ProductOrder.objects.filter(id__in=selected_product_orders).update(collected=True)
        return redirect('collect_product_order',id)
    providersubscription = ProviderSubscription.objects.get(id=id)
    store = Store.objects.get(provider=providersubscription.provider)
    products = Product.objects.filter(store=store)
    product_orders = ProductOrder.objects.filter(product__in=products,collected=False,status=Status.IN_PROGRESS)
    product_statistics=get_product_statistics(product_orders,providersubscription)

    total_products = product_orders.count()

    context = {
        'product_orders': product_orders,
        'providersubscription': providersubscription,
        'total_products': total_products,
        'product_statistics':product_statistics
        
    }
    return render(request, 'provider_subscription/order/collect_product_order_details.html', context)

@staff_member_required(login_url='login')
def collect_service_order_details(request, id):
    if request.method == 'POST':
        selected_service_orders = request.POST.getlist('collected_service_orders')
        ServiceOrder.objects.filter(id__in=selected_service_orders).update(collected=True)
        return redirect('collect_service_order',id)
    providersubscription = ProviderSubscription.objects.get(id=id)
    store = Store.objects.get(provider=providersubscription.provider)
    service = Service.objects.filter(store=store)
    service_orders = ServiceOrder.objects.filter(service__in=service,collected=False,status=Status.IN_PROGRESS)
    service_statistics=get_services_statistics(service_orders,providersubscription)

    total_services = service_orders.count()

    context = {
        'service_orders': service_orders,
        'providersubscription': providersubscription,
        'total_services': total_services,
        'service_statistics':service_statistics
        
    }
    return render(request, 'provider_subscription/order/collect_service_order_details.html', context)

@staff_member_required(login_url='login')
def update_collected_status(request):
    if request.method == 'POST':
        selected_product_orders = request.POST.getlist('collected_product_orders')
        ProductOrder.objects.filter(id__in=selected_product_orders).update(collected=True)
        return redirect('product_orders')  # Redirect to the appropriate page after updating the status
    
    return render(request, 'update_collected_status.html')  # Render the template for updating the collected status

@staff_member_required(login_url='login')
def subscription_order_details(request, id):
    providersubscription = ProviderSubscription.objects.get(id=id)
    store = Store.objects.get(provider=providersubscription.provider)
    services = Service.objects.filter(store=store)

    service_orders = ServiceOrder.objects.filter(service__in=services)

    if request.GET.get('service_filter') == 'accepted':
        service_orders = service_orders.filter(status=Status.IN_PROGRESS)
    if request.GET.get('collected_filter') == 'collected':
        service_orders = service_orders.filter(collected=False)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        service_orders = service_orders.filter(date__range=(start_date, end_date))

    total_service = service_orders.count()

    context = {
        'service_orders': service_orders,
        'providersubscription': providersubscription,
        'total_service': total_service
    }
    return render(request, 'provider_subscription/order/subscription_service_order_details.html', context)

@staff_member_required(login_url='login')
def provider_subscription_list(request):
    subscriptions = ProviderSubscription.objects.all()
    return render(request, 'provider_subscription/subscription_list.html', {'subscriptions': subscriptions})

@staff_member_required(login_url='login')
def add_provider_subscription(request):
    if request.method == 'POST':
        form = ProviderSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = ProviderSubscriptionForm()
    return render(request, 'provider_subscription/subscription_form.html', {'form': form})

@staff_member_required(login_url='login')
def delete_provider_subscription(request, subscription_id):
    subscription = get_object_or_404(ProviderSubscription, id=subscription_id)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'subscription_confirm_delete.html', {'subscription': subscription})

@staff_member_required(login_url='login')
def edit_provider_subscription(request, provider_subscription_id):
    provider_subscription = ProviderSubscription.objects.get(id=provider_subscription_id)
    if request.method == 'POST':
        form = ProviderSubscriptionForm(request.POST, instance=provider_subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = ProviderSubscriptionForm(instance=provider_subscription)
    
    context = {'form': form}
    return render(request, 'provider_subscription/edit_provider_subscription.html', context)


########Promotion subscription###############
@staff_member_required(login_url='login')
def create_promotion_subscription(request):
    if request.method == 'POST':
        form = PromotionSubscriptionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('promotion-subscription-list')
    else:
        form = PromotionSubscriptionForm()
    return render(request, 'promotion_subscription/create_subscription.html', {'form': form})

@staff_member_required(login_url='login')
def update_promotion_subscription(request, pk):
    subscription = PromotionSubscription.objects.get(pk=pk)
    if request.method == 'POST':
        form = PromotionSubscriptionForm(request.POST, request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('promotion-subscription-list')
    else:
        form = PromotionSubscriptionForm(instance=subscription)
    return render(request, 'promotion_subscription/update_subscription.html', {'form': form})

@staff_member_required(login_url='login')
def delete_promotion_subscription(request, pk):
    subscription = PromotionSubscription.objects.get(pk=pk)
    subscription.delete()
    return redirect('promotion-subscription-list')


@staff_member_required(login_url='login')
def list_promotion_subscriptions(request):
    subscriptions = PromotionSubscription.objects.all()
    return render(request, 'promotion_subscription/list_subscriptions.html', {'subscriptions': subscriptions})


####Services
@staff_member_required(login_url='login')
def create_service(request, provider_id):
    store = Store.objects.get(provider__id=provider_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.store = store
            service.save()
            return redirect('service_list',provider_id)
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'provider_id': provider_id
    }
    return render(request, 'provider_subscription/service/create_service.html', context)


@staff_member_required(login_url='login')
def service_list(request,provider_id):
    services = Service.objects.filter(store__provider__id=provider_id)
    context = {
        'services': services,
        'provider_id':provider_id
    }
    return render(request, 'provider_subscription/service/service_list.html', context)

@staff_member_required(login_url='login')
def update_service(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list',service.store.provider.id)
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'service': service
    }
    return render(request, 'provider_subscription/service/update_service.html', context)

@staff_member_required(login_url='login')
def delete_service(request, id):
    service = Service.objects.get(id=id)
    service.delete()
    return redirect('service_list',service.store.provider.id)

#######Products
@staff_member_required(login_url='login')
def product_list(request,provider_id):
    product = Product.objects.filter(store__provider__id=provider_id)
    context = {
        'products': product,
        'provider_id':provider_id
    }
    return render(request, 'provider_subscription/product/product_list.html', context)

@staff_member_required(login_url='login')
def create_product(request, provider_id):
    store = get_object_or_404(Store, provider__id=provider_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('product_list', provider_id=store.provider.id)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'provider_id': provider_id
    }
    
    return render(request, 'provider_subscription/product/create_product.html', context)

@staff_member_required(login_url='login')
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', provider_id=product.store.provider.id)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product
    }
    
    return render(request, 'provider_subscription/product/update_product.html', context)

@staff_member_required(login_url='login')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    provider_id = product.store.provider.id
    product.delete()
    return redirect('product_list', provider_id=provider_id)

#### Store Gallery
@staff_member_required(login_url='login')
def store_gallery_list(request, provider_id):
    gallery = StoreGallery.objects.filter(store__provider__id=provider_id)
    context = {
        'galleries': gallery,
        'provider_id': provider_id
    }
    return render(request, 'provider_subscription/gallery/store_gallery_list.html', context)

@staff_member_required(login_url='login')
def create_store_gallery(request, provider_id):
    store = get_object_or_404(Store, provider__id=provider_id)
    
    if request.method == 'POST':
        form = StoreGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.store = store
            gallery.save()
            return redirect('store_gallery_list', provider_id=store.provider.id)
    else:
        form = StoreGalleryForm()
    
    context = {
        'form': form,
        'provider_id': provider_id
    }
    
    return render(request, 'provider_subscription/gallery/create_store_gallery.html', context)

@staff_member_required(login_url='login')
def update_store_gallery(request, id):
    gallery = get_object_or_404(StoreGallery, id=id)
    
    if request.method == 'POST':
        form = StoreGalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            return redirect('store_gallery_list', provider_id=gallery.store.provider.id)
    else:
        form = StoreGalleryForm(instance=gallery)
    
    context = {
        'form': form,
        'gallery': gallery
    }
    
    return render(request, 'provider_subscription/gallery/update_store_gallery.html', context)

@staff_member_required(login_url='login')
def delete_store_gallery(request, id):
    gallery = get_object_or_404(StoreGallery, id=id)
    provider_id = gallery.store.provider.id
    gallery.delete()
    return redirect('store_gallery_list', provider_id=provider_id)


# Reviews
@staff_member_required(login_url='login')
def review_list(request, provider_id):
    reviews = Reviews.objects.filter(store__provider__id=provider_id)
    context = {
        'reviews': reviews,
        'provider_id': provider_id
    }
    return render(request, 'provider_subscription/reviews/review_list.html', context)

@staff_member_required(login_url='login')
def create_review(request, provider_id):
    store = get_object_or_404(Store, provider__id=provider_id)
    
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.store = store
            review.save()
            return redirect('review_list', provider_id=store.provider.id)
    else:
        form = ReviewsForm()
    
    context = {
        'form': form,
        'provider_id': provider_id
    }
    
    return render(request, 'provider_subscription/reviews/create_review.html', context)

@staff_member_required(login_url='login')
def update_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    
    if request.method == 'POST':
        form = ReviewsForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list', provider_id=review.store.provider.id)
    else:
        form = ReviewsForm(instance=review)
    
    context = {
        'form': form,
        'review': review
    }
    
    return render(request, 'provider_subscription/reviews/update_review.html', context)

@staff_member_required(login_url='login')
def delete_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    provider_id = review.store.provider.id
    review.delete()
    return redirect('review_list', provider_id=provider_id)



#StoreAdminServices Add or delete or update main service to store

@staff_member_required(login_url='login')
def store_admin_services_list(request, provider_id):
    services = StoreAdminServices.objects.filter(store__provider__id=provider_id)
    context = {
        'services': services,
        'provider_id': provider_id
    }
    return render(request, 'provider_subscription/store_and_min_services/store_admin_services_list.html', context)

@staff_member_required(login_url='login')
def create_store_admin_service(request, provider_id):
    store = get_object_or_404(Store, provider__id=provider_id)
    
    if request.method == 'POST':
        form = StoreAdminServicesForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.store = store
            service.save()
            return redirect('store_admin_services_list', provider_id=provider_id)
    else:
        form = StoreAdminServicesForm()
    
    context = {
        'form': form,
        'provider_id': provider_id
    }
    
    return render(request, 'provider_subscription/store_and_min_services/create_store_admin_service.html', context)

@staff_member_required(login_url='login')
def update_store_admin_service(request, id):
    service = get_object_or_404(StoreAdminServices, id=id)
    
    if request.method == 'POST':
        form = StoreAdminServicesForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('store_admin_services_list', provider_id=service.store.provider.id)
    else:
        form = StoreAdminServicesForm(instance=service)
    
    context = {
        'form': form,
        'service': service
    }
    
    return render(request, 'provider_subscription/store_and_min_services/update_store_admin_service.html', context)

@staff_member_required(login_url='login')
def delete_store_admin_service(request, id):
    service = get_object_or_404(StoreAdminServices, id=id)
    store_id = service.store.id
    service.delete()
    return redirect('store_admin_services_list', provider_id=service.store.provider.id)