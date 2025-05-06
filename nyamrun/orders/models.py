from django.db import models
from django.conf import settings

from catalog.models import Product, ProductOption
from places.models import Place, Address


class OrderStatus(models.TextChoices):
    CREATED = 'created', 'Создан'
    READY = 'ready', 'Готов к выдаче'
    ISSUED = 'issued', 'Выдан'
    CANCELED = 'canceled', 'Отменен'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        verbose_name='Заведение'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name='Адрес'
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    ready_time = models.TimeField(verbose_name="Время приготовления")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая цена'
    )
    payment_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Номер чека'
    )

    def __str__(self):
        return f'Заказ #{self.pk}'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    options = models.ManyToManyField(
        ProductOption,
        blank=True,
        verbose_name='Опции'
    )

    @property
    def price(self):
        base = self.product.price
        opts = sum(opt.additional_price for opt in self.options.all())
        return base + opts

    @property
    def total_price(self):
        return self.price * self.quantity
    
    class Meta:
        verbose_name = 'Элементы заказа'
        verbose_name_plural = 'Элементы заказов'
