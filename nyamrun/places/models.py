from django.db import models
from django.conf import settings


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
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_address',
        verbose_name='Менеджер'
    )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house_number}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class PlaceType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название типа'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Код типа'
    )
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип заведения'
        verbose_name_plural = 'Типы заведений'



class Place(models.Model):
    type = models.ForeignKey(
        PlaceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    addresses = models.ManyToManyField(
        Address,
        blank=True,
        related_name='places',
        verbose_name='Адреса'
    )
    owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='places',
        verbose_name='Владелец',
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
