from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderItem


@login_required
def order_create(request):
    cart = request.user.cart
    items = cart.items.select_related('product').prefetch_related('options')
    place = cart.place

    if request.method == "POST":
        form = OrderForm(request.POST, place=place)
        if form.is_valid():
            address = form.cleaned_data['address']
            ready_time = form.cleaned_data['time']
            comment = form.cleaned_data['comment']
            total_price = cart.get_total_price()
            order = Order.objects.create(
                user=request.user,
                place=place,
                address=address,
                comment=comment,
                total_price=total_price,
                ready_time=ready_time
            )
            for item in items:
                order_item = OrderItem.objects.create(
                    order=order, product=item.product, quantity=item.quantity
                )
                order_item.options.set(item.options.all())
            cart.items.all().delete()
            return redirect('home')
    else:
        form = OrderForm(place=place)

    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart': cart,
        'items': items,
    })
