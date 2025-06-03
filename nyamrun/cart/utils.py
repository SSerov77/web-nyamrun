from cart.models import Cart
from django.db import transaction


def get_or_create_cart(request):
    """
    Возвращает Cart:
    - у анонимов: по request.session['cart_id'], или создаёт новую;
    - у аутентифицированных: по user (или создаёт новую), а затем
      если в сессии есть cart_id гостя — сливает её в user.cart.
    """
    # 1) Получаем гостевую корзину из сессии (если есть)
    guest_cart = None
    cart_id = request.session.get("cart_id")
    if cart_id:
        try:
            guest_cart = Cart.objects.get(id=cart_id, user__isnull=True)
        except Cart.DoesNotExist:
            guest_cart = None

    # 2) Если пользователь аутентифицирован
    if request.user.is_authenticated:
        # доставляем или создаём корзину пользователя
        user_cart, _ = Cart.objects.get_or_create(user=request.user)

        # если у нас была гостевая — мерджим
        if guest_cart and guest_cart.id != user_cart.id:
            with transaction.atomic():
                # переносим все позиции
                for item in guest_cart.items.all():
                    # пробуем найти дубликат в user_cart
                    existing = user_cart.items.filter(
                        product=item.product,
                        options__in=[o.id for o in item.options.all()],
                    ).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        # перепривязываем элемент к user_cart
                        item.cart = user_cart
                        item.save()
                # удаляем гостевую корзину
                guest_cart.delete()

            # чистим session
            request.session.pop("cart_id", None)

        return user_cart

    # 3) Анонимный: если гостевой нет — создаём
    if not guest_cart:
        guest_cart = Cart.objects.create()
        request.session["cart_id"] = guest_cart.id

    return guest_cart
