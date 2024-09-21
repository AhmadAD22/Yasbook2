from django import forms
from provider_details.models import Store

class StoreForm(forms.ModelForm):
    whatsapp_link = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Store
        fields = ['image','en_name','name', 'about', 'whatsapp_link']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'image': 'رفع الصورة',
            'name': ' الإسم التجاري',
            'about': 'الوصف',
            'whatsapp_link': 'رابط الواتساب',
        }
        