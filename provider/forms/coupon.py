from django import forms
from provider_details.models import Coupon, Provider
from django.utils import timezone

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('name', 'code', 'value', 'expired')
        labels = {
            'name': 'Coupon Name',
            'code': 'Coupon Code',
            'value': 'Discount Value (%)',
            'expired': 'Expiration Date',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'expired': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
