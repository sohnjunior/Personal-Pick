from django.contrib import admin
from .models import Category, Product


class ProductInline(admin.StackedInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductInline, ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'mallName', 'category')
    search_fields = ('title', 'mallName')
    list_filter = ('category',)
