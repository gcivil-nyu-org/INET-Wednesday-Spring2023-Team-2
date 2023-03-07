from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('home/', views.home_view, name="home_page"), 
]