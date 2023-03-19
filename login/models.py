from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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

    profile_picture = models.ImageField(upload_to="images/", default= "default-profile.jpeg", validators=[validate_image_extension])

    def __str__(self):
        return self.username

    # name = models.CharField(max_length=50)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)