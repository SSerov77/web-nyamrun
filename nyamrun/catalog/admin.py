from django.contrib import admin

from catalog.models import Category, Product, ProductOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'category', 'price')
    search_fields = ('name', 'place__name', 'category__name')
    list_filter = ('place', 'category')
    list_per_page = 10


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'additional_price')
    search_fields = ('name', 'product__name')
    list_filter = ('product',)
    list_per_page = 10