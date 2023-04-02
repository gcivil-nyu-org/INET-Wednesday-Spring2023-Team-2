from django.shortcuts import render


# Create your views here.
def chat_view(request):
    return render(request, "pages/chat.html")


# delete later
def chat_view_test(request, connection_id):
    return render(request, "pages/chat_test.html", {"connection_id": connection_id})
