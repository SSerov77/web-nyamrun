from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from cart.models import Cart, CartItem
from cart.utils import get_or_create_cart
from catalog.models import Product, ProductOption


@require_POST
def cart_add_ajax(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get("quantity", 1))
    options_ids = request.POST.getlist("options")
    selected_options = ProductOption.objects.filter(id__in=options_ids)
    place = product.place

    # Если корзина ещё без place — связываем
    if cart.place is None:
        cart.place = place
        cart.save()
    elif cart.place != place:
        return JsonResponse({
            "error": (
                f"В корзине уже выбранo заведение: {cart.place.name}. "
                "Очистите корзину для заказа из другого заведения."
            )
        }, status=400)

    # Объединяем одинаковые позиции
    existing_items = CartItem.objects.filter(cart=cart, product=product)
    opts_set = set(selected_options.values_list("id", flat=True))

    for item in existing_items:
        if set(item.options.values_list("id", flat=True)) == opts_set:
            item.quantity += quantity
            item.save()
            break
    else:
        item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        item.options.set(selected_options)
        item.save()

    html = render_to_string("cart/cart_sidebar.html", {"cart": cart}, request=request)
    return JsonResponse({"cart_html": html})


def cart_detail_ajax(request):
    cart = get_or_create_cart(request)
    cart_html = render_to_string(
        "cart/cart_sidebar.html", {"cart": cart}, request=request
    )
    return JsonResponse({"cart_html": cart_html})


@require_POST
def cart_clear_ajax(request):
    cart = get_or_create_cart(request)
    if cart:
        cart.items.all().delete()
    cart_html = render_to_string(
        "cart/cart_sidebar.html", {"cart": cart}, request=request
    )
    return JsonResponse({"cart_html": cart_html})


@require_POST
def cart_remove_ajax(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

    cart_html = render_to_string(
        "cart/cart_sidebar.html", {"cart": cart}, request=request
    )
    return JsonResponse({"cart_html": cart_html})


@require_POST
def cart_update_ajax(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    cart_html = render_to_string(
        "cart/cart_sidebar.html", {"cart": cart}, request=request
    )
    return JsonResponse({"cart_html": cart_html})
