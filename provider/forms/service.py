from provider_details.models import Service, StoreSpecialist, Store
from django import forms
class ServiceForm(forms.ModelForm):
    specialists = forms.ModelMultipleChoiceField(
        queryset=StoreSpecialist.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='المتخصصون',
        required=False
    )

    class Meta:
        model = Service
        fields = ('image', 'name','en_name', 'description', 'price', 'offers', 'duration', 'main_service', 'specialists')
        labels = {
            'image': 'رفع الصورة',
            'name': 'اسم الخدمة',
            'description': 'الوصف',
            'price': 'السعر',
            'offers': 'الخصم',
            'duration': 'مدة الخدمة (بالدقائق)',
            'main_service': 'الخدمة الرئيسية',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offers': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_service': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, store, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialists'].queryset = StoreSpecialist.objects.filter(store=store)
        
    # def save(self, store, commit=True):
    #     service = super().save(commit=False)
    #     service.store = store
    #     service.save()
    #     service.specialists.set(self.cleaned_data['specialists'])
    #     return service
        