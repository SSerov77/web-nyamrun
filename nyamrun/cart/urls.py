from django.urls import path

from cart import views

urlpatterns = [
    path('cart/add-ajax/<int:product_id>/', views.cart_add_ajax, name='cart_add_ajax'),
    path('cart/sidebar/', views.cart_detail_ajax, name='cart_sidebar_ajax'),
    path('cart/clear-ajax/', views.cart_clear_ajax, name='cart_clear_ajax'),
]