from .models import Fly, Country
from django import forms
from django.contrib.auth.models import User

class FlyForm(forms.ModelForm):

    class Meta:
        model = Fly
        fields = ['orginplace', 'descinationplace', 'price', 'day', 'currency', 'number_city', 'airports', 'date', 'endDate']



class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ['name']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
