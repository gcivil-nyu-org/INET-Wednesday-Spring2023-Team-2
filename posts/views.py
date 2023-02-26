from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
    
#home page - will generate random post id to display for user - will change to empty later in urls
#generate id and redirect/reverse with that parameter
def home_view(request):
    return render(request, "pages/home.html")