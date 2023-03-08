from django.db import models
from login.models import Custom_User

# Create your models here.


class Post_Model(models.Model):
    question_text = models.CharField(max_length=200)
    created_by = models.ForeignKey(Custom_User, related_name='posts_created', on_delete=models.CASCADE)
    viewed_by = models.ManyToManyField(Custom_User, related_name='posts_viewed', blank=True)

    def __str__(self):
        return str(self.id) + " => " + self.question_text
    

class Options_Model(models.Model):
    question = models.ForeignKey(Post_Model, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    chosen_by = models.ManyToManyField(Custom_User, related_name="user_option", blank=True)

    def __str__(self):
        return self.question.__str__() + " : " + self.choice_text