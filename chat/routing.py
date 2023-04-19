from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat import consumers
from django.core.asgi import get_asgi_application

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns = [
    re_path(r"ws/chat/$", consumers.ChatRoomConsumer.as_asgi()),
]
