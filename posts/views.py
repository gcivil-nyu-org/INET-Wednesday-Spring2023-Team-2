from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.template import loader
from django.views import View

from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view


import random



from .models import Post_Model, Options_Model, Comments_Model
from .forms import CommentsForm
from login.models import Custom_User


#use rest-framework.APIView
#restrict api urls from being accessed
#need to do ajax implementation for other urls (notification, profile, chat)
#comment revealed after result voting
#make an api return func to give polls and once next or home ot polls is clicked, ajax calls this func to get the next poll

# Create your views here.

current_pid = None

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_random_pid():
    pids = Post_Model.objects.all()


    ##to check if user has alread seen/ interaacted with the post
    # if request.user.is_authenticated:
    #     user_posts_viewed = request.user.posts_viewed.all()
    #     pids = pids.difference(user_posts_viewed)

    try:
        pid = random.choice(list(pids))
        pid = pid.pk

        return (pid, True)

    except:
        return (None, False)


# home page - will generate random post id that user hasn't interacted with to display for user - will change to empty later in urls
# generate id and redirect/reverse with that parameter
def home_view(request):
    global current_pid

    pid, truth = get_random_pid()

    if truth:
        current_pid = pid
        return redirect(reverse("posts:post_generation_page", kwargs={"pid": pid}))
    else:
        return render(request, "pages/posts_home.html")


# def posts_view(request, pid, call="noapi"):
    # post_ = Post_Model.objects.get(pk=pid)
    # options_ = post_.options_model_set.all()

    # ##to directly show results if user has already voted!
    # ## Remove later as user should not even see posts that has already been interacted with
    # # if post_.viewed_by.filter(username=request.user.username).exists():
    # #     #display results
    # #     return results_view(request, pid)

    # if request.method == "POST":
    #     try:
    #         selected_choice = post_.options_model_set.get(pk=request.POST["option"])
    #     except (KeyError, Options_Model.DoesNotExist):
    #         print("error")
    #         messages.error(request, "Select an option to submit!")
            
    #         template = loader.get_template("pages/poll_disp.html")
    #         post_ = Post_Model.objects.get(pk=pid)
    #         options_ = post_.options_model_set.all()
    #         contents = {"post": post_, "options": options_, "display_result": False}
    #         return HttpResponse(template.render(contents, request))
            
    #         # else:
    #         #     template = loader.get_template("pages/poll_disp.html")
    #         #     post_ = Post_Model.objects.get(pk=pid)
    #         #     options_ = post_.options_model_set.all()
    #         #     contents = {"post": post_, "options": options_, "display_result": False}
    #         #     return HttpResponse(template.render(contents, request))
    #         #     # contents = {"post": post_, "options": options_, "display_result": False}
    #         #     # return render(request, "pages/posts_home.html", contents)

    #     selected_choice.votes += 1
    #     selected_choice.chosen_by.add(request.user)
    #     selected_choice.save()

    #     post_.viewed_by.add(request.user)
    #     post_.save()

    #     # display results
    #     return results_view(request, pid)

    # contents = {"post": post_, "options": options_, "display_result": False}
    # return render(request, "pages/posts_home.html", contents)

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


    ##use this to get user's choice and color code the username in comments to match the choice!
    # user_choice = post_.options_model_set.get(chosen_by=request.user)
    # user_color = user_choice.color
    # print(user_choice, user_color)
    
    return HttpResponse(template.render(contents, request))


    # return render(request, "pages/posts_home.html", contents)


##api view
## once next button is clicked, it goes to test1func and u call post view from here with random pid and call="api"
# def test1_view(request):
    # return JsonResponse({'hello': 'world'})
    # print(request, request.GET['hello'])
    # template = loader.get_template("pages/poll_disp.html")
    # post_ = Post_Model.objects.all()
    # post_ = Post_Model.objects.get(pk=1)
    # options_ = post_.options_model_set.all()
    # contents = {"post": post_, "options": options_, "display_result": False}
    # return HttpResponse(template.render(contents, request))

# shows whether you have voted or not
# if voted, then results. if not, poll
def show_curr_post_api_view(request):
    global current_pid

    pid = current_pid
    post_view_class = PostsView()
    if request.method == 'GET':
        return post_view_class.get(request=request, pid=pid, call="api")
    return post_view_class.post(request=request, pid=pid, call="api")
    

#put ajax in poll_disp.html

