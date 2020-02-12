from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Vue app migrate
    path('', TemplateView.as_view(template_name="index.html"), name='app'),

    # shopping app urls
    path('shopping/', include('shopping.urls')),
]
