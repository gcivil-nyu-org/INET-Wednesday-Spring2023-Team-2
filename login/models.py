from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import gettext_lazy as _

import os


# from posts.models import Post_Model

# Create your models here.

# in Post_Model => created_by = Foreignkey(User, name="post_creation") so I can do User.post_creation.all() and Post.created_by = User1
# I can do Post.viewed_by.all() and User.posts_viewed.all()


def validate_image_extension(value):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    ext = os.path.splitext(value.name)[-1]
    if not ext.lower() in allowed_extensions:
        raise ValidationError(
            "Only image files with the following extensions are allowed: %s"
            % ", ".join(allowed_extensions)
        )


class Custom_User(AbstractUser):
    # posts_viewed = models.ManyToManyField(Post_Model, related_name='viewed_by')

    profile_picture = models.ImageField(
        upload_to="Profile-Pictures/",
        default="Profile-Pictures/default-profile.jpeg",
        validators=[validate_image_extension],
    )

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w]+$",
                _(
                    "Enter a valid username. "
                    "This value may contain only letters, numbers "
                    "and _ characters."
                ),
                "invalid",
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    has_unread_messages = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    # name = models.CharField(max_length=50)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)
