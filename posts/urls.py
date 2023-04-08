from django.urls import path
from . import views
from .views import SearchPostsView


app_name = "posts"

urlpatterns = [
    path("home/", views.home_view, name="home_page"),
    path(
        "<category>/<int:pid>/", views.PostsView.as_view(), name="post_generation_page"
    ),
    path(
        "show_curr_post/<category>/<int:current_pid>",
        views.show_curr_post_api_view,
        name="show_curr_post_api",
    ),
    path(
        "show_next_post/<int:current_pid>/<category>",
        views.show_next_post_api_view,
        name="show_next_post_api",
    ),
    path(
        "get_current_url/<category>/<int:current_pid>",
        views.CurrentPostURL.as_view(),
        name="get_current_post_url_api",
    ),
    path(
        "show_comments_text/<int:current_pid>",
        views.show_comments_text_api,
        name="show_comments_text_api",
    ),
    path(
        "show_comments/<int:current_pid>",
        views.CommentsView.as_view(),
        name="show_comments_api",
    ),
    path(
        "show_categorybased_post/<int:current_pid>/<category>/",
        views.show_categorybased_post_api_view,
        name="show_categorybased_post_api",
    ),
    # path("get_current_url/", views.get_current_url_api_view, name="get_current_url_api")
    # path("get_current_url/", views.get_current_url_api_view, name="get_current_url_api"),
    path("create_poll/", views.create_poll, name="create_poll"),
    path("search/", SearchPostsView.as_view(), name="search_posts"),
    path(
        "report_comment/<int:comment_id>", views.report_comment, name="report_comment"
    ),
    path(
        "delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"
    ),
    path(
        "upvote_comment/<int:comment_id>", views.upvote_comment, name="upvote_comment"
    ),
    path(
        "downvote_comment/<int:comment_id>",
        views.downvote_comment,
        name="downvote_comment",
    ),
    path("report_post/<int:post_id>/", views.report_post, name="report_post"),
    path("get_back/<category>/<int:pid>", views.get_back_api_view, name="get_back_api"),
]
