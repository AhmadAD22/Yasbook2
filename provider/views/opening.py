from django.shortcuts import render, redirect, get_object_or_404
from ..forms.opening import StoreOpeningForm
from provider_details.models import StoreOpening, Store
from django.contrib.auth.decorators import login_required

@login_required(login_url='provider-login')
def store_opening_list(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    store_openings = StoreOpening.objects.filter(store=store)
    return render(request, 'provider/store_openings/list.html', {'store_openings': store_openings, 'store': store})

@login_required(login_url='provider-login')
def store_opening_create(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    if request.method == 'POST':
        form = StoreOpeningForm(request.POST)
        if form.is_valid():
            store_opening = form.save(commit=False)
            store_opening.store = store
            store_opening.save()
            return redirect('store_opening_list')
    else:
        form = StoreOpeningForm()
    return render(request, 'provider/store_openings/create.html', {'form': form, 'store': store})

@login_required(login_url='provider-login')
def store_opening_edit(request, opening_id):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    store_opening = get_object_or_404(StoreOpening, id=opening_id, store=store)
    if request.method == 'POST':
        form = StoreOpeningForm(request.POST, instance=store_opening)
        if form.is_valid():
            form.save()
            return redirect('store_opening_list')
    else:
        form = StoreOpeningForm(instance=store_opening)
    return render(request, 'provider/store_openings/update.html', {'form': form, 'store': store, 'store_opening': store_opening})

@login_required(login_url='provider-login')
def store_opening_delete(request, opening_id):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    store_opening = get_object_or_404(StoreOpening, id=opening_id, store=store)
    store_opening.delete()
    return redirect('store_opening_list')