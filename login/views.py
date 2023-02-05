from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from .forms import LoginForm
from .forms import RegisterForm


# Create your views here.

def login_view(request):
    my_form = LoginForm()
    contents = {'form': my_form}
    return render(request, "pages/login.html", contents)


def register_view(request):
    form = RegisterForm()
    contents = {'form': form}
    return render(request, "pages/register.html", contents)