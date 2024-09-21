from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Category, MainService
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'created_at', 'updated_on')
    search_fields = ('name',)
    readonly_fields = ('display_image','display_image_field','created_at', 'updated_on')
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'display_image_field')
        }),
        ('تواريخ', {
            'fields': ('created_at', 'updated_on'),
            'classes': ('collapse',),
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50">',obj.image.url)
        return None

    display_image.short_description = 'صورة التصنيف'

    def display_image_field(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="450" height="350">')
        return None

    display_image_field.short_description = 'صورة الخدمة'
admin.site.register(Category, CategoryAdmin)


class MainServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_image', 'created_at', 'updated_on')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    readonly_fields = ('display_image','display_image_field','created_at', 'updated_on')
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'image', 'display_image_field'),
        }),

        ('تواريخ', {
            'fields': ('created_at', 'updated_on'),
            'classes': ('collapse',),
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50">')
        return None

    display_image.short_description = 'صورة الخدمة'

    def display_image_field(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="450" height="350">')
        return None

    display_image_field.short_description = 'صورة الخدمة'

admin.site.register(MainService, MainServiceAdmin)