from django import forms
from .models import Place

# Allows the web application to communicate with the database.
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')
