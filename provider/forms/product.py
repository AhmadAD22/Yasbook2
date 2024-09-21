from provider_details.models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image', 'name','en_name','quantity','description', 'price', 'offers')
        labels = {
            'image': 'رفع الصورة',
            'name': 'اسم المنتج',
            'en_name':'اسم المنتج بالإنكليزية',
            'description': 'الوصف',
            'price': 'السعر',
            'offers': 'الخصم',
            'quantity': 'الكمية',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offers': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
 