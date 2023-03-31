from django.shortcuts import render


# Create your views here.
def chat_view(request):
    return render(request, "pages/chat.html")
