import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from yookassa import Configuration, Payment
from django.template.loader import render_to_string
from django.http import JsonResponse

from cart.models import Cart
from orders.forms import OrderForm
from orders.helper import get_time_choices
from orders.models import Order, OrderItem
from places.models import Address


@login_required
def order_create(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product").prefetch_related("options")
    place = cart.place
    time_choices = get_time_choices(place=place)

    total_price = cart.get_total_price()

    if request.method == "POST":
        form = OrderForm(request.POST, place=place, time_choices=time_choices)

        if form.is_valid():
            request.session["order_data"] = {
                "address": form.cleaned_data["address"].pk,
                "ready_time": form.cleaned_data["time"],
                "comment": form.cleaned_data["comment"],
                "total_price": f"{total_price:.2f}",
            }
            return redirect("order_payment")
    else:
        form = OrderForm(place=place, time_choices=time_choices)

    return render(
        request,
        "orders/order_create.html",
        {
            "form": form,
            "cart": cart,
            "items": items,
            "total_price": total_price,
        },
    )


@login_required
def order_payment(request):
    user = request.user
    order_data = request.session.get("order_data")
    if not order_data:
        return redirect("order_create")

    cart = user.cart
    total_price = cart.get_total_price()

    receipt_items = []
    for item in cart.items.select_related("product").prefetch_related("options"):
        desc = item.product.name
        if item.options.exists():
            desc += " (" + ", ".join([opt.name for opt in item.options.all()]) + ")"
        receipt_items.append(
            {
                "description": desc,
                "quantity": item.quantity,
                "amount": {
                    "value": str(item.product.price),
                    "currency": "RUB",
                },
                "vat_code": 4,
            }
        )

    customer_email = user.email
    if not customer_email:
        return render(
            request,
            "orders/payment_failed.html",
            {
                "error": (
                    "У пользователя не указан email. "
                    "Без email фискальный чек невозможен."
                )
            },
        )

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    payment = Payment.create(
        {
            "amount": {"value": str(total_price), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri(reverse("order_success")),
            },
            "capture": True,
            "description": f"Оплата заказа от {user.username}",
            "metadata": {"user_id": user.id, "order_data": json.dumps(order_data)},
            "receipt": {
                "customer": {
                    "email": customer_email,
                    "full_name": user.get_full_name() or user.username,
                },
                "items": receipt_items,
            },
        }
    )
    request.session["payment_id"] = payment.id
    return redirect(payment.confirmation.confirmation_url)


@login_required
def order_success(request):
    payment_id = request.session.get("payment_id")
    order_data = request.session.get("order_data")

    user = request.user
    cart = user.cart

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    payment = Payment.find_one(payment_id)

    if payment.status == "succeeded":
        existing = Order.objects.filter(payment_id=payment_id).first()
        if existing:
            return render(request, "orders/order_success.html", {"order": existing})

        order = Order.objects.create(
            user=user,
            place=cart.place,
            address=Address.objects.get(pk=order_data["address"]),
            comment=order_data["comment"],
            total_price=cart.get_total_price(),
            ready_time=order_data["ready_time"],
            payment_id=payment_id,
        )
        for item in cart.items.select_related("product").prefetch_related("options"):
            order_item = OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )
            order_item.options.set(item.options.all())
        cart.items.all().delete()

        # Чистим сессию, чтобы по F5 не пытаться ещё раз
        del request.session["payment_id"]
        del request.session["order_data"]

        return render(request, "orders/order_success.html", {"order": order})
    else:
        return render(request, "orders/payment_failed.html")


@login_required
def order_items_partial(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product").prefetch_related("options")
    total_price = cart.get_total_price()
    
    # Check if cart is empty
    is_empty = not items.exists()
    
    html = render_to_string(
        "orders/_order_items.html",
        {
            "items": items,
            "total_price": total_price
        },
        request=request
    )
    return JsonResponse({
        "html": html, 
        "total_price": total_price,
        "is_empty": is_empty
    })
