from django.shortcuts import render, redirect
from .forms import CustomerForm
from auth_login.models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required


######Customer###########################
@staff_member_required(login_url='login')
def customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'users/customer/customer_list.html', context)

@staff_member_required(login_url='login')
def add_customer(request):
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('customer_list')  # Redirect to the customer list view
    else:
        form = AddCustomerForm()
        
    context = {'form': form}
    return render(request, 'users/customer/add_customer.html', context)

@staff_member_required(login_url='login')
def update_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to the customer list view
    else:
        form = CustomerForm(instance=customer)
        
    context = {'form': form}
    return render(request, 'users/customer/update_customer.html', context)

@staff_member_required(login_url='login')
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('customer_list') 
###################ENnd Customer#######################

######Provider###########################

@staff_member_required(login_url='login')
def provider_list(request):
    providers = Provider.objects.all()
    return render(request, 'users/provider/provider_list.html', {'providers': providers})


@staff_member_required(login_url='login')
def add_provider(request):
    if request.method == 'POST':
        form = AddProviderForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('provider_list')
    else:
        form = AddProviderForm()
    return render(request, 'users/provider/add_provider.html', {'form': form})

@staff_member_required(login_url='login')
def update_provider(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'users/provider/update_provider.html', {'form': form, 'provider': provider})

@staff_member_required(login_url='login')
def delete_provider(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    provider.delete()
    return redirect('provider_list')
###################ENnd Provider#######################


######Admin###########################
@staff_member_required(login_url='login')
def admins_list(request):
    admins = AdminUser.objects.all()
    return render(request, 'users/admin/admin_list.html', {'admins': admins})


@staff_member_required(login_url='login')
def add_admin(request):
    if request.method == 'POST':
        form = AddAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin_list')
    else:
        form = AddAdminForm()
    return render(request, 'users/admin/add_admin.html', {'form': form})


@staff_member_required(login_url='login')
def update_admin(request, admin_id):
    admin = get_object_or_404(AdminUser, id=admin_id)
    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('admin_list')
    else:
        form = AdminForm(instance=admin)
    return render(request, 'users/admin/update_admin.html', {'form': form, 'admin': admin})

@staff_member_required(login_url='login')
def delete_admin(request, admin_id):
    admin = get_object_or_404(AdminUser, id=admin_id)
    admin.delete()
    return redirect('admin_list')