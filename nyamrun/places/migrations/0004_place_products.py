# Generated by Django 5.2 on 2025-04-27 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_remove_product_place'),
        ('places', '0003_remove_product_category_remove_product_place_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='products',
            field=models.ManyToManyField(blank=True, to='catalog.product', verbose_name='Товары'),
        ),
    ]
