from django.db import models
from login.models import Custom_User
from django.core.exceptions import ValidationError

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
    blocked_by = models.ForeignKey(
        Custom_User,
        on_delete=models.CASCADE,
        related_name="blocked_users",
        blank=True,
        null=True,
    )

    connection_request_time = models.DateTimeField(auto_now_add=True)
    connection_answer_time = models.DateTimeField(default=datetime.now)

    conection_answer_options = [
        ("Pending", "Pending"),
        ("Accepted", "Accept"),
        ("Declined", "Decline"),
        ("Blocked", "Block"),
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

    def connection_exists(cls, from_user, to_user):
        return (
            cls.objects.filter(from_user=from_user, to_user=to_user).exists()
            or cls.objects.filter(from_user=to_user, to_user=from_user).exists()
        )

    latest_message = models.CharField(max_length=23, blank=True)

    latest_message_time = models.DateTimeField(blank=True, null=True)

    def save_checks(self, to_user, from_user):
        if Connection_Model.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            ##change from pending to accepted or declined
            if (
                self.connection_status == "Accepted"
                or self.connection_status == "Declined"
            ) and Connection_Model.objects.get(
                from_user=from_user, to_user=to_user
            ).connection_status == "Pending":
                return True

            ##change from declined to pending i.e. requesting again after initial decline
            elif (
                self.connection_status == "Pending"
                and Connection_Model.objects.get(
                    from_user=from_user, to_user=to_user
                ).connection_status
                == "Declined"
            ):
                return True

            ##change from accepted to blocked
            elif self.connection_status == "Blocked" and (
                Connection_Model.objects.get(
                    from_user=from_user, to_user=to_user
                ).connection_status
                == "Accepted"
            ):
                return True

            ##change from blocked to accepted or declined
            elif (
                self.connection_status == "Accepted"
                or self.connection_status == "Declined"
            ) and (
                Connection_Model.objects.get(
                    from_user=from_user, to_user=to_user
                ).connection_status
                == "Blocked"
            ):
                return True

            elif (
                self.connection_status
                == Connection_Model.objects.get(
                    from_user=from_user, to_user=to_user
                ).connection_status
            ):
                return True

        return False

    def save(self, *args, **kwargs):
        # print(self.connection_status, self.from_user, self.to_user, Connection_Model.objects.get(
        #         from_user=self.from_user, to_user=self.to_user
        #     ).connection_status)
        if not (
            Connection_Model.objects.filter(
                from_user=self.from_user, to_user=self.to_user
            ).exists()
            or Connection_Model.objects.filter(
                from_user=self.to_user, to_user=self.from_user
            ).exists()
        ):
            super(Connection_Model, self).save(*args, **kwargs)

        elif self.save_checks(to_user=self.to_user, from_user=self.from_user):
            super(Connection_Model, self).save(*args, **kwargs)

        elif self.save_checks(to_user=self.from_user, from_user=self.to_user):
            super(Connection_Model, self).save(*args, **kwargs)

        else:
            raise ValidationError("Connection between specified users already exists!!")

        # ((Connection_Model.objects.filter(from_user=self.from_user, to_user=self.to_user).exists()
        # and Connection_Model.objects.get(from_user=self.from_user, to_user=self.to_user).connection_status == "Declined") or (Connection_Model.objects.filter(from_user=self.to_user, to_user=self.from_user).exists() and Connection_Model.objects.get(from_user=self.to_user, to_user=self.from_user).connection_status == "Declined"))

    # def save(self, *args, **kwargs):
    #     if (
    #         Connection_Model.objects.filter(
    #             from_user=self.from_user, to_user=self.to_user
    #         ).exists()
    #         and Connection_Model.objects.get(
    #             from_user=self.from_user, to_user=self.to_user
    #         ).connection_status
    #         == "Pending"
    #         and self.connection_status != "Pending"
    #     ):
    #         Connection_Model.objects.get(
    #             from_user=self.from_user, to_user=self.to_user
    #         ).delete()
    #         super(Connection_Model, self).save(*args, **kwargs)
    #     elif (
    #         Connection_Model.objects.filter(
    #             to_user=self.from_user, from_user=self.to_user
    #         ).exists()
    #         and Connection_Model.objects.get(
    #             to_user=self.from_user, from_user=self.to_user
    #         ).connection_status
    #         == "Pending"
    #         and self.connection_status != "Pending"
    #     ):
    #         Connection_Model.objects.get(
    #             to_user=self.from_user, from_user=self.to_user
    #         ).delete()
    #         super(Connection_Model, self).save(*args, **kwargs)
    #     elif (
    #         Connection_Model.objects.filter(
    #             from_user=self.from_user, to_user=self.to_user
    #         ).exists()
    #     ) or (
    #         Connection_Model.objects.filter(
    #             to_user=self.from_user, from_user=self.to_user
    #         ).exists()
    #     ):
    #         raise ValidationError("Connection between specified users already exists!!")

    #     super(Connection_Model, self).save(*args, **kwargs)


class Chat_Message(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    message = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    seen_by = models.ManyToManyField(Custom_User, related_name="messages_seen")

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

    def append_latest_message(self, message, timestamp):
        if len(message) <= 20:
            self.connection.latest_message = message
            self.connection.latest_message_time = timestamp
        else:
            self.connection.latest_message = message[:20] + "..."
            self.connection.latest_message_time = timestamp

        self.connection.save()

    # REQUIRED_FIELDS = ["user1", "user2", "history"]
