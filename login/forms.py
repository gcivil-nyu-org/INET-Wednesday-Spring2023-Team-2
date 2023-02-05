from django import forms

from .models import UserRegistration


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        exclude = []
        widget = {
        'password': forms.PasswordInput,
        }
