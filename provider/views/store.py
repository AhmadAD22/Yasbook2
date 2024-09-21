
from provider_details.models import Store
from ..forms.store import StoreForm
from django.shortcuts import render, redirect


def store_update_view(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=request.user.provider.store)
        if form.is_valid():
            form.save()
            return redirect('store_update-settings')
    else:
        form = StoreForm(instance=request.user.provider.store)

    context = {
        'form': form,
    }
    return render(request, 'provider/store/settings.html', context)

