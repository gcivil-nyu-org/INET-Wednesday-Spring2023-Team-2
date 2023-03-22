from django.db import models
from login.models import Custom_User
from django.utils import timezone
from multiselectfield import MultiSelectField

from datetime import datetime, timedelta
from pytz import timezone


def resut_reveal_time_function():
    return datetime.now() + timedelta(hours=0)


# Create your models here.


class Post_Model(models.Model):
    question_text = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        Custom_User, related_name="posts_created", on_delete=models.CASCADE
    )
    viewed_by = models.ManyToManyField(
        Custom_User, related_name="posts_viewed", blank=True
    )

    # view_time = models.DateTimeField(auto_now_add=True, blank=True)

    category_list = [
        ("sports", "Sports"),
        ("fantasy", "Fantasy"),
        ("entertainment", "Entertainment"),
        ("misc", "Misc"),
    ]
    category = MultiSelectField(
        max_length=20, choices=category_list, max_choices=3, default="misc"
    )

    # created_time = models.DateTimeField(auto_now_add=True, blank=True)
    created_time = models.DateTimeField(
        default=datetime.now, editable=False, blank=True
    )
    result_reveal_time = models.DateTimeField(default=resut_reveal_time_function)

    def __str__(self):
        return str(self.id) + " => " + self.question_text


class Options_Model(models.Model):
    question = models.ForeignKey(Post_Model, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    chosen_by = models.ManyToManyField(
        Custom_User, related_name="user_option", blank=True
    )

    color_list = [
        ("AED9E0", "AED9E0"),
        ("8CB369", "8CB369"),
        ("D7A5E4", "D7A5E4"),
        ("5D6DD3", "5D6DD3"),
    ]
    color = models.CharField(max_length=6, choices=color_list, default="AED9E0")

    def __str__(self):
        return self.question.__str__() + " : " + self.choice_text


class Comments_Model(models.Model):
    question = models.ForeignKey(Post_Model, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(
        Custom_User,
        related_name="comments_created",
        on_delete=models.CASCADE,
        default=1,
    )
    comment_text = models.CharField(max_length=500)
    commented_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return (
            self.question.__str__()
            + " => "
            + self.commented_by.__str__()
            + " : "
            + self.comment_text
        )


class UserPostViewTime(models.Model):
    user = models.ForeignKey(
        Custom_User, related_name="posts_view_time", on_delete=models.CASCADE
    )

    post = models.ForeignKey(Post_Model, on_delete=models.CASCADE)

    view_time = models.DateTimeField(default=datetime.now, blank=True)
