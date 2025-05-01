from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string

from cart.models import Cart, CartItem
from catalog.models import Product, ProductOption
from places.models import Place


def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').prefetch_related('options')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    option_ids = request.POST.getlist('options')

    cart, created = Cart.objects.get_or_create(user=request.user)
    options = ProductOption.objects.filter(id__in=option_ids)

    place = product.place

    if cart.place is None:
        cart.place = place
        cart.save()
    elif cart.place != place:
        return render(request, 'cart/wrong_place.html', {'current_place': cart.place, 'new_place': place})

    found_item = None
    for item in cart.items.filter(product=product):
        item_options = set(item.options.values_list('id', flat=True))
        if item_options == set(map(int, option_ids)):
            found_item = item
            break

    if found_item:
        found_item.quantity += quantity
        found_item.save()
    else:
        new_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        new_item.options.set(options)
        new_item.save()

    return redirect('cart_detail')


@require_POST
def cart_add_ajax(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Авторизуйтесь'}, status=403)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    options_ids = request.POST.getlist('options')
    selected_options = ProductOption.objects.filter(id__in=options_ids)

    # === ОПРЕДЕЛЯЕМ PLACE (теперь всегда через FK) ===
    place = product.place

    # === Привязываем Cart к заведению ===
    if cart.place is None:
        cart.place = place
        cart.save()
    elif cart.place != place:
        return JsonResponse({'error': f'В корзине уже выбранo заведение: {cart.place.name}. Очистите корзину для заказа из другого заведения.'}, status=400)

    # === Дальше твоя логика поиска CartItem ===
    existing_items = CartItem.objects.filter(cart=cart, product=product)
    selected_options_ids = set(selected_options.values_list('id', flat=True))

    for item in existing_items:
        item_options_ids = set(item.options.values_list('id', flat=True))
        if item_options_ids == selected_options_ids:
            # Найден — увеличиваем количество
            item.quantity += quantity
            item.save()
            break
    else:
        # Не найден — создаём новый элемент с выбранными опциями
        item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        item.options.set(selected_options)
        item.save()

    cart_html = render_to_string('cart/cart_sidebar.html', {'cart': cart}, request=request)
    return JsonResponse({'cart_html': cart_html})

def cart_detail_ajax(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_html = render_to_string('cart/cart_sidebar.html', {'cart': cart}, request=request)
    return JsonResponse({'cart_html': cart_html})


@require_POST
def cart_clear_ajax(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
    cart_html = render_to_string('cart/cart_sidebar.html', {'cart': cart}, request=request)
    return JsonResponse({'cart_html': cart_html})