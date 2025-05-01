from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        'product',
        'quantity',
        'get_options',
        'get_total_price'
    )
    readonly_fields = ('product', 'quantity', 'get_options', 'get_total_price')

    def get_options(self, obj):
        return ", ".join([opt.name for opt in obj.options.all()])
    get_options.short_description = "Опции"

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Сумма по позиции, ₽"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'place',
        'address',
        'status',
        'created_at',
        'ready_time',
        'total_price'
    )
    list_filter = ('place', 'status', 'created_at')
    search_fields = (
        'user__username',
        'place__name',
        'address__city',
        'address__street'
    )
    inlines = [OrderItemInline]
    readonly_fields = (
        'user',
        'place',
        'address',
        'created_at',
        'total_price'
    )

    def view_items(self, obj):
        return " | ".join(f"{item.product.name} x{item.quantity}" for item in obj.items.all())
    view_items.short_description = "Позиции заказа"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'show_options',
        'get_total_price'
    )
    search_fields = ('product__name',)
    list_filter = ('product__place',)

    def show_options(self, obj):
        return ", ".join([opt.name for opt in obj.options.all()])
    show_options.short_description = "Опции"

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Итого, ₽"
