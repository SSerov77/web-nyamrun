from django.shortcuts import render

def restaurants_list(request):
    return render(request, 'catalog/restaurants.html')

def restaurant_detail(request, pk):
    return render(request, 'catalog/restaurant_item.html', {'pk': pk})
