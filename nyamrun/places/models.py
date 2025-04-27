from django.db import models


class Address(models.Model):
    country = models.CharField(
        max_length=255,
        default='Россия',
        verbose_name='Страна'
    )
    city = models.CharField(
        max_length=255,
        default='Не указан',
        verbose_name='Город'
    )
    street = models.CharField(
        max_length=255, 
        default='Не указан', 
        verbose_name='Улица'
    )
    house_number = models.CharField(
        max_length=50,
        default='Не указан', 
        verbose_name='Дом'
    )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house_number}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class PlaceType(models.TextChoices):
    CAFE = 'cafe', 'Кафе'
    BAKERY = 'bakery', 'Пекарня'
    COFFEE_SHOP = 'coffee_shop', 'Кофейня'


class Place(models.Model):
    type = models.CharField(
        max_length=20,
        choices=PlaceType.choices,
        default=PlaceType.CAFE,
        verbose_name='Тип заведения'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='place_images/',
        verbose_name='Изображение',
    )
    categories = models.ManyToManyField(
        'catalog.Category',
        related_name='places',
        verbose_name='Категории товаров'
    )
    working_hours = models.CharField(
        max_length=255,
        verbose_name='Время работы'
    )
    products = models.ManyToManyField(
        'catalog.Product',
        verbose_name='Товары', 
        blank=True
    )
    addresses = models.ManyToManyField(
        Address,
        blank=True,
        related_name='places',
        verbose_name='Адреса'
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
