from django.contrib import admin
from .models import Chat_History, Chat_Message, Connection_Model, Group_Connection

# Register your models here.


admin.site.register(Connection_Model)
admin.site.register(Chat_Message)
admin.site.register(Chat_History)
admin.site.register(Group_Connection)
