from django import forms
from provider_details.models import StoreOpening, Store

class StoreOpeningForm(forms.ModelForm):
    class Meta:
        model = StoreOpening
        fields = ( 'day', 'time_start', 'time_end')
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
        }