from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .forms import LoginForm
from .forms import RegisterForm



# Create your views here.

def logout_view(request):
    logout(request)
    return redirect(reverse('home_page')) 



def login_view(request):
    my_form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('home_page'))
        else:
            messages.error(request, f"username or password is wrong")

    contents = {'form': my_form}
    return render(request, "pages/login.html", contents)


def register_view(request):
    my_form = RegisterForm()
    if request.method == 'POST':
        my_form = RegisterForm(request.POST)
        if my_form.is_valid():
            data_ = my_form.cleaned_data
            email_subject = "Verification"
            email_msg = f"Hello {data_['username']}"
            try:
                send_mail(
                    subject = email_subject,
                    message = email_msg,
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [data_['email']]
                )
            except:
                messages.error(request, "Email verification failed!")
                my_form = RegisterForm(request.POST)
                contents = {'form': my_form}
                return render(request, "pages/register.html", contents)
                
            user_obj = my_form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()

            messages.success(request, "Registration Successfull, Verify Email to Login")

            my_form = RegisterForm()

        else:
            for err in list(my_form.errors.values()):
                messages.error(request, err)
            my_form = RegisterForm(request.POST)
    
    contents = {'form': my_form}
    return render(request, "pages/register.html", contents)