from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from places.models import Place
from cart.models import Cart
from catalog.models import Product, Category


def place_list(request):
    places = Place.objects.all()
    selected_types = request.GET.getlist('type')
    selected_cuisines = request.GET.getlist('cuisine')

    if selected_types:
        places = places.filter(type__in=selected_types)

    if selected_cuisines:
        try:
            category_ids = list(map(int, selected_cuisines))
            places = places.filter(categories__id__in=category_ids).distinct()
        except ValueError:
            pass

    categories = Category.objects.all()

    context = {
        'places': places,
        'categories': categories,
        'selected_types': selected_types,
        'selected_cuisines': selected_cuisines,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'places/place_list_items.html', context)
    else:
        return render(request, 'places/place_list.html', context)


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    categories = place.categories.all()
    categories_with_items = []
    for category in categories:
        items = Product.objects.filter(place=place, category=category)
        categories_with_items.append({
            'category': category,
            'items': items,
        })
    cart, _ = Cart.objects.get_or_create(user=request.user)

    return render(request, 'places/place_detail.html', {
        'place': place,
        'categories': categories_with_items,
        'cart': cart,
    })


def product_modal_data(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    options = product.options.all()
    options_data = [{'id': opt.id, 'name': opt.name, 'additional_price': float(
        opt.additional_price)} for opt in options]

    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'image_url': product.image.url if product.image else '',
        'description': product.description,
        'options': options_data,
        'add_url': reverse('cart_add_ajax', args=[product.id]),
    })
