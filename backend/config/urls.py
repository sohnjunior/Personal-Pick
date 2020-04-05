from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),

    # shopping app urls
    path('shopping/', include('shopping.urls')),

    # django-allauth
    path('accounts/', include('allauth.urls')),

    # django-rest-auth
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
