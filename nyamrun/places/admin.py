from django.contrib import admin

from places.models import Place, Address
from places.forms import PlaceAdminForm

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    fields = (
        'name',
        'type',
        'image',
        'working_hours',
        'categories',
        'addresses',
    )
    list_display = ('name', 'type', 'get_categories',)
    list_filter = ('type', 'categories')
    search_fields = ('name',)
    filter_horizontal = ('categories', 'addresses')

    def get_categories(self, obj):
        return ", ".join(cat.name for cat in obj.categories.all())
    get_categories.short_description = "Категории"

    # Если очень нужно видеть продукты заведения, можно добавить метод:
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = "Число товаров"

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('get_places', 'country', 'city', 'street', 'house_number')
    search_fields = ('city', 'street', 'house_number')
    list_filter = ('country', 'city')
    list_per_page = 10

    def get_places(self, obj):
        return ", ".join([place.name for place in obj.places.all()])
    get_places.short_description = 'Заведения'