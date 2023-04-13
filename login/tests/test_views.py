import os
import json

from PIL import Image
from django.test import TestCase, Client
from login.models import Custom_User, validate_image_extension
from chat.models import Connection_Model
from django.core import mail
from unittest.mock import patch
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from login.forms import LoginForm
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from django.core import mail

from login.models import Custom_User
from login.tokens import account_activation_token, password_reset_token
from login.forms import (
    LoginForm,
    RegisterForm,
    PasswordChangeForm,
    PasswordResetConfirmationForm,
    PasswordResetForm,
    ProfilePicForm,
)
from login.views import (
    access_view,
    logout_view,
    activate_view,
    password_reset_confirmation_view,
    password_reset_view,
    profile_view,
    UserHistory,
    UserPostsCreated,
    email_token,
)


class TestLoginModels(TestCase):
    def test_valid_image_extensions(self):
        valid_extensions = [".jpg", ".jpeg", ".png"]

        for ext in valid_extensions:
            image = SimpleUploadedFile(
                f"test_image{ext}", b"file_content", content_type=f"image/{ext}"
            )

            try:
                validate_image_extension(image)
            except ValidationError:
                self.fail(
                    f"validate_image_extension raised ValidationError for a valid extension: {ext}"
                )

    def test_invalid_image_extensions(self):
        invalid_extensions = [".gif", ".bmp", ".tiff"]

        for ext in invalid_extensions:
            image = SimpleUploadedFile(
                f"test_image{ext}", b"file_content", content_type=f"image/{ext}"
            )

            with self.assertRaises(ValidationError):
                validate_image_extension(image)

    def test_case_insensitive_validation(self):
        valid_extensions = [".JPG", ".JPEG", ".PNG"]

        for ext in valid_extensions:
            image = SimpleUploadedFile(
                f"test_image{ext}", b"file_content", content_type=f"image/{ext.lower()}"
            )

            try:
                validate_image_extension(image)
            except ValidationError:
                self.fail(
                    f"validate_image_extension raised ValidationError for a valid case-insensitive extension: {ext}"
                )


class TestLoginForms(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="test", email="test@testemail.com", password="test1234"
        )

        self.client.login(username="test", password="test1234")

    def test_existed_emial(self):
        form = RegisterForm(
            data={
                "username": "test1",
                "email": "test@testemail.com",
                "password1": "test1234",
                "password2": "test1234",
            }
        )

        self.assertFalse(form.is_valid())


class TestLoginViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="test", password="test1234", email="test@testemail.com"
        )

        self.url = reverse("account:login_page")

    def test_login_url(self):
        url_path = "/account/login/"
        # response = self.client.get(url_path)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_success(self):
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "password": "test1234",
                "access_info": "Sign In",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # A successful login should redirect
        self.assertEqual(
            response.url, reverse("posts:home_page")
        )  # User should be redirected to the home page

    def test_login_view_failure(self):
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "password": "wrongpassword",
                "access_info": "Sign In",
            },
        )

        self.assertEqual(
            response.status_code, 200
        )  # Login failed, should render the same page
        self.assertContains(
            response, "Username or password is wrong."
        )  # Error message should be displayed

    def test_login_view_invalid_username(self):
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "invalid_user",
                "password": "test1234",
                "access_info": "Sign In",
            },
        )

        self.assertEqual(
            response.status_code, 200
        )  # Login failed, should render the same page
        self.assertContains(
            response, "Username or password is wrong."
        )  # Error message should be displayed


class TestRegisterViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_form = RegisterForm(
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "test1234",
                "password2": "test1234",
            }
        )

    def test_register_view_success(self):
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "testpasswordcs6063",
                "password2": "testpasswordcs6063",
                "access_info": "Sign Up",
            },
        )

        self.assertEqual(
            response.status_code, 302
        )  # Successful registration should redirect
        self.assertRedirects(
            response,
            reverse("account:login_page"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Custom_User.objects.filter(username="test").exists())
        self.assertEqual(len(mail.outbox), 1)

        # Check email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Verification")
        self.assertIn("activate your account", email.body)
        self.assertEqual(email.to, ["test@testemail.com"])

        # Retrieve the user
        test_user = Custom_User.objects.get(username="test")

        # Generate the activation URL
        uid = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = account_activation_token.make_token(test_user)
        url = reverse("account:activate_page", kwargs={"uid": uid, "token": token})

        # Activate the user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account:login_page"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email Verified! Login to proceed")

        # Check if the user is now active
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_active)

        # login using registration info
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "testpasswordcs6063",
                "access_info": "Sign In",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_register_view_email_verification_failed(self):
        # Register a new user
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "testpasswordcs6063",
                "password2": "testpasswordcs6063",
                "access_info": "Sign Up",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Custom_User.objects.filter(username="test").exists())

        # Retrieve the user
        test_user = Custom_User.objects.get(username="test")

        # Generate an invalid activation URL
        uid = urlsafe_base64_encode(force_bytes(test_user.pk))
        invalid_token = "invalid_token"
        url = reverse(
            "account:activate_page", kwargs={"uid": uid, "token": invalid_token}
        )

        # Attempt to activate the user with an invalid token
        response = self.client.get(url)

        # Check if the email verification failed message is displayed
        messages = list(response.wsgi_request._messages)

        self.assertEqual(str(messages[1]), "Invalid Link!!")

        # Check if the user is still inactive
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_active)

    def test_register_view_password_mismatch(self):
        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "testpasswordcs6063",
                "password2": "testwrongpasswordcs6063",
                "access_info": "Sign Up",
            },
        )

        self.assertEqual(
            response.status_code, 200
        )  # Registration failed, should render the same page
        self.assertEqual(
            Custom_User.objects.filter(username="test").count(), 0
        )  # No new user should be created

    def test_register_view_username_exists(self):
        self.user = Custom_User.objects.create_user(
            username="test", email="test@testemail.com", password="testpasswordcs6063"
        )

        response = self.client.post(
            reverse("account:login_page"),
            {
                "username": "test",
                "email": "test@testemail.com",
                "password1": "newpasswordcs6063",
                "password2": "newpasswordcs6063",
                "access_info": "Sign Up",
            },
        )

        self.assertEqual(
            response.status_code, 200
        )  # Registration failed, should render the same page
        self.assertContains(
            response, "A user with that username already exists."
        )  # Error message should be displayed


