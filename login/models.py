from django.db import models
from django.contrib.auth.models import AbstractUser

from posts.models import Post_Model

# Create your models here.

# in Post_Model => created_by = Foreignkey(User, name="post_creation") so I can do User.post_creation.all() and Post.created_by = User1
# I can do Post.viewed_by.all() and User.posts_viewed.all()

class Custom_User(AbstractUser):
    posts_viewed = models.ManyToManyField(Post_Model, related_name='viewed_by')
    

    def __str__(self):
        return self.username
    # name = models.CharField(max_length=50)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)