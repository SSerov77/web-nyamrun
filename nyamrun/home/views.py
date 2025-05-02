from django.shortcuts import render
from places.models import Place, PlaceType

def index(request):
    coffee_shops = Place.objects.filter(type=PlaceType.COFFEE_SHOP)
    bakeries = Place.objects.filter(type=PlaceType.BAKERY)
    cafes = Place.objects.filter(type=PlaceType.CAFE)

    context = {
        'coffee_shops': coffee_shops,
        'bakeries': bakeries,
        'cafes': cafes,
    }
    return render(request, 'home/home.html', context)

