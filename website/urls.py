from django.urls import path
from .views import *
urlpatterns = [
path('',home,name="website.home"),
path('yasbook/',yasbook_page,name="website.yasbook"),
path('about/',about,name="website.about"),
path('contact/',contact,name="website.contact"),
path('terms_of_use/',terms,name="website.terms_of_use"),
path('privacy_policy/',privacy,name="website.privacy_policy"),
 path('send/', SubmitFormView.as_view(), name='send'),
]