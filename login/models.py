from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Custom_User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    # name = models.CharField(max_length=50)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)