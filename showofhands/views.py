from django.shortcuts import redirect
from django.urls import reverse


#redirect to home
def redirect_to_home_view(request):
    return redirect(reverse('posts:home_page'))