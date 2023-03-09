from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.template import loader
import random



from .models import Post_Model, Options_Model
from login.models import Custom_User




def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#make an api return func to give polls and once next or home ot polls is clicked, ajax calls this func to get the next poll

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


# def posts_view(request, pid, call="noapi"):
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
            
            template = loader.get_template("pages/poll_disp.html")
            post_ = Post_Model.objects.get(pk=pid)
            options_ = post_.options_model_set.all()
            contents = {"post": post_, "options": options_, "display_result": False}
            return HttpResponse(template.render(contents, request))
            
            # else:
            #     template = loader.get_template("pages/poll_disp.html")
            #     post_ = Post_Model.objects.get(pk=pid)
            #     options_ = post_.options_model_set.all()
            #     contents = {"post": post_, "options": options_, "display_result": False}
            #     return HttpResponse(template.render(contents, request))
            #     # contents = {"post": post_, "options": options_, "display_result": False}
            #     # return render(request, "pages/post_home.html", contents)

        selected_choice.votes += 1
        selected_choice.chosen_by.add(request.user)
        selected_choice.save()

        post_.viewed_by.add(request.user)
        post_.save()

        # display results
        return results_view(request, pid)

    contents = {"post": post_, "options": options_, "display_result": False}
    return render(request, "pages/post_home.html", contents)

    # template = loader.get_template("pages/poll_disp.html")
    # post_ = Post_Model.objects.get(pk=pid)
    # options_ = post_.options_model_set.all()
    # contents = {"post": post_, "options": options_, "display_result": False}
    # return HttpResponse(template.render(contents, request))



##need a json response here as post method automatically returns whatever is in this function and renders it!
def results_view(request, pid):
    post_ = Post_Model.objects.get(pk=pid)
    options_ = post_.options_model_set.all()
    contents = {"post": post_, "options": options_, 'pid': pid}
    template = loader.get_template("pages/poll_result.html")
    
    return HttpResponse(template.render(contents, request))


    # return render(request, "pages/post_home.html", contents)




##api view
## once next button is clicked, it goes to test1func and u call post view from here with random pid and call="api"
# def test1_view(request):
    # return JsonResponse({'hello': 'world'})
    # print(request, request.GET['hello'])
    template = loader.get_template("pages/poll_disp.html")
    # post_ = Post_Model.objects.all()
    post_ = Post_Model.objects.get(pk=1)
    options_ = post_.options_model_set.all()
    contents = {"post": post_, "options": options_, "display_result": False}
    return HttpResponse(template.render(contents, request))




def show_curr_post_api_view(request, pid):
    return posts_view(request, pid, call="api")
    






def posts_view(request, pid, call="noapi"):
    post_ = Post_Model.objects.get(pk=pid)
    options_ = post_.options_model_set.all()

    ##to directly show results if user has already voted!
    ## Remove later as user should not even see posts that has already been interacted with
    # if post_.viewed_by.filter(username=request.user.username).exists():
    #     #display results
    #     return results_view(request, pid)

    if request.method == "POST" and is_ajax(request):
        try:
            selected_choice = post_.options_model_set.get(pk=request.POST["option"])
        except (KeyError, Options_Model.DoesNotExist):
            print("error")
            messages.error(request, "Select an option to submit!")
            return
            
            # template = loader.get_template("pages/poll_disp.html")
            # post_ = Post_Model.objects.get(pk=pid)
            # options_ = post_.options_model_set.all()
            # contents = {"post": post_, "options": options_, 'pid': pid}
            # # return HttpResponse(template.render(contents, request))
            # return JsonResponse({'voting': 'Failed!'})
            

        selected_choice.votes += 1
        selected_choice.chosen_by.add(request.user)
        selected_choice.save()

        post_.viewed_by.add(request.user)
        post_.save()

        # display results
        # return results_api_view(request, pid, call="api")
        return JsonResponse({'voting': 'success'})
    
    elif request.method == 'POST':
        return
    
    if call == "noapi":
        contents = {"post": post_, "options": options_, 'pid': pid}
        return render(request, "pages/post_home.html", contents)
    
    template = loader.get_template("pages/poll_disp.html")
    contents = {"post": post_, "options": options_, 'pid': pid}
    return HttpResponse(template.render(contents, request))



