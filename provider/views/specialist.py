from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from provider_details.models import StoreSpecialist,Store
from ..forms.specialist import StoreSpecialistForm,Store

@login_required(login_url='provider-login')
def store_specialist_list(request):
    specialists = StoreSpecialist.objects.filter(store__provider__phone=request.user.phone)
    context = {
        'specialists': specialists,
        'provider_id': request.user.id
    }
    return render(request, 'provider/store_specialist/list.html', context)

@login_required(login_url='provider-login')
def store_specialist_create(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    if request.method == 'POST':
        form = StoreSpecialistForm(request.POST, request.FILES)
        if form.is_valid():
            specialist = form.save(commit=False)
            specialist.store = store
            specialist.save()
            form.save_m2m()
            return redirect('store-specialist-list')
    else:
        form = StoreSpecialistForm()
    context = {
        'form': form
    }
    return render(request, 'provider/store_specialist/create.html', context)

@login_required(login_url='provider-login')
def store_specialist_update(request, pk):
    specialist = get_object_or_404(StoreSpecialist, pk=pk)
    if request.method == 'POST':
        form = StoreSpecialistForm(request.POST, request.FILES, instance=specialist)
        if form.is_valid():
            form.save()
            return redirect('store-specialist-list')
    else:
        form = StoreSpecialistForm(instance=specialist)
    context = {
        'form': form,
        'specialist': specialist
    }
    return render(request, 'provider/store_specialist/update.html', context)

@login_required(login_url='provider-login')
def store_specialist_delete(request, pk):
    specialist = get_object_or_404(StoreSpecialist, pk=pk)
    specialist.delete()
    return redirect('store-specialist-list')