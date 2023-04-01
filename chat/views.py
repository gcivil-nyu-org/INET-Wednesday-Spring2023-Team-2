from django.shortcuts import render


# Create your views here.
def chat_view(request):
    return render(request, "pages/chat.html")


#delete later
def chat_view_test(request, chat_box_name):
    return render(request, "pages/chat_test.html", {"chat_box_name": chat_box_name})
