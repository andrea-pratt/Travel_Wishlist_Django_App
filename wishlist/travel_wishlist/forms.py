from django import forms
from .models import Place

# Allows the web application to communicate with the database.
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')


# Tell the form to use a data picker and date data type for date_visited field
class DateInput(forms.DateInput):
    input_type = 'date'


# Define the fields for the Trip Review form that displays when a visited place is selected
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }
