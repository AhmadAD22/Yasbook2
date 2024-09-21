from django.shortcuts import render, redirect
from ..forms.profile import AddProviderForm
from auth_login.models import Provider

def provider_profile(request):
    provider = Provider.objects.get(pk=request.user.pk)
    return render(request, 'provider/profile/profile.html', {'provider': provider})

def provider_update(request):
    provider = Provider.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = AddProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('provider_profile')
    else:
        form = AddProviderForm(instance=provider)
    return render(request, 'provider/profile/update_profile.html', {'form': form})