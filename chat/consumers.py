import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat_History, Connection_Model
from login.models import Custom_User

from datetime import datetime, timedelta

# chat_box_name = connection_id
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["connection_id"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        connection_id = text_data_json["connection_id"]
        timestamp = datetime.now()

        print(message, username)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )
        ##todo: save data to db

        try:
            chat_history = Connection_Model.objects.get(id=connection_id).get_chat_history
        except (KeyError, Chat_History.DoesNotExist):
            chat_history = Chat_History.objects.create(connection = Connection_Model.objects.get(id=connection_id))
            chat_history = chat_history

        # chat_history.history.append({"message": message,"username": username, "timestamp": timestamp},)
        # chat_history.save()
        
        chat_history.history.create(user=Custom_User.objects.get(username=username), message=message, timestamp=timestamp)
       


    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

    pass
