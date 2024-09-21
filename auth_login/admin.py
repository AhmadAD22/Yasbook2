from django.contrib import admin

from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Provider, AdminUser
from django.urls import reverse
from django.utils.html import format_html
from provider_details.models import Store


admin.site.register(MyUser)


admin.site.register(Customer)


admin.site.register(Provider)


class AdminUserAdmin(UserAdmin):
    list_display = ('name', 'phone', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('name', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Contact Information', {'fields': ('name','phone','email')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(AdminUser, AdminUserAdmin)

from django.contrib import admin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

class ProviderSubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('details',)

    def details(self, obj):
        return format_html('<a href="http://127.0.0.1:8000/">Clic to show more details</a>') 
    details.short_description = 'Details'

admin.site.register(ProviderSubscription, ProviderSubscriptionAdmin)
admin.site.register(PromotionSubscription)
admin.site.register(OTPRequest)
admin.site.register(PendingClient)
admin.site.register(PendingProvider)


