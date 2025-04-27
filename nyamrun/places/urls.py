from django.urls import path

from places import views


urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
    path('products/<int:product_id>/modal_data/', views.product_modal_data, name='product_modal_data'),
]
