from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views import View

from login.views import get_user_friends_list


import datetime

from rest_framework.views import APIView

from django.contrib.auth.decorators import login_required

from .models import Chat_History, Connection_Model, Chat_Message, Group_Connection
from login.models import Custom_User
from .forms import Group_Connection_Form


# to check if request is form ajax
def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# Create your views here.


class SearchFriendsView(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("search", "")

        search_results = []

        if query:
            friends = get_user_friends_list(request.user)
            user_results = Custom_User.objects.filter(
                Q(
                    id__in=[
                        friend.to_user.id
                        for friend in friends
                        if friend.from_user == request.user
                    ]
                    + [
                        friend.from_user.id
                        for friend in friends
                        if friend.to_user == request.user
                    ]
                )
                & Q(username__icontains=query)
            ).distinct()

            for user in user_results:
                connection = (
                    Connection_Model.objects.filter(
                        from_user=user,
                        to_user=request.user,
                        connection_status="Accepted",
                    ).first()
                    or Connection_Model.objects.filter(
                        from_user=request.user,
                        to_user=user,
                        connection_status="Accepted",
                    ).first()
                )

                search_results.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "connection_id": connection.id,
                        "type": "user",
                    }
                )

            group_results = Group_Connection.objects.filter(
                Q(members__id=request.user.id) & Q(group_name__icontains=query)
            ).distinct()

            for group in group_results:
                connection = group.connection_id_for_group
                search_results.append(
                    {
                        "id": group.id,
                        "group_name": group.group_name,
                        "group_id": group.id,
                        "connection_id": connection.id,
                        "type": "group",
                    }
                )

        return JsonResponse({"search_results": search_results})


