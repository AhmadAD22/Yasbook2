from django.shortcuts import render, redirect,get_object_or_404

from auth_login.models  import *
from order_cart.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from datetime import datetime
from ..forms.product import ProductForm

@login_required(login_url='provider-login')
def product_list(request):
    product = Product.objects.filter(store__provider__phone=request.user.phone)
    context = {
        'products': product,
        'provider_id':request.user.id
    }
    return render(request,'provider/product/product_list.html', context)

@login_required(login_url='provider-login')
def create_product(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('provider-product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'provider/product/create_product.html', context)

@login_required(login_url='provider-login')
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('provider-product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product
    }
    
    return render(request, 'provider/product/update_product.html', context)

@login_required(login_url='provider-login')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('provider-product_list')
