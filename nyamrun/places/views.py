from django.shortcuts import render, get_object_or_404
from places.models import Place, Category, Product


def place_list(request):
    places = Place.objects.all()
    return render(request, 'places/place_list.html', {'places': places})



def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)

    # Получаем категории заведения
    categories = place.categories.all()

    # Для удобства собираем категории вместе с товарами в каждой
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
