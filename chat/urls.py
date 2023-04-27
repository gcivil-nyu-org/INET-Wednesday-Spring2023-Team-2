from django.urls import path
from . import views
from .views import SearchFriendsView

app_name = "connections"

urlpatterns = [
    # path("chat/", views.chat_view, name="chat_page"),
    # for test delete later
    # path("chat/<connection_id>/", views.chat_view_test, name="chat_page_test"),
    path("chat/", views.chat_page, name="chat_page"),
    path(
        "chat/get_chat_history/<connection_id>",
        views.chat_history_box_view,
        name="get_chat_history_box",
    ),
    path(
        "chat/get_chat_connections_list/",
        views.get_chat_connections_list_view,
        name="get_chat_connections_list",
    ),
    path(
        "chat/update_msg_seen/<message_id>/",
        views.update_msg_seen_view,
        name="update_msg_seen",
    ),
    path(
        "chat/get_chat_group_creation/<connection_id>/",
        views.Get_Chat_Group_Creation_View.as_view(),
        name="get_chat_group_creation",
    ),
    path(
        "chat/delete_group/<connection_id>/",
        views.delete_group_view,
        name="delete_group",
    ),
    path(
        "chat/exit_group/<connection_id>/",
        views.exit_group_view,
        name="exit_group",
    ),
    path(
        "chat/add_message_notification/",
        views.add_message_notification_view,
        name="add_message_notification",
    ),
    path(
        "chat/update_user_pending_status/",
        views.update_user_pending_status_view,
        name="update_user_pending_status",
    ),
    path("search/", SearchFriendsView.as_view(), name="search_friends"),
]
