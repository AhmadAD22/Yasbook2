from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ProductOrder)
admin.site.register(ServiceOrder)
admin.site.register(Cart)
admin.site.register(ServiceCartItem)
admin.site.register(CartItem)