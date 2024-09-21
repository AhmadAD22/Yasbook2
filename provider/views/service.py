from django.shortcuts import render, redirect, get_object_or_404
from auth_login.models import *
from order_cart.models import *
from django.contrib.auth.decorators import login_required
from ..forms.service import ServiceForm

@login_required(login_url='provider-login')
def service_list(request):
    services = Service.objects.filter(store__provider__phone=request.user.phone)
    context = {
        'services': services,
        'provider_id': request.user.id
    }
    return render(request, 'provider/service/service_list.html', context)

@login_required(login_url='provider-login')
def create_service(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)

    if request.method == 'POST':
        form = ServiceForm(data=request.POST, files=request.FILES, store=store)
        if form.is_valid():
                service = form.save(commit=False)
                service.store = store
                service.save()
                service.specialists.set(form.cleaned_data['specialists'])
                return redirect('provider-service_list')
    else:
        form = ServiceForm(store=store)

    context = {
        'form': form
    }

    return render(request, 'provider/service/create_service.html', context)

@login_required(login_url='provider-login')
def update_service(request, id):
    service = get_object_or_404(Service, id=id)
    store = service.store  # Get the store associated with the service

    if request.method == 'POST':
        form = ServiceForm(store=store, data=request.POST, files=request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('provider-service_list')
    else:
        form = ServiceForm(store=store, instance=service)

    context = {
        'form': form,
        'service': service
    }

    return render(request, 'provider/service/update_service.html', context)

@login_required(login_url='provider-login')
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    return redirect('provider-service_list')