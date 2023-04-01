from django.urls import path
from . import views

app_name = "connections"

urlpatterns = [
    # path("chat/", views.chat_view, name="chat_page"),
    #for test delete later
    path("chat/<chat_box_name>/", views.chat_view_test, name="chat_page_test"),
]
