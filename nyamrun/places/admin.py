from django.contrib import admin

from places.models import Place, Address
from places.forms import PlaceAdminForm


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ['country', 'city', 'street', 'house_number']
    verbose_name = 'Адрес'
    verbose_name_plural = 'Адреса'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ('name', 'type', 'get_categories')
    list_filter = ('type', 'categories')
    search_fields = ('name',)
    inlines = [AddressInline]
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = "Категории"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('place', 'country', 'city', 'street', 'house_number')
    search_fields = ('place__name', 'city', 'street', 'house_number')
    list_filter = ('country', 'city')
    list_per_page = 10
