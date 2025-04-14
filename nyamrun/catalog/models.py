from django.db import models

class Place(models.Model):
    PLACE_TYPES = [
        ('cafe', 'Кафе'),
        ('bakery', 'Пекарня'),
        ('coffee_shop', 'Кофейня'),
    ]

    type = models.CharField(max_length=20, choices=PLACE_TYPES)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='place_images/')
    categories = models.ManyToManyField('Category', related_name='places')
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.name} — {self.place.name}'


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name} (+{self.additional_price}₽) для {self.product.name}'