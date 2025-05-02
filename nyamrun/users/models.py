from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Логин'
    )
    name = models.CharField(max_length=30, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='Почта')

    def __str__(self):
        return self.username