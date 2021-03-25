from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(request):
    if request.method == 'POST':
        form = NewPlaceForm(request.POST) 
        place = form.save() # save the form in a place object
        if form.is_valid():
            place.save() # save the place to the database
            return redirect('place_list') # return to the main page

    # Display all unvisited places
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places' : places, 'new_place_form': new_place_form })


def places_visited(request):
    visited = Place.objects.filter(visited=True) # display all visited places when on /visited page
    return render(request, 'travel_wishlist/visited.html', {'visited' : visited})


# Update unvisited places to visited when the button is clicked
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')