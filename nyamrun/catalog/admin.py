from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget

from catalog.models import Category, Product, ProductOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    search_fields = ("name", "slug",)
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "category", "price")
    search_fields = ("name", "place__name", "category__name")
    list_filter = ("place", "category")
    filter_horizontal = ("options",)
    list_per_page = 10
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            object_id = request.resolver_match.kwargs.get('object_id')
            if object_id:
                # редактирование существующего Product
                product = Product.objects.get(pk=object_id)
                # берем только категории, связанные с этим Place
                kwargs["queryset"] = product.place.categories.all()
            else:
                # создание нового — не показываем ни одной категории
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "additional_price", "get_products")
    search_fields = ("name", "products__name")
    list_per_page = 10

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    get_products.short_description = "Товары"