class PostsView(View):
    def get(self, request, pid, call="noapi"):
        global current_pid

        current_pid = pid
        post_ = Post_Model.objects.get(pk=pid)
        options_ = post_.options_model_set.all()

        if call == "noapi":
            contents = {"post": post_, "options": options_, 'pid': pid}
            return render(request, "pages/posts_home.html", contents)
        
        if post_.viewed_by.filter(username=request.user.username).exists():
            #display results
            return results_view(request, pid)
        
        template = loader.get_template("pages/poll_disp.html")
        contents = {"post": post_, "options": options_, 'pid': pid}
        return HttpResponse(template.render(contents, request))
    
    def post(self, request, pid, call="noapi"):
        if is_ajax(request):
            post_ = Post_Model.objects.get(pk=pid)
            try:
                selected_choice = post_.options_model_set.get(pk=request.POST["option"])
            except (KeyError, Options_Model.DoesNotExist):
                print("error")
                messages.error(request, "Select an option to submit!")
                return JsonResponse({'voting': 'Wrong request, nope'}) 
                

            selected_choice.votes += 1
            selected_choice.chosen_by.add(request.user)
            selected_choice.save()

            post_.viewed_by.add(request.user)
            post_.save()
            return JsonResponse({'voting': 'success'})
        return JsonResponse({'voting': 'Wrong request tt'})


# def posts_view(request, pid, call="noapi"):
#     post_ = Post_Model.objects.get(pk=pid)
#     options_ = post_.options_model_set.all()

#     ##to directly show results if user has already voted!
#     ## Remove later as user should not even see posts that has already been interacted with
#     # if post_.viewed_by.filter(username=request.user.username).exists():
#     #     #display results
#     #     return results_view(request, pid)

#     if request.method == "POST" and is_ajax(request):
#         try:
#             selected_choice = post_.options_model_set.get(pk=request.POST["option"])
#         except (KeyError, Options_Model.DoesNotExist):
#             print("error")
#             messages.error(request, "Select an option to submit!")
#             return
            
#             # template = loader.get_template("pages/poll_disp.html")
#             # post_ = Post_Model.objects.get(pk=pid)
#             # options_ = post_.options_model_set.all()
#             # contents = {"post": post_, "options": options_, 'pid': pid}
#             # # return HttpResponse(template.render(contents, request))
#             # return JsonResponse({'voting': 'Failed!'})
            

#         selected_choice.votes += 1
#         selected_choice.chosen_by.add(request.user)
#         selected_choice.save()

#         post_.viewed_by.add(request.user)
#         post_.save()

#         # display results
#         # return results_api_view(request, pid, call="api")
#         return JsonResponse({'voting': 'success'})
    
#     elif request.method == 'POST':
#         return JsonResponse({'voting': 'success'})
    
#     if call == "noapi":
#         print("Hello")
#         contents = {"post": post_, "options": options_, 'pid': pid}
#         return render(request, "pages/post_home.html", contents)
    
#     template = loader.get_template("pages/poll_disp.html")
#     contents = {"post": post_, "options": options_, 'pid': pid}
#     return HttpResponse(template.render(contents, request))


def show_next_post_api_view(request):
    global current_pid
    pid, truth = get_random_pid()

    if truth:
        post_view_class = PostsView()
        current_pid = pid
        if request.method == 'GET':
            return post_view_class.get(request=request, pid=pid, call="api")
        return post_view_class.post(request=request, pid=pid, call="api")
    
    else:
        ## need to implement an empty template to say you have reached the end! and pass a httpresponse here
        pass



# def get_current_url_api_view(request):
#     if request.method == 'GET':
#         pid = current_pid
#         current_url = request.build_absolute_uri(reverse("posts:post_generation_page", kwargs={"pid": pid}))
#         return JsonResponse({'current_url': current_url})






class CurrentPostURL(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'profile_list.html'

    renderer_classes = [JSONRenderer]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        pid = current_pid
        current_url = request.build_absolute_uri(reverse("posts:post_generation_page", kwargs={"pid": pid}))
        content = {'current_url': current_url}
        return Response(content)
    



##to show comments
class CommentsView(View):

    def post(self, request):
        if is_ajax(request):
            pid = current_pid
            post_ = Post_Model.objects.get(pk=pid)
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_ = comments_form.save(commit=False)
                comments_.question = post_
                comments_.commented_by = request.user
                comments_.save()
                return JsonResponse({'commment': 'success'})
        
            # comment_text = request.POST["comment_text"].cleaned_data()

    ## Maybe sort and feed here
    def get(self, request):
        pid = current_pid
        post_ = Post_Model.objects.get(pk=pid)
        # comments_ = post_.comments_model_set.get(pk=pid)
        comments_ = post_.comments_model_set.all()
        template = loader.get_template("pages/comments.html")
        contents = {'comments': comments_, 'show_comments_text': False}
        if post_.viewed_by.filter(username=request.user.username).exists():
            contents['show_comments_text'] = True
        return HttpResponse(template.render(contents, request))
    


def show_comments_text_api(request):
    if request.method == "GET":
        pid = current_pid
        post_ = Post_Model.objects.get(pk=pid)
        comments_form = CommentsForm()

        contents = {'comments_form': comments_form, 'show_comments_text': False}
        if post_.viewed_by.filter(username=request.user.username).exists():
            contents['show_comments_text'] = True

        template = loader.get_template("pages/comments_text.html")
        return HttpResponse(template.render(contents, request))
    



# @api_view(["GET"])
# def get_user_history(request):
#     if is_ajax(request):
#         return



        
        




    
