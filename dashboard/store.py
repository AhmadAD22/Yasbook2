from django.shortcuts import render, redirect, get_object_or_404
from provider_details.models import Store
from .forms import StoreForm
from django.contrib.admin.views.decorators import staff_member_required


######Customer###########################
@staff_member_required(login_url='login')
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'store/store_list.html', {'stores': stores})

@staff_member_required(login_url='login')
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save()
            return redirect('store_list')
    else:
        form = StoreForm()
    
    return render(request, 'store/store_create.html', {'form': form})

@staff_member_required(login_url='login')
def store_update(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store_list')
    else:
        form = StoreForm(instance=store)
    
    return render(request, 'store/store_update.html', {'form': form, 'store': store})

@staff_member_required(login_url='login')
def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    store.delete()
    return redirect('store_list')
    