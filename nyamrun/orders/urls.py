from django.urls import path

from orders.views import order_create, order_payment, order_success

urlpatterns = [
    path("create/", order_create, name="order_create"),
    path("payment/", order_payment, name="order_payment"),
    path("success/", order_success, name="order_success"),
]
