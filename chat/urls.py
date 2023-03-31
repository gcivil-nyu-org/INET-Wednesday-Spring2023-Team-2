from django.urls import path
from . import views

app_name = "connections"

urlpatterns = [
    path("chat/", views.chat_view, name="chat_page"),
]
