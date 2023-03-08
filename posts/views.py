from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import random


from .models import Post_Model, Options_Model
from login.models import Custom_User


# Create your views here.


# home page - will generate random post id that user hasn't interacted with to display for user - will change to empty later in urls
# generate id and redirect/reverse with that parameter
def home_view(request):
    pids = Post_Model.objects.all()

    ##to check if user has alread seen/ interaacted with the post
    # if request.user.is_authenticated:
    #     user_posts_viewed = request.user.posts_viewed.all()
    #     pids = pids.difference(user_posts_viewed)

    try:
        pid = random.choice(list(pids))
        pid = pid.pk

        return redirect(reverse("posts:post_generation_page", kwargs={"pid": pid}))

    except:
        return render(request, "pages/home.html")


def posts_view(request, pid):
    post_ = Post_Model.objects.get(pk=pid)
    options_ = post_.options_model_set.all()

    ##to directly show results if user has already voted!
    ## Remove later as user should not even see posts that has already been interacted with
    # if post_.viewed_by.filter(username=request.user.username).exists():
    #     #display results
    #     return results_view(request, pid)

    if request.method == "POST":
        try:
            selected_choice = post_.options_model_set.get(pk=request.POST["option"])
        except (KeyError, Options_Model.DoesNotExist):
            print("error")
            messages.error(request, "Select an option to submit!")
            contents = {"post": post_, "options": options_, "display_result": False}
            return render(request, "pages/post_home.html", contents)

        selected_choice.votes += 1
        selected_choice.chosen_by.add(request.user)
        selected_choice.save()

        post_.viewed_by.add(request.user)
        post_.save()

        # display results
        return results_view(request, pid)

    contents = {"post": post_, "options": options_, "display_result": False}
    return render(request, "pages/post_home.html", contents)


def results_view(request, pid):
    post_ = Post_Model.objects.get(pk=pid)
    options_ = post_.options_model_set.all()

    contents = {"post": post_, "options": options_, "display_result": True}

    return render(request, "pages/post_home.html", contents)
