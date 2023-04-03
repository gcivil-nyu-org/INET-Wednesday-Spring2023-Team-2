from django.db import models
from login.models import Custom_User

from datetime import datetime, timedelta

# Create your models here.


class Connection_Model(models.Model):
    from_user = models.ForeignKey(
        Custom_User, on_delete=models.CASCADE, related_name="connection_requests_sent"
    )
    to_user = models.ForeignKey(
        Custom_User,
        on_delete=models.CASCADE,
        related_name="connection_requests_received",
    )

    connection_request_time = models.DateTimeField(auto_now_add=True)
    connection_answer_time = models.DateTimeField(default=datetime.now)

    conection_answer_options = [
        ("Pending", "Pending"),
        ("Accepted", "Accept"),
        ("Declined", "Decline"),
    ]

    connection_status = models.CharField(
        max_length=20, choices=conection_answer_options, default="Pending"
    )

    def __str__(self):
        return str(self.id) + " => " + str(self.from_user) + " + " + str(self.to_user)

    def get_friend(self, user):
        if user == self.from_user:
            return self.to_user
        return self.from_user


class Chat_Message(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    message = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " => " + str(self.user) + " " + str(self.timestamp)

    def disp_msg(self):
        return str(self.message) + " by " + str(self.user) + "\n"


class Chat_History(models.Model):
    # user1 = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    # user2 = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    connection = models.ForeignKey(
        Connection_Model, on_delete=models.CASCADE, related_name="get_chat_history"
    )

    # history = models.JSONField(blank=True, default=list)

    history = models.ManyToManyField(Chat_Message, blank=True)

    # REQUIRED_FIELDS = ["user1", "user2", "history"]
