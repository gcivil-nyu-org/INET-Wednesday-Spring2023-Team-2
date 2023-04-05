from django.urls import path
from . import views

app_name = "connections"

urlpatterns = [
    # path("chat/", views.chat_view, name="chat_page"),
    # for test delete later
    path("chat/<connection_id>/", views.chat_view_test, name="chat_page_test"),
    path("chat/", views.chat_page, name="chat_page"),
]
