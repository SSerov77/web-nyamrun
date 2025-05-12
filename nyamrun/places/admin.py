from django.contrib import admin

from places.forms import PlaceAdminForm
from places.models import Address, Place, PlaceType


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    fields = (
        "name",
        "type",
        "image",
        "working_hours",
        "categories",
        "addresses",
        "owner",
    )
    list_display = ("name", "get_place_type", "get_categories", "owner")
    list_filter = ("type", "categories")
    search_fields = ("name", "owner__username", "owner__email")
    filter_horizontal = ("categories", "addresses")

    def get_categories(self, obj):
        return ", ".join(cat.name for cat in obj.categories.all())

    get_categories.short_description = "Категории"

    def get_place_type(self, obj):
        return obj.type.name if obj.type else "-"

    get_place_type.short_description = "Тип заведения"

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = "Число товаров"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "get_places",
        "country",
        "city",
        "street",
        "house_number",
        "manager",
    )
    search_fields = ("city", "street", "house_number")
    list_filter = ("country", "city")
    list_per_page = 10
    raw_id_fields = ("manager",)

    def get_places(self, obj):
        return ", ".join([place.name for place in obj.places.all()])

    get_places.short_description = "Заведения"


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
