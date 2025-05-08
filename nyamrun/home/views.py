from django.shortcuts import render
from places.models import Place, PlaceType


def index(request):
    try:
        coffee_shops = Place.objects.filter(type__slug='coffee_shop')
        bakeries = Place.objects.filter(type__slug='bakery')
        cafes = Place.objects.filter(type__slug='cafe')
    except PlaceType.DoesNotExist:
        coffee_shops = bakeries = cafes = Place.objects.none()

    context = {
        'coffee_shops': coffee_shops,
        'bakeries': bakeries,
        'cafes': cafes,
    }
    return render(request, 'home/home.html', context)
