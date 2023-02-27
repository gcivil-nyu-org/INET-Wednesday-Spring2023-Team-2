from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Custom_User



class PasswordResetConfirmationForm(forms.Form):
    username_or_email = forms.CharField()


class PasswordResetForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = []


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        # widget = {
        # 'password': forms.PasswordInput,
        # }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Custom_User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
