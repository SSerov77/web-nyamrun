# Generated by Django 5.2 on 2025-04-27 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cartitem',
            name='unique_product_in_cart',
        ),
    ]
