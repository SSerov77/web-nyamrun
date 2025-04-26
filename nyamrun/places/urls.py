from django.urls import path

from places import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
]
