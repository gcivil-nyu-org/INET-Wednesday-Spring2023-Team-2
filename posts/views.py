from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.

def redirect_to_home_view(request):
    return redirect(reverse('home_page'))
    

def home_view(request):
    return render(request, "pages/home.html")
