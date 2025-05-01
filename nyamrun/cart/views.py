from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from cart.models import Cart, CartItem
from catalog.models import Product, ProductOption


@require_POST
def cart_add_ajax(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Авторизуйтесь'}, status=403)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    options_ids = request.POST.getlist('options')
    selected_options = ProductOption.objects.filter(id__in=options_ids)
    place = product.place

    if cart.place is None:
        cart.place = place
        cart.save()
    elif cart.place != place:
        return JsonResponse(
            {
                'error': (
                    f'В корзине уже выбранo заведение: {cart.place.name}.'
                    'Очистите корзину для заказа из другого заведения.'
                )
            },
            status=400
        )

    existing_items = CartItem.objects.filter(cart=cart, product=product)
    selected_options_ids = set(selected_options.values_list('id', flat=True))

    for item in existing_items:
        item_options_ids = set(item.options.values_list('id', flat=True))
        if item_options_ids == selected_options_ids:
            item.quantity += quantity
            item.save()
            break
    else:
        item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity)
        item.options.set(selected_options)
        item.save()

    cart_html = render_to_string(
        'cart/cart_sidebar.html',
        {'cart': cart},
        request=request
    )
    return JsonResponse({'cart_html': cart_html})


def cart_detail_ajax(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_html = render_to_string(
        'cart/cart_sidebar.html',
        {'cart': cart},
        request=request
    )
    return JsonResponse({'cart_html': cart_html})


@require_POST
def cart_clear_ajax(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
    cart_html = render_to_string(
        'cart/cart_sidebar.html',
        {'cart': cart},
        request=request
    )
    return JsonResponse({'cart_html': cart_html})
