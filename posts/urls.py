from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path("home/", views.home_view, name="home_page"),
    path("<int:pid>/", views.PostsView.as_view(), name="post_generation_page"),
    path("show_curr_post/", views.show_curr_post_api_view, name="show_curr_post_api"),
    path("show_next_post/", views.show_next_post_api_view, name="show_next_post_api"),
    path("get_current_url/", views.get_current_url_api_view, name="get_current_url_api")
]
