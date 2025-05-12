from django.urls import path

from orders.views import order_create, order_payment, order_success, order_items_partial

urlpatterns = [
    path("create/", order_create, name="order_create"),
    path("payment/", order_payment, name="order_payment"),
    path("success/", order_success, name="order_success"),
    path("order-items-partial/", order_items_partial, name="order_items_partial"),
]
