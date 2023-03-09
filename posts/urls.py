from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path("home/", views.home_view, name="home_page"),
    path("<int:pid>/", views.posts_view, name="post_generation_page"),
    path("test1/", views.test1_view, name="test1")
]
