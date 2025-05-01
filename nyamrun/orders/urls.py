from django.urls import path
from .views import order_create

urlpatterns = [
    path('create/', order_create, name='order_create'),
    # path('success/<int:pk>/', order_success, name='order_success'), # сам реализуй, как захочешь
]