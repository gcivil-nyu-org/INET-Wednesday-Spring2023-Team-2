import os

from django.test import TestCase, Client
from login.models import Custom_User, validate_image_extension
from django.core import mail
from unittest.mock import patch
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from login.tokens import account_activation_token
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from login.forms import LoginForm
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from login.forms import (
    LoginForm,
    RegisterForm,
    PasswordChangeForm,
    PasswordResetConfirmationForm,
    PasswordResetForm,
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
        url = reverse("account:activate_page", kwargs={"uid": uid, "token": invalid_token})

        # Attempt to activate the user with an invalid token
        response = self.client.get(url)

        # Check if the email verification failed message is displayed
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), "Registration successful, verify email to login.")
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
            username=self.username,
            password=self.password
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

            
