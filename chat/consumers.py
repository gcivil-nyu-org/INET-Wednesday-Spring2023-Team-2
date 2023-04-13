import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat_History, Connection_Model
from login.models import Custom_User

from datetime import datetime, timedelta

from asgiref.sync import sync_to_async, async_to_sync


# chat_box_name = connection_id
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["connection_id"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def blockclose(self, connection_id):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": "",
                "username": "",
                "timestamp": "",
                "closed": True,
            },
        )

    @sync_to_async
    def store_info_db(self, message, username, connection_id, timestamp):
        try:
            chat_history = Chat_History.objects.get(
                connection=Connection_Model.objects.get(id=connection_id)
            )
        except (KeyError, Chat_History.DoesNotExist):
            chat_history = Chat_History.objects.create(
                connection=Connection_Model.objects.get(id=connection_id)
            )

        # chat_history.history.append({"message": message,"username": username, "timestamp": timestamp},)
        # chat_history.save()

        if (
            Connection_Model.objects.get(id=connection_id).connection_status
            == "Blocked"
        ):
            async_to_sync(self.blockclose)(connection_id)
            return False

        chat_history.history.create(
            user=Custom_User.objects.get(username=username),
            message=message,
            timestamp=timestamp,
        )

        return True

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        connection_id = text_data_json["connection_id"]
        timestamp = datetime.now()

        success = await self.store_info_db(message, username, connection_id, timestamp)

        if success:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chatbox_message",
                    "message": message,
                    "username": username,
                    "timestamp": str(timestamp),
                    "closed": False,
                },
            )

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]
        closed = event["closed"]

        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "timestamp": timestamp,
                    "closed": closed,
                }
            )
        )

    pass
