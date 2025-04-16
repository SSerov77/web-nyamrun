from django.shortcuts import render


def places_list(request):
    return render(request, 'places/places_list.html')


def place_detail(request, pk):
    return render(request, 'places/place_detail.html', {'pk': pk})
