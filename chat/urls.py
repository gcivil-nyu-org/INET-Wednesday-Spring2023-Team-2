from django.urls import path
from . import views

app_name = "connections"

urlpatterns = [
    # path("chat/", views.chat_view, name="chat_page"),
    # for test delete later
    path("chat/<connection_id>/", views.chat_view_test, name="chat_page_test"),
    path("test/abc/", views.chat_get_friends_info, name="chat_page"),
]
