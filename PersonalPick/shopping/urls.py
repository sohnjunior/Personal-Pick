from django.urls import path

from . import views

app_name = 'shopping'
urlpatterns = [
    # /shopping/query
    path('query/', views.ProductQuery.as_view(), name='product_query'),

    # /shopping/cart
    path('cart/', views.ProductCart.as_view(), name='product_cart'),
]
