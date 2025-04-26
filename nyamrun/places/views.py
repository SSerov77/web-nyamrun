from django.shortcuts import render, get_object_or_404

from places.models import Place, Product, Category


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

    return render(request, 'places/place_detail.html', {
        'place': place,
        'categories': categories_with_items,
    })
