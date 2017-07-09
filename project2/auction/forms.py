from django.contrib.auth.models import User
from django import forms
from .models import product


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class BidForm(forms.ModelForm):

    class Meta:
        model = product
        fields = ['price']