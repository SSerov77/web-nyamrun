from django.urls import path
from places import views

urlpatterns = [
    path('', views.places_list, name='places'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
]
