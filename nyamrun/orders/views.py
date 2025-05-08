import json

from yookassa import Configuration, Payment

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from orders.forms import OrderForm
from orders.models import Order, OrderItem
from orders.helper import get_time_choices
from places.models import Address
from cart.models import Cart


@login_required
def order_create(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').prefetch_related('options')
    place = cart.place
    time_choices = get_time_choices(place=place)

    if request.method == "POST":
        form = OrderForm(request.POST, place=place, time_choices=time_choices)

        if not cart.total_price():
            total_price = "0"
        else:
            total_price = str(cart.total_price())

        if form.is_valid():
            request.session['order_data'] = {
                'address': form.cleaned_data['address'].pk,
                'ready_time': form.cleaned_data['time'],
                'comment': form.cleaned_data['comment'],
                'total_price': total_price,
            }

            return redirect('order_payment')
    else:
        form = OrderForm(place=place, time_choices=time_choices)

    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart': cart,
        'items': items,
    })


@login_required
def order_payment(request):
    user = request.user
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('order_create')

    cart = user.cart
    total_price = cart.total_price()

    receipt_items = []
    for item in cart.items.select_related('product').prefetch_related('options'):
        desc = item.product.name
        if item.options.exists():
            desc += " (" + ", ".join([opt.name for opt in item.options.all()]) + ")"
        receipt_items.append({
            "description": desc,
            "quantity": item.quantity,
            "amount": {
                "value": str(item.product.price),
                "currency": "RUB",
            },
            "vat_code": 4,
        })

    customer_email = user.email
    if not customer_email:
        return render(request, "orders/payment_failed.html", {
            "error": "У пользователя не указан email. Без email фискальный чек невозможен."
        })

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    payment = Payment.create({
        "amount": {"value": str(total_price), "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse('order_success'))
        },
        "capture": True,
        "description": f"Оплата заказа от {user.username}",
        "metadata": {
            "user_id": user.id,
            "order_data": json.dumps(order_data)
        },
        "receipt": {
            "customer": {
                "email": customer_email,
                "full_name": user.get_full_name() or user.username,
            },
            "items": receipt_items
        }
    })
    request.session['payment_id'] = payment.id
    return redirect(payment.confirmation.confirmation_url)


@login_required
def order_success(request):
    payment_id = request.session.get('payment_id')
    order_data = request.session.get('order_data')
    user = request.user
    cart = user.cart

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    payment = Payment.find_one(payment_id)

    if payment.status == "succeeded":
        order = Order.objects.create(
            user=user,
            place=cart.place,
            address=Address.objects.get(pk=order_data['address']),
            comment=order_data['comment'],
            total_price=cart.total_price(),
            ready_time=order_data['ready_time'],
            payment_id=payment_id,
        )
        for item in cart.items.select_related('product').prefetch_related('options'):
            order_item = OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )
            order_item.options.set(item.options.all())
        cart.items.all().delete()

        del request.session['payment_id']
        del request.session['order_data']

        return render(request, 'orders/order_success.html', {'order': order})
    else:
        return render(request, 'orders/payment_failed.html')
