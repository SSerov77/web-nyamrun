from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'display_options',
              'get_price', 'get_total_price')
    readonly_fields = ('display_options', 'get_price', 'get_total_price')

    def display_options(self, obj):
        return ', '.join([opt.name for opt in obj.options.all()])
    display_options.short_description = 'Опции'

    def get_price(self, obj):
        return obj.get_price()
    get_price.short_description = 'Цена за единицу (с учётом опций)'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'created_at', 'total_price')
    search_fields = ('user__username', 'user__email')
    list_filter = ('place',)
    inlines = [CartItemInline]

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Итого'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity',
                    'display_options', 'get_price', 'get_total_price')
    search_fields = (
        'cart__user__username',
        'cart__user__email',
        'product__name',
    )
    list_filter = ['product']

    def display_options(self, obj):
        return ', '.join([opt.name for opt in obj.options.all()])
    display_options.short_description = 'Опции'

    def get_price(self, obj):
        return obj.get_price()
    get_price.short_description = 'Цена за 1 (с учётом опций)'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Всего'
