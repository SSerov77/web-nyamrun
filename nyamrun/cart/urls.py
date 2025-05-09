from django.urls import path

from cart import views

urlpatterns = [
    path("add-ajax/<int:product_id>/", views.cart_add_ajax, name="cart_add_ajax"),
    path("sidebar/", views.cart_detail_ajax, name="cart_sidebar_ajax"),
    path("clear-ajax/", views.cart_clear_ajax, name="cart_clear_ajax"),
    path("remove-ajax/<int:item_id>/", views.cart_remove_ajax, name="cart_remove_ajax"),
    path("update-ajax/<int:item_id>/", views.cart_update_ajax, name="cart_update_ajax"),
]
