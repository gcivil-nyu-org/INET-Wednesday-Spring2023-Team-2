from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .forms import LoginForm
from .forms import RegisterForm
from .forms import PasswordResetForm
from .forms import PasswordResetConfirmationForm
from .tokens import account_activation_token, password_reset_token
from .models import Custom_User


# Create your views here.

#put token generator in a single function and call it function


#to reset password after clickin on link in eamil
def password_reset_view(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user_ = Custom_User.objects.get(pk=uid)
    except:
        user_ = None

    if user_ != None and password_reset_token.check_token(user_, token):
        password_reset_form = PasswordResetForm()
        if request.method == 'POST':
            password_reset_form = PasswordResetForm(request.POST)

            if password_reset_form.is_valid():
                user_.set_password(password_reset_form.cleaned_data["password1"])
                print(password_reset_form.cleaned_data['password1'])
                user_.save()

                messages.success(request, f"Password Reset! Login to proceed")
                return redirect(reverse('account:login_page'))
            else:
                for err in list(password_reset_form.errors.values()):
                    messages.error(request, err)
                password_reset_form = PasswordResetForm(request.POST)
        
        contents = {'form': password_reset_form}
        return render(request, "pages/password_reset.html", contents)
    
    messages.error(request, f"Invalid Link!!")
    return redirect(reverse('account:login_page'))




#to send password link in mail
def password_reset_confirmation_view(request):
    password_reset_form = PasswordResetConfirmationForm()
    if request.method == 'POST':
        username_email = request.POST['username_or_email']
        try:
            user_ = Custom_User.objects.get(username=username_email)
            email_ = user_.email
        except:
            try:
                user_ = Custom_User.objects.get(email=username_email)
                email_ = user_.email
            except:
                messages.error(request, f"Username or Email doesn't exist!")
                contents = {'form': password_reset_form}
                return render(request, "pages/password_reset_confirmation.html", contents)
        print(user_.username, email_)
        
        #send token mail
        email_subject = "Password Reset"
        uid = urlsafe_base64_encode(force_bytes(user_.pk)),
        token = password_reset_token.make_token(user_)
        password_reset_link = request.build_absolute_uri(reverse('account:passwordreset_page', kwargs={'uid': uid[0], 'token': token}))

        email_msg = f"Hello {user_.username},\n\nPlease click the following link to reset your password:\n{password_reset_link}"
        
        try:
            send_mail(
                subject = email_subject,
                message = email_msg,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [email_]
            )
        except:
            messages.error(request, "Error sending email!")
            password_reset_form = PasswordResetConfirmationForm(request.POST)
            contents = {'form': password_reset_form}
            return render(request, "pages/password_reset_confirmation.html", contents)

        messages.success(request, "Password Reset Link set via email. Reset Password to Login")
        # return maybe redirect to home? or login?


    contents = {'form': password_reset_form}
    return render(request, "pages/password_reset_confirmation.html", contents)




#To authenticate user and email and is_activate = True
def activate_view(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user_ = Custom_User.objects.get(pk=uid)
    except:
        user_ = None

    if user_ != None and account_activation_token.check_token(user_, token):
        user_.is_active = True
        user_.save()
        messages.success(request, f"Email Verified! Login to proceed")
        return redirect(reverse('account:login_page'))

    messages.error(request, f"Invalid Link!!")
    return redirect(reverse('account:login_page'))


#log out a logged in user
def logout_view(request):
    logout(request)
    return redirect(reverse('posts:home_page')) 


#log in a user
def login_view(request):
    my_form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('posts:home_page'))
        else:
            messages.error(request, f"username or password is wrong")

    contents = {'form': my_form}
    return render(request, "pages/login.html", contents)


#register a user
def register_view(request):
    my_form = RegisterForm()
   
    if request.method == 'POST':
        my_form = RegisterForm(request.POST)
        
        if my_form.is_valid():
            user_obj = my_form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()
            
            data_ = my_form.cleaned_data
            
            email_subject = "Verification"
            uid = urlsafe_base64_encode(force_bytes(user_obj.pk)),
            token = account_activation_token.make_token(user_obj)
            email_act_link = request.build_absolute_uri(reverse('account:activate_page', kwargs={'uid': uid[0], 'token': token}))

            email_msg = f"Hello {data_['username']},\n\nPlease click the following link to activate your account:\n{email_act_link}"
            
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

            messages.success(request, "Registration Successfull, Verify Email to Login")
            return redirect(reverse('account:login_page'))

        else:
            for err in list(my_form.errors.values()):
                messages.error(request, err)
            my_form = RegisterForm(request.POST)
    
    contents = {'form': my_form}
    return render(request, "pages/register.html", contents)