class TestLogoutViews(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testuserpasswordcs6063"
        self.user = Custom_User.objects.create_user(
            username=self.username, password=self.password
        )

        self.post = Post_Model.objects.create(
            question_text="Test question", created_by=self.user, id=1
        )
        self.option1 = Options_Model.objects.create(
            question=self.post, choice_text="option1", id=1
        )
        self.option2 = Options_Model.objects.create(
            question=self.post, choice_text="option2", id=2
        )
        self.post.viewed_by.add(self.user)
        self.post.save()
        self.option1.chosen_by.add(self.user)
        self.option1.save()

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("account:logout_page"), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("posts:home_page"))
        user_after_logout = response.client
        self.assertFalse(user_after_logout.session.get("_auth_user_id"))


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="test", email="test@testemail.com", password="test1234"
        )
        self.profile_pic = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        self.client.login(username="test", password="test1234")
        self.login_url = reverse("account:login_page")
        self.home_page_url = reverse("posts:home_page")
        self.logout_url = reverse("account:logout_page")
        self.login_form = LoginForm()
        self.register_form = RegisterForm()

    # testing profile functions:
    # view profile as user authenicated
    def test_profile_view_user_auth(self):
        response = self.client.get(reverse("account:profile_page", args=["test"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile"], self.user)
        self.assertTrue(response.context["edit_access"])
        self.assertTemplateUsed(response, "pages/profile.html")
        self.assertIsInstance(
            response.context["password_change_form"], PasswordChangeForm
        )
        self.assertIsInstance(
            response.context["profile_picture_change_form"], ProfilePicForm
        )

    # view another user profile as user authenicated
    def test_profile_view_different_user(self):
        self.user1 = Custom_User.objects.create_user(
            username="test1", email="test1@testemail.com", password="test1234"
        )
        response = self.client.get(reverse("account:profile_page", args=["test1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile"], self.user1)
        self.assertFalse(response.context["edit_access"])

    # change profile picture as user authenicated
    def test_profile_view_post_profilepic(self):
        url = reverse("account:profile_page", args=["test"])
        response = self.client.post(
            url, {"account_info": "profile_pic", "profile_picture": self.profile_pic}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Custom_User.objects.get(username=self.user.username).profile_picture.url,
            f"/media/Profile-Pictures/default-profile.jpeg",
        )

    # change password from profile as user authenicated: success
    def test_profile_view_post_passwordchange_success(self):
        url = reverse("account:profile_page", kwargs={"username_": "test"})
        response = self.client.post(
            url,
            {
                "account_info": "pass_change",
                "old_password": "test1234",
                "password1": "test4321",
                "password2": "test4321",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("test4321"))

    # change password from profile as user authenicated: fail
    def test_profile_view_post_passwordchange_fail(self):
        url = reverse("account:profile_page", kwargs={"username_": "test"})
        response = self.client.post(
            url,
            {
                "account_info": "pass_change",
                "old_password": "wrongpass",
                "password1": "test4321",
                "password2": "test4321",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Current Password is wrong" in response.content.decode())


class TestRegister(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="test", email="test@testemail.com", password="testpasstest123"
        )
        self.profile_pic = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        self.login_url = reverse("account:login_page")
        self.home_page_url = reverse("posts:home_page")
        self.logout_url = reverse("account:logout_page")
        self.password_reset_confirmation_url = reverse(
            "account:passwordresetconfirmation_page"
        )

        self.login_form = LoginForm()
        self.register_form = RegisterForm()
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    # testing activating account using email token
    #       - correct email token -> account activate & login
    #       - incorrect email token -> message invalid link
    def test_activate_view_valid_token(self):
        url = reverse(
            "account:activate_page", kwargs={"uid": self.uid, "token": self.token}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # check the message results from valid link
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email Verified! Login to proceed")

        # check user_.is_active = True
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # check user is able to log in with credientials
        self.client.login(username="test", password="testpasstest123")

    def test_activate_view_invalid_token(self):
        # added string to token to make invalid token
        url = reverse(
            "account:activate_page",
            kwargs={"uid": self.uid, "token": self.token + "abc"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # check the message results from invalid link
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Link!!")

    # testing passwordresetconfirmation page:
    #       - valid username -> email sent
    #       - valid email -> email sent
    #       - invalid username -> error message, no email sent
    #       - invalid email -> error message, no email sent
    def test_passwordresetconfirmation_view_get(self):
        response = self.client.get(self.password_reset_confirmation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset_confirmation.html")

    def test_passwordresetconfirmation_view_valid_email(self):
        response = self.client.post(
            self.password_reset_confirmation_url,
            {"username_or_email": "test@testemail.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset_confirmation.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Password Reset Link sent via email. Reset Password to Login",
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test@testemail.com"])

    def test_passwordresetconfirmation_view_valid_username(self):
        response = self.client.post(
            self.password_reset_confirmation_url, {"username_or_email": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset_confirmation.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Password Reset Link sent via email. Reset Password to Login",
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test@testemail.com"])

    def test_passwordresetconfirmation_view_invalid_email(self):
        response = self.client.post(
            self.password_reset_confirmation_url,
            {"username_or_email": "wrongtest@testemail.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset_confirmation.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Email doesn't exist!")

    def test_passwordresetconfirmation_view_invalid_username(self):
        response = self.client.post(
            self.password_reset_confirmation_url, {"username_or_email": "wrongtest"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset_confirmation.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Email doesn't exist!")

    # testing passwordresetview after clicking on a link sent to email
    #       - valid link -> password_reset_form:
    #               * password change successful
    #               * password change unsuccessful: same pass or too common
    #       - invalid link -> message
    def test_passwordreset_view_validlink_success(self):
        passreset_token = password_reset_token.make_token(self.user)
        password_reset_url = reverse(
            "account:passwordreset_page",
            kwargs={"uid": self.uid, "token": passreset_token},
        )

        response = self.client.get(password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset.html")

        response = self.client.post(
            password_reset_url, {"password1": "newtest1234", "password2": "newtest1234"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Password Reset! Login to proceed")

        self.assertTrue(self.client.login(username="test", password="newtest1234"))

    def test_passwordreset_view_validlink_unsuccess_mismatch(self):
        passreset_token = password_reset_token.make_token(self.user)
        password_reset_url = reverse(
            "account:passwordreset_page",
            kwargs={"uid": self.uid, "token": passreset_token},
        )

        response = self.client.get(password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/password_reset.html")

        response = self.client.post(
            password_reset_url,
            {"password1": "testpasstest123", "password2": "testpasstest"},
        )

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertContains(response, "The two password fields didn’t match.")

    def test_passwordreset_view_invalidlink(self):
        password_reset_url = reverse(
            "account:passwordreset_page",
            kwargs={"uid": self.uid, "token": "fake_invalid_token"},
        )

        response = self.client.get(password_reset_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Link!!")


class TestSendFriendRequest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = Custom_User.objects.create_user(
            username="testuser1", password="testpassword1"
        )

        self.user2 = Custom_User.objects.create_user(
            username="testuser2", password="testpassword2"
        )

    def test_send_friend_request_not_ajax(self):
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(
            reverse("account:send_friend_request", args=[self.user2.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "error", "message": "Not an AJAX request."},
        )

    def test_send_friend_request_new_request(self):
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse("account:send_friend_request", args=[self.user2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": f"Friend request sent to {self.user2.username}!"},
        )
        self.assertTrue(
            Connection_Model.objects.filter(
                from_user=self.user1, to_user=self.user2, connection_status="Pending"
            ).exists()
        )

    def test_send_friend_request_declined_request(self):
        # Create a declined friend request
        declined_request = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user2, connection_status="Declined"
        )

        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse("account:send_friend_request", args=[self.user2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": f"Friend request sent to {self.user2.username}!"},
        )

        declined_request.refresh_from_db()
        self.assertEqual(declined_request.connection_status, "Pending")


class TestAcceptFriendRequest(TestCase):
    def setUp(self):
        self.user1 = Custom_User.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.user2 = Custom_User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        self.friend_request = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user2
        )

    def test_accept_friend_request_success(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(
            reverse(
                "account:accept_friend_request", kwargs={"uid": self.friend_request.id}
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.connection_status, "Accepted")
        self.assertJSONEqual(response.content, {"status": "success"})

    def test_accept_friend_request_no_permission(self):
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse(
                "account:accept_friend_request", kwargs={"uid": self.friend_request.id}
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.connection_status, "Pending")
        self.assertJSONEqual(
            response.content,
            {
                "status": "error",
                "message": "You don't have permission to accept this friend request.",
            },
        )


class TestDeclineFriendRequest(TestCase):
    def setUp(self):
        self.user1 = Custom_User.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.user2 = Custom_User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        self.friend_request = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user2
        )

    def test_decline_friend_request_success(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(
            reverse(
                "account:decline_friend_request", kwargs={"uid": self.friend_request.id}
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.connection_status, "Declined")
        self.assertJSONEqual(response.content, {"status": "success"})

    def test_decline_friend_request_no_permission(self):
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse(
                "account:decline_friend_request", kwargs={"uid": self.friend_request.id}
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.connection_status, "Pending")
        self.assertJSONEqual(
            response.content,
            {
                "status": "error",
                "message": "You don't have permission to decline this friend request.",
            },
        )


class TestBlockAndUnblockFriend(TestCase):
    def setUp(self):
        self.user1 = Custom_User.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.user2 = Custom_User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        self.user3 = Custom_User.objects.create_user(
            username="testuser3", password="testpassword3"
        )
        self.friend_connection = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user2, connection_status="Accepted"
        )

    def test_block_friend_success(self):
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse(
                "account:block_friend",
                kwargs={"connection_id": self.friend_connection.id},
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_connection.refresh_from_db()
        self.assertEqual(self.friend_connection.connection_status, "Blocked")
        self.assertJSONEqual(
            response.content,
            {"status": "success", "message": "The user has been blocked"},
        )

    def test_block_friend_no_permission(self):
        self.client.login(username="testuser3", password="testpassword3")
        response = self.client.post(
            reverse(
                "account:block_friend",
                kwargs={"connection_id": self.friend_connection.id},
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_connection.refresh_from_db()
        self.assertEqual(self.friend_connection.connection_status, "Accepted")
        self.assertJSONEqual(
            response.content,
            {
                "status": "error",
                "message": "You don't have permission to block this user.",
            },
        )

    def test_unblock_friend_success(self):
        self.friend_connection.connection_status = "Blocked"
        self.friend_connection.blocked_by = self.user1
        self.friend_connection.save()
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse(
                "account:unblock_friend",
                kwargs={"connection_id": self.friend_connection.id},
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_connection.refresh_from_db()
        self.assertEqual(self.friend_connection.connection_status, "Accepted")
        self.assertJSONEqual(
            response.content,
            {"status": "success", "message": "The user has been unblocked"},
        )

    def test_unblock_friend_no_permission(self):
        self.friend_connection.connection_status = "Blocked"
        self.friend_connection.blocked_by = self.user1
        self.friend_connection.save()
        self.client.login(username="testuser3", password="testpassword3")
        response = self.client.post(
            reverse(
                "account:unblock_friend",
                kwargs={"connection_id": self.friend_connection.id},
            ),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.friend_connection.refresh_from_db()
        self.assertEqual(self.friend_connection.connection_status, "Blocked")
        self.assertJSONEqual(
            response.content,
            {
                "status": "error",
                "message": "You don't have permission to unblock this user.",
            },
        )
