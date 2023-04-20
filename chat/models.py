from django.db import models
from login.models import Custom_User
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

import os

def validate_image_extension(value):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    ext = os.path.splitext(value.name)[-1]
    if not ext.lower() in allowed_extensions:
        raise ValidationError(
            "Only image files with the following extensions are allowed: %s"
            % ", ".join(allowed_extensions)
        )


# Create your models here.

class Group_Connection(models.Model):
    profile_picture = models.ImageField(
        upload_to="Group-Profile-Pictures/",
        default="Group-Profile-Pictures/default-group-profile.jpeg",
        validators=[validate_image_extension],
    )

    group_name = models.CharField(max_length=50, unique=True)

    members = models.ManyToManyField(Custom_User, related_name="groups_in")

    group_created_time = models.DateTimeField(auto_now_add=True)
    
    group_created_by = models.ForeignKey(Custom_User,  on_delete=models.CASCADE, related_name="groups_created")

    def __str__(self):
        return self.group_name

    ###USE:
    ### self._state.adding is True creating
    ### self._state.adding is False updating
    
    
    ##TODO: fix  "<Group_Connection: cc>" needs to have a value for field "id" before this many-to-many relationship can be used.
    # def save(self, *args, **kwargs):
    #     if self.members:
    #         #check max number of members <= 15
    #         if len(self.members) > 15:
    #             raise ValidationError("A Group can only have a max of 15 members!!")
    #         else:
    #             super(Group_Connection, self).save(*args, **kwargs)
    #     else:  
    #         super(Group_Connection, self).save(*args, **kwargs)



class Connection_Model(models.Model):
    from_user = models.ForeignKey(
        Custom_User, on_delete=models.CASCADE, related_name="connection_requests_sent", blank=True, null=True
    )
    to_user = models.ForeignKey(
        Custom_User,
        on_delete=models.CASCADE,
        related_name="connection_requests_received",
        blank = True,
        null = True
    )
    group = models.OneToOneField(
        Group_Connection,
        on_delete=models.CASCADE,
        related_name="connection_id_for_group",
        blank = True,
        null = True
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
        if self.from_user and self.to_user:
            return str(self.id) + " => " + str(self.from_user) + " + " + str(self.to_user)
        else:
            return str(self.id) + " => " + self.group.__str__()

    def get_friend(self, user):
        if self.from_user and self.to_user:
            if user == self.from_user:
                return self.to_user
            return self.from_user
        else:
            return self.group

    def connection_exists(cls, from_user, to_user):
        return (
            cls.objects.filter(from_user=from_user, to_user=to_user).exists()
            or cls.objects.filter(from_user=to_user, to_user=from_user).exists()
        )

    # latest_message = models.CharField(max_length=23, blank=True)

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
        #2 users
        if self.to_user and self.from_user and not self.group:
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
            
        #group
        elif self.group and not (self.from_user or self.to_user):
            #check no blocks
            if self.blocked_by:
                raise ValidationError("Group Connection cannot be blocked from Connection Model!!")
            
            #save as accepted connection
            else:
                self.connection_status = "Accepted"
                super(Connection_Model, self).save(*args, **kwargs)

        else:
            raise ValidationError("Connection requires 2 users/ group!!")



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

    connection = models.OneToOneField(
        Connection_Model, on_delete=models.CASCADE, related_name="get_chat_history"
    )

    # history = models.JSONField(blank=True, default=list)

    history = models.ManyToManyField(Chat_Message, blank=True)

    def append_latest_message(self, message, timestamp):
        # if len(message) <= 20:
        #     self.connection.latest_message = message
        #     self.connection.latest_message_time = timestamp
        # else:
        #     self.connection.latest_message = message[:20] + "..."

        self.connection.latest_message_time = timestamp

        self.connection.save()

    # REQUIRED_FIELDS = ["user1", "user2", "history"]
