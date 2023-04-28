from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Group_Connection, Connection_Model


class Group_Connection_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        friends = kwargs.pop("friends", None)
        super(Group_Connection_Form, self).__init__(*args, **kwargs)

        if friends is not None:
            self.fields["members"].queryset = friends

    class Meta:
        model = Group_Connection
        fields = ["group_name", "members", "profile_picture"]
