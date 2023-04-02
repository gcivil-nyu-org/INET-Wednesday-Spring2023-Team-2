from django.db import models
from login.models import Custom_User

from datetime import datetime, timedelta

# Create your models here.

class Connection_Model(models.Model):
    from_user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    connection_request_time = models.DateTimeField(default=datetime.now, blank=True)
    connection_answer_time = models.DateTimeField(default=datetime.now, blank=True)

    conection_answer_options = [
        ("Pending", "Pending"),
        ("Accept", "Accept"),
        ("Decline", "Decline"),
    ]

    connection_status = models.CharField(max_length=20, choices=conection_answer_options, default="Pending")

    def __str__(self):
        return str(self.id) + " => " + str(self.from_user) + " + " + str(self.to_user)

class Chat_History(models.Model):
    # user1 = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    # user2 = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    connection = models.ForeignKey(Connection_Model, on_delete=models.CASCADE, related_name="get_chat_history")

    history = models.JSONField(blank=True, default=list)

    # REQUIRED_FIELDS = ["user1", "user2", "history"]
