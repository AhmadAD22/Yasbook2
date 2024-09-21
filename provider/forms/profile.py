
from auth_login.models import Provider,PendingProvider
from django import forms

class AddProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'category', 'email','address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'الاسم',  # Arabic label for name field
            'category': 'الفئة',  # Arabic label for category field
            'email': 'البريد الإلكتروني',  # Arabic label for email field
            'address': 'العنوان',  # Arabic label for address field
        }
        


class PendingProviderForm(forms.ModelForm):
    class Meta:
        model = PendingProvider
        fields = ['fullName', 'phone', 'email', 'category']
        widgets = {
            'fullName': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'fullName': 'الاسم الكامل',
            'phone': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'category': 'الفئة',
        }