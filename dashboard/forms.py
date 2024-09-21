from django import forms
from auth_login.models import *
from  provider_details.models import *
from .models import Config


class ConfigForm(forms.ModelForm):
     class Meta:
        model = Config
        fields = '__all__'
        widgets = { 
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProviderSubscriptionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='تاريخ الإشتراك'
    )

    class Meta:
        model = ProviderSubscription
        fields = '__all__'
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'duration_days': forms.Select(attrs={'class': 'form-control'}),
            'service_profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'store_subscription': forms.CheckboxInput(attrs={'class': 'form-check-inline'}),
            'product_profit': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date':'تاريخ الإشتراك',  # Translated label for the "date" field
            'provider': "المزود",  # Translated label for the "provider" field
            'duration_days':"المدة (بالأيام)",  # Translated label for the "duration_days" field
            'service_profit': "الربح من الخدمات",  # Translated label for the "service_profit" field
            'store_subscription': "Products Subscription",  # Translated label for the "store_subscription" field
            'product_profit': "الربح من المنتجات",  # Translated label for the "product_profit" field
        }


class PromotionSubscriptionForm(forms.ModelForm):
    promotion_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='تاريخ الإشتراك'
    )

    class Meta:
        model = PromotionSubscription
        fields = '__all__'
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'promotion_date': forms.Select(attrs={'class': 'form-control'}),
            'promotion_duration_days': forms.Select(attrs={'class': 'form-control'}),
            'profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'input','type':'file' ,'accept': 'image/*'}),
        }
        labels = {
            'promotion_date': 'تاريخ الإشتراك',
            'provider': 'المزود',
            'promotion_duration_days': 'المدة (بالأيام)',
            'profit': ' المبلغ المستحق',
            'image': 'رفع الصورة',
        }

class CustomerForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
    )

    class Meta:
        model = Customer
        fields = ['name', 'username' ,'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AddCustomerForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
    )

    class Meta:
        model = Customer
        fields = ['name', 'username','password' ,'email', 'phone', 'address']
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProviderForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
        label='اسم المستخدم',  # Arabic label for username field
    )

    class Meta:
        model = Provider
        fields = ['name', 'username', 'category', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'الاسم',  # Arabic label for name field
            'category': 'الفئة',  # Arabic label for category field
            'email': 'البريد الإلكتروني',  # Arabic label for email field
            'phone': 'رقم الهاتف',  # Arabic label for phone field
            'address': 'العنوان',  # Arabic label for address field
        }


class AddProviderForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
        label='اسم المستخدم',  # Arabic label for username field
    )

    class Meta:
        model = Provider
        fields = ['name', 'username', 'password', 'category', 'email', 'phone', 'address']
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'الاسم',  # Arabic label for name field
            'category': 'الفئة',  # Arabic label for category field
            'email': 'البريد الإلكتروني',  # Arabic label for email field
            'phone': 'رقم الهاتف',  # Arabic label for phone field
            'address': 'العنوان',  # Arabic label for address field
        }
    
class AdminForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
    )

    class Meta:
        model = AdminUser
        fields = ['name', 'username' ,'email', 'phone',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AddAdminForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=None,  # Remove the help text explicitly
    )

    class Meta:
        model = AdminUser
        fields = ['name', 'username','password' ,'email', 'phone',]
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

###########Store#######

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['provider', 'image','en_name',  'name', 'about']
        labels = {
            'provider': 'المزود',
            'image': 'حمل صورة',
            'name': 'الإسم التجاري',
            'about': 'وصف',
        }
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'input','type':'file' ,'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        
        
###########Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['main_service', 'image', 'name','en_name','description', 'price', 'offers', 'duration']
        labels = {
            'main_service': 'الخدمة الرئيسية',
            'image': 'رفع الصورة',
            'name': 'اسم الخدمة',
            'description': 'الوصف',
            'price': 'السعر',
            'offers': 'الخصم',
            'duration': 'مدة الخدمة (بالدقائق)',
        }
        widgets = {
            'main_service': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offers': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','en_name','name', 'description', 'price','quantity','offers')
        labels = {
            'image': 'رفع الصورة',
            'name': 'اسم المنتج',
            'description': 'الوصف',
            'price': 'السعر',
            'offers': 'الخصم',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'offers': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class StoreGalleryForm(forms.ModelForm):
    class Meta:
        model = StoreGallery
        fields = ('image',)
        labels = {
            'image': 'رفع الصورة'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }
        
        
class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('customer', 'message', 'rating')
        labels = {
            'customer': 'الزبون',
            'message': 'رسالة',
            'rating': 'تقييم المنتج',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StoreAdminServicesForm(forms.ModelForm):
    class Meta:
        model = StoreAdminServices
        fields = ('main_service',)
        labels = {
            'main_service': 'الخدمة الرئيسية',
        }
        widgets = {
            'main_service': forms.Select(attrs={'class': 'form-control'}),
        }