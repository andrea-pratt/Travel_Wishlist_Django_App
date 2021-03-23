from django.shortcuts import render


def place_list(request):
    return render(request, 'travel_wishlist/wishlist.html')