def get_friends_info(request):
    connections_sent = request.user.connection_requests_sent.filter(
        connection_status="Accepted"
    )
    connections_recieved = request.user.connection_requests_received.filter(
        connection_status="Accepted"
    )
    group_connects = request.user.groups_in.all().values_list(
        "connection_id_for_group", flat=True
    )
    group_connects = Connection_Model.objects.filter(
        connection_status="Accepted", id__in=group_connects
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

        connection = Connection_Model.objects.get(id=connection_id)

        is_group = False
        if connection.group:
            is_group = True

        template = loader.get_template("pages/chat_box.html")
        contents = {
            "connection_id": connection_id,
            "messages": messages,
            "friend_name": connection.get_friend(request.user),
            "friend_pic": connection.get_friend(request.user).profile_picture.url,
            "is_group": is_group,
            "connection": connection,
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
        friend_object = []
        has_unread_messages = False

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
                latest_message = ""

            if unread_msg_count:
                has_unread_messages = True

            friend_object.append(
                (
                    friend.get_friend(request.user),
                    friend,
                    unread_msg_count,
                    latest_message,
                )
            )

        request.user.has_unread_messages = has_unread_messages
        request.user.save()

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
    def get(self, request, connection_id):
        if is_ajax(request):
            friends = get_user_friends(request.user)
            chat_group_creation_form = Group_Connection_Form(friends=friends)
            if int(connection_id):
                group_ = Connection_Model.objects.get(id=connection_id).group
                chat_group_creation_form = Group_Connection_Form(instance=group_, friends=friends)

            contents = {
                "chat_group_creation_form": chat_group_creation_form,
                "connection_id": connection_id,
            }
            template = loader.get_template("pages/chat_group_creation.html")

            return HttpResponse(template.render(contents, request))

        else:
            return HttpResponse("Thou Shall not Enter!!")

    def post(self, request, connection_id):
        if is_ajax(request):
            chat_group_creation_form = Group_Connection_Form(
                request.POST, request.FILES
            )
            errors_ = ""
            form_reset = True
            group_ = None
            if int(connection_id):
                print("here")
                form_reset = False
                group_ = Connection_Model.objects.get(id=connection_id).group
                chat_group_creation_form = Group_Connection_Form(
                    request.POST, instance=group_
                )
            else:
                connection_id = None

            if chat_group_creation_form.is_valid():
                try:
                    if group_:
                        group_.group_name = chat_group_creation_form.cleaned_data[
                            "group_name"
                        ]
                        if request.FILES.get("profile_picture"):
                            group_.profile_picture = request.FILES.get(
                                "profile_picture"
                            )
                        members = list(chat_group_creation_form.cleaned_data["members"])
                        members.append(request.user)
                        group_.members.set(members)
                        group_.save()

                    else:
                        group_ = Group_Connection.objects.create(
                            group_created_by=request.user,
                            group_name=chat_group_creation_form.cleaned_data[
                                "group_name"
                            ],
                        )
                        if request.FILES.get("profile_picture"):
                            group_.profile_picture = request.FILES.get(
                                "profile_picture"
                            )
                        members = list(chat_group_creation_form.cleaned_data["members"])
                        members.append(request.user)
                        group_.members.set(members)
                        group_.save()
                except Exception as e:
                    return JsonResponse(
                        {
                            "group_creation": "fail",
                            "errors": str(e),
                            "form_reset": form_reset,
                            "connection_id": connection_id,
                        }
                    )

                # group_connection_model = Group_Connection.objects.get(group_name=chat_group_creation_form["group_name"])
                try:
                    if form_reset:
                        Connection_Model.objects.create(group=group_)
                except Exception as e:
                    return JsonResponse(
                        {
                            "group_creation": "fail",
                            "errors": str(e),
                            "form_reset": form_reset,
                            "connection_id": connection_id,
                        }
                    )

            else:
                print(chat_group_creation_form.errors.values())
                errors_ = ", ".join(list(chat_group_creation_form.errors.values())[0])
                print("how", errors_)
                return JsonResponse(
                    {
                        "group_creation": "fail",
                        "errors": errors_,
                        "form_reset": form_reset,
                        "connection_id": connection_id,
                    }
                )

            return JsonResponse(
                {
                    "group_creation": "success",
                    "errors": errors_,
                    "form_reset": form_reset,
                    "connection_id": connection_id,
                }
            )

        else:
            return HttpResponse("Thou Shall not Enter!!")


def delete_group_view(request, connection_id):
    if is_ajax(request):
        group_ = Connection_Model.objects.get(id=connection_id).group
        group_.delete()
        return JsonResponse({"delete": "success", "message": f"{group_} Terminated!"})
    else:
        return HttpResponse("Thou Shall not Enter!!")


def exit_group_view(request, connection_id):
    if is_ajax(request):
        group_ = Connection_Model.objects.get(id=connection_id).group
        group_.members.remove(request.user)
        group_.save()
        return JsonResponse(
            {"delete": "success", "message": f"{group_} wishes you Farewell!"}
        )
    else:
        return HttpResponse("Thou Shall not Enter!!")


##TODO: Delete ONLY IF model idea works
# def get_unread_messages_count(request):
#     friends = get_friends_info(request)
#     unread_msg_count = (
#         friend.get_chat_history.history.filter(~Q(user=request.user))
#         .filter(~Q(seen_by__username__contains=request.user.username))
#         .count()
#     )


def add_message_notification_view(request):
    if is_ajax(request):
        # print(request.user.has_unread_messages)
        if request.user.is_authenticated and request.user.has_unread_messages:
            return JsonResponse({"pending": "true"})
        return JsonResponse({"pending": "false"})
    else:
        return HttpResponse("Thou Shall not Enter!!")


def update_user_pending_status_view(request):
    if is_ajax(request):
        request.user.has_unread_messages = True
        request.user.save()
        return JsonResponse({"pending": "true"})
    else:
        return HttpResponse("Thou Shall not Enter!!")


def get_user_friends(user):
    friends = (
        Custom_User.objects.filter(
            Q(connection_requests_received__from_user=user)
            & Q(connection_requests_received__connection_status="Accepted")
        )
        | Custom_User.objects.filter(
            Q(connection_requests_sent__to_user=user)
            & Q(connection_requests_sent__connection_status="Accepted")
        )
    ).distinct()

    return friends
