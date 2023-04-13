from django.urls import path, re_path
from . import views

from django.contrib.auth.decorators import login_required


app_name = "account"

urlpatterns = [
    path("login/", views.access_view, name="login_page"),
    # path('register/', views.register_view, name="register_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("activate/<uid>/<token>/", views.activate_view, name="activate_page"),
    path(
        "password-reset-confirmation/",
        views.password_reset_confirmation_view,
        name="passwordresetconfirmation_page",
    ),
    path(
        "password-reset/<uid>/<token>/",
        views.password_reset_view,
        name="passwordreset_page",
    ),
    path("profile/<str:username_>/", views.profile_view, name="profile_page"),
    path(
        "profile/<str:username_>/history",
        login_required(views.UserHistory.as_view()),
        name="profile_history_page",
    ),
    path(
        "profile/<str:username_>/postscreated",
        login_required(views.UserPostsCreated.as_view()),
        name="profile_postscreated_page",
    ),
    path(
        "profile/get_url/<page>/<username>",
        login_required(views.CurrentProfileURL.as_view()),
        name="get_current_profile_url_api",
    ),
    path(
        "profile/<str:username_>/friends",
        login_required(views.UserFriends.as_view()),
        name="profile_friends_page",
    ),
    # re_path("^profile/(?:name=(?P<username_>\w+))/$", views.UserHistory.as_view(), name="profile_page"),
    # re_path("profile/", login_required(views.UserHistory.as_view()), name="profile_page"),
    path(
        "profile/send_friend_request/<int:uid>/",
        views.send_friend_request,
        name="send_friend_request",
    ),
    path(
        "profile/<str:username_>/requests/",
        views.friend_requests,
        name="friend_requests",
    ),
    path(
        "profile/accept_friend_request/<int:uid>/",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
    path(
        "profile/decline_friend_request/<int:uid>/",
        views.decline_friend_request,
        name="decline_friend_request",
    ),
    path(
        "profile/block_friend/<int:connection_id>/",
        views.block_friend,
        name="block_friend",
    ),
    path(
        "profile/unblock_friend/<int:connection_id>/",
        views.unblock_friend,
        name="unblock_friend",
    ),
]
