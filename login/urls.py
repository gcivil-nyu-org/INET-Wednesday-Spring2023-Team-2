from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name="login_page"),
    path('register/', views.register_view, name="register_page"),
    path('logout/', views.logout_view, name="logout_page"),
    path('activate/<uid>/<token>', views.activate_view, name="activate_page"),
    
]