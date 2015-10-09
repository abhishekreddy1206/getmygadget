from django import forms
from django.contrib.auth.models import User

from models import DTUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = DTUser
        fields = ('address1', 'address2', 'city', 'state', 'zipcode', 'phone',)
