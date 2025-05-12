from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from catalog.models import Product, ProductOption
from places.models import Address, Place


class OrderStatus(models.TextChoices):
    CREATED = "created", "Создан"
    READY = "ready", "Готов к выдаче"
    ISSUED = "issued", "Выдан"
    CANCELED = "canceled", "Отменен"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="Заведение")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Адрес")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    ready_time = models.TimeField(verbose_name="Время приготовления")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая цена",
        validators=[MinValueValidator(0)],
    )
    payment_id = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Номер чека"
    )

    def __str__(self):
        return f"Заказ #{self.pk}"

    def update_total_price(self):
        """
        Пересчитывает и сохраняет итоговую сумму заказа,
        пробегаясь по всем связанным OrderItem'ам.
        """
        # Суммируем total_price у всех элементов
        total = sum((item.total_price for item in self.items.all()), Decimal("0"))
        # Сохраняем
        self.total_price = total
        # Обновляем только поле total_price, чтобы не трогать остальные
        self.save(update_fields=["total_price"])

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(
        verbose_name="Количество", validators=[MinValueValidator(1)]
    )
    options = models.ManyToManyField(ProductOption, blank=True, verbose_name="Опции")

    def clean(self):
        if self.product.place != self.order.place:
            raise ValidationError(
                {"product": "Товар должен принадлежать выбранному заведению"}
            )

    @property
    def price(self):
        """Get price for single item with options"""
        base = self.product.price
        opts = sum(opt.additional_price for opt in self.options.all())
        return base + opts

    @property
    def total_price(self):
        """Get total price for all items"""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_price()

    class Meta:
        verbose_name = "Элементы заказа"
        verbose_name_plural = "Элементы заказов"
