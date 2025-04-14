from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.restaurants_list, name='restaurants'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
]
