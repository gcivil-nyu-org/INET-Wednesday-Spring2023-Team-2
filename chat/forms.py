from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Group_Connection, Connection_Model


class Group_Connection_Form(forms.ModelForm):
    class Meta:
        model = Group_Connection
        fields = ["group_name", "members", "profile_picture"]
