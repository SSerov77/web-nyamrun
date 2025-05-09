from django.contrib import admin

from catalog.models import Category, Product, ProductOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "category", "price")
    search_fields = ("name", "place__name", "category__name")
    list_filter = ("place", "category")
    filter_horizontal = ("options",)
    list_per_page = 10


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "additional_price", "get_products")
    search_fields = ("name", "products__name")
    list_per_page = 10

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    get_products.short_description = "Товары"
