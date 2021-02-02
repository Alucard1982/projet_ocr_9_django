from django.contrib.auth.forms import UserCreationForm
from django import forms
from litLogin.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
