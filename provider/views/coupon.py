from django.shortcuts import render, redirect,get_object_or_404
from auth_login.models  import *
from order_cart.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from datetime import datetime
from ..forms.coupon import CouponForm

@login_required(login_url='provider-login')
def coupon_list(request):
    coupons = Coupon.objects.filter(provider__phone=request.user.phone)
    context = {
        'coupons': coupons,
        'provider_id':request.user.id
    }
    return render(request,'provider/coupon/coupon_list.html', context)

@login_required(login_url='provider-login')
def create_coupon(request):
    provider = get_object_or_404(Provider,phone=request.user.phone)
    
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.provider = provider
            coupon.save()
            return redirect('provider-coupon_list')
    else:
        form = CouponForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'provider/coupon/create_coupon.html', context)

@login_required(login_url='provider-login')
def update_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('provider-coupon_list')
    else:
        form = CouponForm(instance=coupon)
    
    context = {
        'form': form,
        'coupon': coupon
    }
    
    return render(request, 'provider/coupon/update_coupon.html', context)

@login_required(login_url='provider-login')
def delete_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    coupon.delete()
    return redirect('provider-coupon_list')
