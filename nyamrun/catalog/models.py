from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    place = models.ForeignKey(
        'places.Place',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Заведение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='product_images/', verbose_name='Изображение')
    
    def __str__(self):
        return f'{self.name} — {self.place.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductOption(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Товар'
    )
    name = models.CharField(max_length=100, verbose_name='Название опции')
    additional_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name='Доплата'
    )

    def __str__(self):
        return f'{self.name} (+{self.additional_price}₽) для {self.product.name}'

    class Meta:
        verbose_name = 'Опция товара'
        verbose_name_plural = 'Опции товаров'
