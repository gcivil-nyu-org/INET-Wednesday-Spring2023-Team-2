from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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


#fucntion to send eamil for account verf and reset password
def email_token(request, user_, email_subject, text_, token_, reverse_link):
    uid = urlsafe_base64_encode(force_bytes(user_.pk)),
    token = token_.make_token(user_)
    password_reset_link = request.build_absolute_uri(reverse(reverse_link, kwargs={'uid': uid[0], 'token': token}))

    email_msg = f"Hello {user_.username},\n\nPlease click the following link to {text_}:\n{password_reset_link}"

    try:
        send_mail(
            subject = email_subject,
            message = email_msg,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [user_.email]
        )
    except:
        return 0
    
    return 1



#to send password link in mail
def password_reset_confirmation_view(request):
    password_reset_form = PasswordResetConfirmationForm()
    if request.method == 'POST':
        username_email = request.POST['username_or_email']
        try:
            user_ = Custom_User.objects.get(username=username_email)
        except:
            try:
                user_ = Custom_User.objects.get(email=username_email)
            except:
                messages.error(request, f"Username or Email doesn't exist!")
                contents = {'form': password_reset_form}
                return render(request, "pages/password_reset_confirmation.html", contents)
        
        #send token mail
        email_subject = "Password Reset"
        text_ = "reset your password"
        token_ = password_reset_token
        reverse_link = "account:passwordreset_page"
        
        if email_token(request, user_, email_subject, text_, token_, reverse_link):
            messages.success(request, "Password Reset Link set via email. Reset Password to Login")
            # return maybe redirect to home? or login?

        else:
            messages.error(request, "Error sending email!")
            password_reset_form = PasswordResetConfirmationForm(request.POST)
            

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



#comprises of both login_view and register_view
def access_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    access_info_d = {'Sign In': login_view, 'Sign Up': register_view}

    if request.method == 'POST':
        return access_info_d[request.POST['access_info']](request, login_form, register_form)
    
    contents = {'login_form': login_form, 'register_form': register_form, 'class_': ""}
    return render(request, "pages/login.html", contents)



#log in a user
def login_view(request, login_form, register_form):
    login_form = AuthenticationForm(request, data=request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('posts:home_page'))
    else:
        messages.error(request, f"Username or password is wrong.")
    
    contents = {'login_form': login_form, 'register_form': register_form, 'class_': ""}
    return render(request, "pages/login.html", contents)


#register a user
def register_view(request, login_form, register_form):
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        user_ = register_form.save(commit=False)
        user_.is_active = False
        user_.save()
        
        # send email token
        email_subject = "Verification"
        text_ = "activate your account"
        token_ = account_activation_token
        reverse_link = "account:activate_page"
        
        if email_token(request, user_, email_subject, text_, token_, reverse_link):
            messages.success(request, "Registration successful, verify email to login.")
            return redirect(reverse('account:login_page'))
        else:
            messages.error(request, "Email verification failed!")
    else:
        for err in list(register_form.errors.values()):
            messages.error(request, err)

    contents = {'login_form': login_form, 'register_form': register_form, 'class_': "right-panel-active"}
    return render(request, "pages/login.html", contents)
