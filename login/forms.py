from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Custom_User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = ['username', 'email']
        # widget = {
        # 'password': forms.PasswordInput,
        # }
