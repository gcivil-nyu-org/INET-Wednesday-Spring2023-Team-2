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
    path("profile/<str:username_>/history", login_required(views.UserHistory.as_view()), name="profile_history_page")
    # re_path("^profile/(?:name=(?P<username_>\w+))/$", views.UserHistory.as_view(), name="profile_page"),
    # re_path("profile/", login_required(views.UserHistory.as_view()), name="profile_page"),

]
