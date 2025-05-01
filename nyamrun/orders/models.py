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
        related_name='orders'
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
    created_at = models.DateTimeField(auto_now_add=True)
    ready_time = models.TimeField(verbose_name="Время приготовления")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order #{self.pk} for {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    options = models.ManyToManyField(ProductOption, blank=True)

    def get_price(self):
        base = self.product.price
        opts = sum(opt.additional_price for opt in self.options.all())
        return base + opts

    def get_total_price(self):
        return self.get_price() * self.quantity
