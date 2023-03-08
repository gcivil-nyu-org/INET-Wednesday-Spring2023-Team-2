from django.db import models
from login.models import Custom_User

# Create your models here.


class Post_Model(models.Model):
    question_text = models.CharField(max_length=200)
    created_by = models.ForeignKey(Custom_User, related_name='posts_created')

    def __str__(self):
        return self.question_text
    

class Options_Model(models.Model):
    question = models.ForeignKey(Post_Model, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text