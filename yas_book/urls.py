
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    # path('', include('admin_material.urls')),
    path('admin/', admin.site.urls),
    # path("", redirect_to_admin, name="to_admin"),
    path('user/',include('auth_login.urls')),
    path('',include('website.urls')),
    path('category/',include('categroy.urls')),
    path('store/',include('provider_details.urls')),
    path('client/',include('client.urls')),
    path('provider/',include('provider.urls')),
    path('order/',include('order_cart.urls')),
    path('dashboard/',include('dashboard.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
