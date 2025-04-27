from django.db import models
from django.conf import settings

from places.models import Product, ProductOption


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


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
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    options = models.ManyToManyField(
        ProductOption,
        blank=True,
        verbose_name='Опции'
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        # Убираем unique_together и UniqueConstraint, т.к. они не учитывают опции

    def __str__(self):
        opts = ", ".join(opt.name for opt in self.options.all())
        if opts:
            return f'{self.product.name} ({opts}) x {self.quantity}'
        return f'{self.product.name} x {self.quantity}'

    def get_options_price(self):
        return sum(option.additional_price for option in self.options.all())

    def get_price(self):
        return self.product.price + self.get_options_price()

    def get_total_price(self):
        return self.get_price() * self.quantity