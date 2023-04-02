from django.shortcuts import render
from django.http import HttpResponse
from .models import Chat_History, Connection_Model


#to check if request is form ajax
def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# Create your views here.
def chat_view(request):
    return render(request, "pages/chat.html")


# delete later
def chat_view_test(request, connection_id):
    #if connection doesn't exists (i.e. users don't know each other) or 
    # if connection is not in accepted status (i.e. users agreed to chat with each other) or 
    # if request isnot from ajax (url request not accepted)
    
    if Connection_Model.objects.filter(id=connection_id).exists() and Connection_Model.objects.filter(id=connection_id).connection_status == "Accepted": # and is_ajax(request):
        return render(request, "pages/chat_test.html", {"connection_id": connection_id})
    
    else:
        return HttpResponse("Thou Shall not Enter!!")
