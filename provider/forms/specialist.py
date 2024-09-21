from provider_details.models import Service, StoreSpecialist, Store
from django import forms

from django import forms

class StoreSpecialistForm(forms.ModelForm):
    
    class Meta:
        model = StoreSpecialist
        fields = ( 'name', 'phone', 'image')
        labels = {
            'name': 'اسم الموظف',
            'phone': 'رقم الهاتف',
            'image': 'رفع الصورة',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }