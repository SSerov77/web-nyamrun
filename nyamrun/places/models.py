from django.db import models


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
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(
        upload_to='place_images/',
        verbose_name='Изображение',
    )
    categories = models.ManyToManyField(
        'Category',
        related_name='places',
        verbose_name='Категории товаров'
    )
    working_hours = models.CharField(
        max_length=255, verbose_name='Время работы')

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'

    def __str__(self):
        return self.name


class Address(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Заведение'
    )
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

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house_number}'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    place = models.ForeignKey(
        Place,
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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} — {self.place.name}'


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

    class Meta:
        verbose_name = 'Опция товара'
        verbose_name_plural = 'Опции товаров'

    def __str__(self):
        return f'{self.name} (+{self.additional_price}₽) для {self.product.name}'
