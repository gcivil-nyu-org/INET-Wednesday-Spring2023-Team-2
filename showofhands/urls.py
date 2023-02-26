"""showofhands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts.views import redirect_to_home_view
from posts.views import home_view
from login.views import login_view
from login.views import register_view
from login.views import logout_view
from header.views import header_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_home_view, name="go_home"),
    path('home/', home_view, name="home_page"),
    path('login/', login_view, name="login_page"),
    path('register/', register_view, name="register_page"),
    path('logout/', logout_view, name="logout_page"),
    path('header/', header_view, name='header'),
]
