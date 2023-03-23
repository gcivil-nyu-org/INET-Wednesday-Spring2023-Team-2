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
from django.contrib.auth.hashers import make_password, check_password

from .forms import LoginForm
from .forms import RegisterForm
from .forms import PasswordResetForm
from .forms import PasswordChangeForm, ProfilePicForm
from .forms import PasswordResetConfirmationForm
from .tokens import account_activation_token, password_reset_token
from .models import Custom_User


from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view


from django.contrib.auth.decorators import login_required


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# Create your views here.

# put token generator in a single function and call it function


# to reset password after clickin on link in eamil
def password_reset_view(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user_ = Custom_User.objects.get(pk=uid)
    except:
        user_ = None

    if user_ != None and password_reset_token.check_token(user_, token):
        password_reset_form = PasswordResetForm()
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)

            if password_reset_form.is_valid():
                if (
                    make_password(password_reset_form.cleaned_data["password1"])
                    == user_.password
                ):
                    messages.error(
                        request, "New Password cannot be the same as old one!"
                    )
                    contents = {"form": password_reset_form}
                    return render(request, "pages/password_reset.html", contents)

                user_.set_password(password_reset_form.cleaned_data["password1"])
                user_.save()

                messages.success(request, f"Password Reset! Login to proceed")
                return redirect(reverse("account:login_page"))
            else:
                for err in list(password_reset_form.errors.values()):
                    messages.error(request, err)
                password_reset_form = PasswordResetForm(request.POST)

        contents = {"form": password_reset_form}
        return render(request, "pages/password_reset.html", contents)

    messages.error(request, f"Invalid Link!!")
    return redirect(reverse("account:login_page"))


# fucntion to send eamil for account verf and reset password
def email_token(request, user_, email_subject, text_, token_, reverse_link):
    uid = (urlsafe_base64_encode(force_bytes(user_.pk)),)
    token = token_.make_token(user_)
    password_reset_link = request.build_absolute_uri(
        reverse(reverse_link, kwargs={"uid": uid[0], "token": token})
    )

    email_msg = f"Hello {user_.username},\n\nPlease click the following link to {text_}:\n{password_reset_link}"

    try:
        send_mail(
            subject=email_subject,
            message=email_msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_.email],
        )
    except:
        return 0

    return 1


# to send password link in mail
def password_reset_confirmation_view(request):
    password_reset_form = PasswordResetConfirmationForm()
    if request.method == "POST":
        username_email = request.POST["username_or_email"]
        try:
            user_ = Custom_User.objects.get(username=username_email)
        except:
            try:
                user_ = Custom_User.objects.get(email=username_email)
            except:
                messages.error(request, f"Username or Email doesn't exist!")
                contents = {"form": password_reset_form}
                return render(
                    request, "pages/password_reset_confirmation.html", contents
                )

        # send token mail
        email_subject = "Password Reset"
        text_ = "reset your password"
        token_ = password_reset_token
        reverse_link = "account:passwordreset_page"

        if email_token(request, user_, email_subject, text_, token_, reverse_link):
            messages.success(
                request, "Password Reset Link set via email. Reset Password to Login"
            )
            # return maybe redirect to home? or login?

        else:
            messages.error(request, "Error sending email!")
            password_reset_form = PasswordResetConfirmationForm(request.POST)

    contents = {"form": password_reset_form}
    return render(request, "pages/password_reset_confirmation.html", contents)


# To authenticate user and email and is_activate = True
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
        return redirect(reverse("account:login_page"))

    messages.error(request, f"Invalid Link!!")
    return redirect(reverse("account:login_page"))


# log out a logged in user
def logout_view(request):
    logout(request)
    return redirect(reverse("posts:home_page"))


# comprises of both login_view and register_view
def access_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    # print(request.POST.get('next'))
    # print("kk:", request.GET.get('next'))

    access_info_d = {"Sign In": login_view, "Sign Up": register_view}

    if request.method == "POST":
        return access_info_d[request.POST["access_info"]](
            request, login_form, register_form
        )

    contents = {"login_form": login_form, "register_form": register_form, "class_": ""}
    return render(request, "pages/login.html", contents)


