# Generated by Django 5.2 on 2025-05-01 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_place'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина пользователя', 'verbose_name_plural': 'Корзины пользователей'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Элемент корзины пользователя', 'verbose_name_plural': 'Элементы корзины пользователей'},
        ),
    ]
