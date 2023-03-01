from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.access_view, name="login_page"),
    # path('register/', views.register_view, name="register_page"),
    path('logout/', views.logout_view, name="logout_page"),
    path('activate/<uid>/<token>/', views.activate_view, name="activate_page"),
    path('password-reset-confirmation/', views.password_reset_confirmation_view, name="passwordresetconfirmation_page"),
    path('password-reset/<uid>/<token>/', views.password_reset_view, name="passwordreset_page"),
    path('profile/', views.profile_view, name="profile_page")
]