# log in a user
def login_view(request, login_form, register_form):
    login_form = AuthenticationForm(request, data=request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data["username"]
        password = login_form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("here:", reverse("posts:home_page"))
            # print(request.POST.get("next"))
            # try:
            #     redirect_url = request.GET.get('next')
            #     return redirect(request.build_absolute_uri(redirect_url))
            # except:
            return redirect(reverse("posts:home_page"))
    else:
        messages.error(request, f"Username or password is wrong.")

    contents = {"login_form": login_form, "register_form": register_form, "class_": ""}
    return render(request, "pages/login.html", contents)


# register a user
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
            return redirect(reverse("account:login_page"))
        else:
            messages.error(request, "Email verification failed!")
    else:       
        for err in list(register_form.errors.values()):
            messages.error(request, err)

    contents = {
        "login_form": login_form,
        "register_form": register_form,
        "class_": "right-panel-active",
    }
    return render(request, "pages/login.html", contents)


def profile_picture_change(request, contents):
    profile_picture_change_form = ProfilePicForm(request.POST, request.FILES)

    if profile_picture_change_form.is_valid():
        request.user.profile_picture = request.FILES.get("profile_picture")
        request.user.save()

        messages.success(request, "Profile Picture Changed Successfully!")

        contents["profile"] = request.user

    else:
        for err in list(profile_picture_change_form.errors.values()):
            messages.error(request, err)

    return render(request, "pages/profile.html", contents)


def password_change(request, contents):
    password_change_form = PasswordChangeForm(request.POST)

    if password_change_form.is_valid():
        old_password = password_change_form.cleaned_data["old_password"]

        if authenticate(request, username=request.user.username, password=old_password):
            if old_password == password_change_form.cleaned_data["password1"]:
                messages.error(request, "New Password cannot be the same as old one!")
                contents["class_"] = "right-panel-active"
                return render(request, "pages/profile.html", contents)

            request.user.set_password(password_change_form.cleaned_data["password1"])
            request.user.save()
            messages.success(request, "Password Changed Successfully!")
            login(request, request.user)
            # contents = {"password_change_form": password_change_form, "class_": ""}
            # contents['username'] = request.user.username
            # contents['email'] = request.user.email
            # contents['edit_access'] = True
            return render(request, "pages/profile.html", contents)
        else:
            messages.error(request, f"Current Password is wrong")
            contents["class_"] = "right-panel-active"
    else:
        for err in list(password_change_form.errors.values()):
            messages.error(request, err)
        contents["class_"] = "right-panel-active"

    return render(request, "pages/profile.html", contents)



def profile_page_contents(request, username_):
    password_change_form = PasswordChangeForm()
    profile_picture_change_form = ProfilePicForm()
    contents = {
        "password_change_form": password_change_form,
        "profile_picture_change_form": profile_picture_change_form,
        "class_": "",
    }

    if request.user.username == username_:
        # my_user_details = Custom_User.objects.get(username = request.user.username)
        # contents['username'] = request.user.username
        # contents['email'] = request.user.email
        contents["profile"] = request.user
        contents["edit_access"] = True
    else:
        requested_user_details = Custom_User.objects.get(username=username_)
        # contents['username'] = requested_user_details.username
        # contents['email'] = requested_user_details.email
        contents["profile"] = requested_user_details
        contents["edit_access"] = False

    return contents


@login_required
def profile_view(request, username_):
    contents = profile_page_contents(request, username_)

    print(request.user.profile_picture.url)
    if request.user.username == username_ and request.method == "POST":
        func_map = {
            "profile_pic": profile_picture_change,
            "pass_change": password_change,
        }
        return func_map[request.POST["account_info"]](request, contents)
    
    contents["tab_to_click"] = "nav-profile-tab"

    return render(request, "pages/profile.html", contents)


## Change all classes to smthng like this and pass a parameter and render post_home.html and check in html to render the right page
class UserHistory(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'profile_list.html'

    renderer_classes = [TemplateHTMLRenderer]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, username_):
        if is_ajax(request):
            print("ajax request")

            user_ = Custom_User.objects.get(username=username_)
            content = user_.posts_view_time.all().order_by(
                "-view_time"
            )  # .order_by('-view_time') order by relation field here
            # print(content)
            return Response({"posts": content}, template_name="pages/profile_history.html")
        
        else:
            # print("url request")
            contents = profile_page_contents(request, username_)

            contents["tab_to_click"] = "nav-history-tab"
            return Response(contents, template_name="pages/profile.html")


class UserPostsCreated(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, username_):
        
        if is_ajax(request):
            # print("ajax request")
            user_ = Custom_User.objects.get(username=username_)
            content = user_.posts_created.all().order_by(
                "-created_time"
            )  # .order_by('-view_time') order by relation field here

            return Response(
                {"posts": content}, template_name="pages/profile_posts_created.html"
            )

        else:
            ## render entire profile page with active nav id
            # print("url request")
            contents = profile_page_contents(request, username_)

            contents["tab_to_click"] = "nav-postscreated-tab"
            return Response(contents, template_name="pages/profile.html")





class CurrentProfileURL(APIView):

    renderer_classes = [JSONRenderer]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, username, page):
        url_page_map = {'history': 'account:profile_history_page', 
                        'posts_created': 'account:profile_postscreated_page', 
                        'profile': 'account:profile_page'}
        current_url = request.build_absolute_uri(
            reverse(url_page_map[page], kwargs={"username_": username})
        )
        content = {"current_url": current_url}
        # print(content)
        return Response(content)

