from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import random

from .models import Post_Model
from login.models import Custom_User

# Create your views here.
    
#home page - will generate random post id that user hasn't interacted with to display for user - will change to empty later in urls
#generate id and redirect/reverse with that parameter
def home_view(request):
    pids = Post_Model.objects.all()
    
    ##to check if user has alread seen/ interaacted with the post
    # if request.user.is_authenticated:
    #     user_posts_viewed = request.user.posts_viewed.all()
    #     pids = pids.difference(user_posts_viewed)

    pid = random.choice(list(pids))
    pid = pid.pk
    
    return redirect(reverse('posts:post_generation_page', kwargs={'pid':pid}))


def posts_view(request, pid):
    post_ = Post_Model.objects.get(pk=pid)
    contents = {'post': post_}
    return render(request, "pages/post_home.html", contents)
