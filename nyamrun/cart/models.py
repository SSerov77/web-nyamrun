from django.db import models
from django.conf import settings

from catalog.models import Product, ProductOption
from places.models import Place


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(
        Place,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Корзина пользователя ID {self.user_id}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    options = models.ManyToManyField(
        ProductOption,
        blank=True,
        verbose_name='Опции'
    )

    def __str__(self):
        return f'Товар {self.product_id} x {self.quantity}'

    def get_options_price(self):
        return sum(option.additional_price for option in self.options.all())

    def get_price(self):
        return self.product.price + self.get_options_price()

    def get_total_price(self):
        return self.get_price() * self.quantity

    class Meta:
        verbose_name = 'Элемент корзины пользователя'
        verbose_name_plural = 'Элементы корзины пользователей'