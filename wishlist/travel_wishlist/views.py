from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages



@login_required
def place_list(request):
    if request.method == 'POST':
        form = NewPlaceForm(request.POST) 
        place = form.save(commit=False) # save the form in a place object
        place.user = request.user
        if form.is_valid():
            place.save() # save the place to the database
            return redirect('place_list') # return to the main page

    # Display all unvisited places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places' : places, 'new_place_form': new_place_form })

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True) # display all visited places when on /visited page
    return render(request, 'travel_wishlist/visited.html', {'visited' : visited})


# Update unvisited places to visited when the button is clicked
@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # get the requested place object or display a 404 error if it doesn't exist
        place = get_object_or_404(Place, pk=place_pk) 
        if place.user == request.user: # only visit request place if it belongs to the current user
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    return redirect('place_list') 


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user: # return an error if a user attempts to view details for a place that doesn't belong to them
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)

        if form.is_valid(): # if all fields are filled out correctly, save the contents of the form to database
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    else: # this displays the place details if the request method is 'GET' instead of 'POST'
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()