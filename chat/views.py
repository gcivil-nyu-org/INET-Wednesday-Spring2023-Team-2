from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views import View

import datetime

from rest_framework.views import APIView

from django.contrib.auth.decorators import login_required

from .models import Chat_History, Connection_Model, Chat_Message, Group_Connection
from .forms import Group_Connection_Form


# to check if request is form ajax
def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# Create your views here.


def get_friends_info(request):
    connections_sent = request.user.connection_requests_sent.filter(
        connection_status="Accepted"
    )
    connections_recieved = request.user.connection_requests_received.filter(
        connection_status="Accepted"
    )
    group_connects_ = request.user.groups_in.all()
    group_connects = group_connects_[0].connection_id_for_group.filter(
        connection_status="Accepted"
    )
    for group_connect_ in group_connects_[1:]:
        group_connects = group_connects | group_connect_.connection_id_for_group.filter(
        connection_status="Accepted"
    )
    # group_connects = [group_connect.connection_id_for_group for group_connect in group_connects]

    friends = connections_sent | connections_recieved | group_connects

    # returns all connection models that has from_user = user or to_user=user
    return friends
    ## use this code to display user's friends list:
    # friends = get_friends_info(request)
    #  for i in friends:
    #      print(i.get_friend(request.user), i.id)


@login_required
def get_num_new_messages(request):
    friends = get_friends_info(request)
    friend_object = [
        (
            friend.get_friend(request.user),
            friend,
            get_chat_history(friend.id),
        )
        for friend in friends
    ]

    num_new_messages = sum(
        1
        for friend in friend_object
        if friend[2] and friend[2][len(friend[2]) - 1].user != request.user
    )

    return num_new_messages


@login_required
def chat_page(request):
    # friends = get_friends_info(request)
    # friends = friends.order_by('-latest_message_time')
    # friend_object = [
    #     (
    #         friend.get_friend(request.user),
    #         friend,
    #     )
    #     for friend in friends
    # ]

    # context = {
    #     "friends": friends,
    #     "friend_object": friend_object,
    # }

    return render(request, "pages/chat.html")


def get_chat_history(connection_id):
    try:
        chat_history = Chat_History.objects.get(
            connection=Connection_Model.objects.get(id=connection_id)
        )
    except (KeyError, Chat_History.DoesNotExist):
        return []

    history_list = chat_history.history.order_by(
        "timestamp"
        # "-timestamp"
    ).all()  # [:100] ##todo: return top 100msg everytime to reduce query time
    return history_list


def chat_history_box_view(request, connection_id):
    if (
        Connection_Model.objects.filter(id=connection_id).exists()
        and Connection_Model.objects.get(id=connection_id).connection_status
        == "Accepted"
    ) and is_ajax(request):
        messages = get_chat_history(connection_id)

        template = loader.get_template("pages/chat_box.html")
        contents = {
            "connection_id": connection_id,
            "messages": messages,
            "friend_name": Connection_Model.objects.get(id=connection_id).get_friend(
                request.user
            ),
            "friend_pic": Connection_Model.objects.get(id=connection_id)
            .get_friend(request.user)
            .profile_picture.url,
        }
        return HttpResponse(template.render(contents, request))

    else:
        return HttpResponse("Thou Shall not Enter!!")


def latest_message_formatting(message):
    if len(message) <= 20:
        return message

    return message[:20] + "..."


def get_chat_connections_list_view(request):
    if is_ajax(request):
        friends = get_friends_info(request)
        friends = friends.order_by("-latest_message_time")

        # friends = friends.order_by("-get_chat_history__latest_message_time")
        # print(friends[0].get_chat_history.all()[0].history.filter(~Q(user=request.user)).filter(~Q(seen_by__username__contains=request.user.username)).count())
        # friend_object = [
        #     (
        #         friend.get_friend(request.user),
        #         friend,
        #         friend.get_chat_history.all()[0]
        #         .history.filter(~Q(user=request.user))
        #         .filter(~Q(seen_by__username__contains=request.user.username))
        #         .count(),
        #     )
        #     for friend in friends
        # ]

        friend_object = []
        for friend in friends:
            try:
                unread_msg_count = (
                    friend.get_chat_history.history.filter(~Q(user=request.user))
                    .filter(~Q(seen_by__username__contains=request.user.username))
                    .count()
                )
                latest_message = friend.get_chat_history.history.last().message
                latest_message = latest_message_formatting(latest_message)
            except:
                unread_msg_count = 0
                latest_message = None

            friend_object.append(
                (
                    friend.get_friend(request.user),
                    friend,
                    unread_msg_count,
                    latest_message,
                )
            )

        contents = {
            "friends": friends,
            "friend_object": friend_object,
        }

        template = loader.get_template("includes/chat_connections_list.html")

        return HttpResponse(template.render(contents, request))

    else:
        return HttpResponse("Thou Shall not Enter!!")


def update_msg_seen_view(request, message_id):
    if is_ajax(request):
        message = Chat_Message.objects.get(id=message_id)

        message.seen_by.add(request.user)

        message.save()

        return HttpResponse("success")

    else:
        return HttpResponse("Thou Shall not Enter!!")


class Get_Chat_Group_Creation_View(View):
    def get(self, request):
        if is_ajax(request):
            chat_group_creation_form = Group_Connection_Form()
            contents = {"chat_group_creation_form": chat_group_creation_form}
            template = loader.get_template("pages/chat_group_creation.html")

            return HttpResponse(template.render(contents, request))
        
        else:
            return HttpResponse("Thou Shall not Enter!!")

    def post(self, request):
        if is_ajax(request):
            chat_group_creation_form = Group_Connection_Form(request.POST)
            errors_ = ""

            if chat_group_creation_form.is_valid():
                # chat_group_creation_form.group_created_by = request.user
                # try:
                #     chat_group_creation_form.save()
                # except:
                #     errors_ = ", ".join(list(chat_group_creation_form.errors.values()))
                #     print("hello", errors_)
                #     return JsonResponse({"group_creation": "fail", "errors": errors_})
                # group_ = chat_group_creation_form.save(commit=False)
                # group_.created_by = request.user
                # group_.save()

                group_ = Group_Connection.objects.create(group_created_by=request.user, 
                                                 group_name=chat_group_creation_form.cleaned_data["group_name"])
                group_.members.set(chat_group_creation_form.cleaned_data["members"])
                
                # group_connection_model = Group_Connection.objects.get(group_name=chat_group_creation_form["group_name"])
                try:
                    Connection_Model.objects.create(group=group_)
                except Exception as e:
                    print("hi", e)
                    return JsonResponse({"group_creation": "fail", "errors": str(e)})

            else:
                errors_ = ", ".join(list(chat_group_creation_form.errors.values()))
                print("how", errors_)
                return JsonResponse({"group_creation": "fail", "errors": errors_})
            
            return JsonResponse({"group_creation": "success", "errors": errors_})

        else:
            return HttpResponse("Thou Shall not Enter!!")
        


# def get_chat_group_creation_view(request):
#     if is_ajax(request):
#         chat_group_creation_form = Group_Connection_Form()
#         contents = {"chat_group_creation_form": chat_group_creation_form}

#         template = loader.get_template("pages/chat_group_creation.html")

#         return HttpResponse(template.render(contents, request))