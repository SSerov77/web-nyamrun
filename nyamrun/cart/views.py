from django.shortcuts import render

def cart_index(request):
    return render(request, 'cart/cart.html')
