from django.contrib import admin
from .models import *
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from auth_login.models import Provider

class StoreAdminServicesInline(admin.TabularInline):
    model = StoreAdminServices
    extra = 1
    readonly_fields = ('main_service_category',)  # Add a readonly field for the category

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if isinstance(self.parent_model.objects.first(), Store):
            store_id = self.parent_model.objects.first().id
            store = Store.objects.get(id=store_id)
            category = store.provider.category
            kwargs['queryset'] = MainService.objects.filter(category=category)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def main_service_category(self, instance):
        return instance.main_service.category.name  # Return the category name for the main service

    main_service_category.short_description = 'Category'  # Set the column header name for the category


class StoreSpecialistInline(admin.TabularInline):
    model = StoreSpecialist
    extra = 0
    readonly_fields = ('name', 'created_at', 'updated_on')
    can_add_related = False
    def has_delete_permission(self, request, obj=None):
        return False
    
class StoreOpeningInline(admin.TabularInline):
    model = StoreOpening
    extra = 0
    readonly_fields = ('day', 'time_start', 'time_end', 'created_at', 'updated_on')
    can_add_related = False
    def has_delete_permission(self, request, obj=None):
        return False
    
class FollowingStoreInline(admin.TabularInline):
    model = FollowingStore
    extra = 0
    readonly_fields = ('store', 'customer')
    can_add_related = False
    def has_delete_permission(self, request, obj=None):
        return False
    
class StoreStoryInline(admin.TabularInline):
    model = StoreStory
    extra = 0
    readonly_fields = ('store', 'image')
    can_add_related = False
    def has_delete_permission(self, request, obj=None):
        return False
    
class StoreGalleryInline(admin.TabularInline):
    model = StoreGallery
    extra = 0
    fields = ('image_display',)
    readonly_fields = ('store', 'image_display', 'created_at', 'updated_on')
    def has_delete_permission(self, request, obj=None):
        return False
    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "N/A"
    image_display.short_description = 'Image'
    
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_link', 'image_display', 'created_at', 'updated_on')
    list_filter = ('created_at', 'updated_on')
    search_fields = ('name', 'provider__name')  # Search by store name or provider name
    inlines = [
        StoreAdminServicesInline,
        StoreSpecialistInline,
        StoreOpeningInline,
        FollowingStoreInline,
        StoreStoryInline,
        StoreGalleryInline,
    ]

    fieldsets = (
        (None, {'fields': ('provider_link',)}),
        ('Store Information', {'fields': ('name', 'about', 'image_display_field')}),
        ('Timestamps', {'fields': ('created_at', 'updated_on')}),
    )
    readonly_fields = ('provider_link', 'image_display','image_display_field','created_at', 'updated_on')

    def provider_link(self, obj):
        provider_url = reverse('admin:auth_login_provider_change', args=[obj.provider.id])
        return format_html('<a href="{}">{}</a>', provider_url, obj.provider.name)
    provider_link.short_description = 'Provider'

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "N/A"
    image_display.short_description = 'Image'

    def image_display_field(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="450" height="450" />', obj.image.url)
        return "N/A"
    image_display_field.short_description = 'Store Image'

admin.site.register(Store, StoreAdmin)



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'image_display', 'price', 'offers']
    list_filter = ['store']
    search_fields = ['name', 'store__name']
    readonly_fields = ('image_display', 'created_at', 'updated_on')

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "N/A"

    image_display.short_description = 'Image'

    fieldsets = (
        ('Product Information', {
            'fields': ('store', 'name', 'description', 'price', 'offers','quantity')
        }),
        ('Image and Dates', {
            'fields': ('image_display', 'created_at', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Product, ProductAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['customer', 'store', 'message', 'rating', 'created_at']
    list_filter = ['store']
    search_fields = ['customer__username', 'store__name', 'message']
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Review Information', {
            'fields': ('customer', 'store', 'message', 'rating')
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Reviews, ReviewsAdmin)



class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'main_service', 'image_display', 'price', 'offers']
    list_filter = ['store', 'main_service']
    search_fields = ['name', 'store__name', 'main_service__name']
    readonly_fields = ('image_display', 'created_at', 'updated_on')

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "N/A"

    image_display.short_description = 'Image'

    fieldsets = (
        ('Service Information', {
            'fields': ('store', 'main_service', 'name','specialists', 'description', 'price', 'offers', 'duration')
        }),
        ('Image and Dates', {
            'fields': ( 'created_at', 'updated_on','image_display'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Service, ServiceAdmin)
admin.site.register(StoreSpecialist)
admin.site.register(StoreOpening)
# admin.site.register(SpecialistWorks)
admin.site.register(StoreGallery)
admin.site.register(StoreAdminServices)
admin.site.register(FollowingStore)
admin.site.register(Coupon)
admin.site.register(CommonQuestion)




# admin.site.register(StoreGalleryInline)


