
import os

from django.test import TestCase, Client
from login.models import Custom_User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from login.forms import LoginForm

# testuser = os.environ["testuser"]
# testuserpassword = os.environ["testuserpassword"]

class TestLoginViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(username="test", password="test1234")
        # self.login_url = reverse("account:login_page")
        # self.home_page_url = reverse("posts:home_page")
        # self.login_form = LoginForm()
        self.url = reverse('account:login_page')

    # def test_login_process(self):
    #     # self.user.login_view(username="test", password="test")
    #     # assert self.user.is_authenticated
    #     response = self.client.post(
    #         self.user.login_url, {
    #             "username":"testuser",
    #             "password":"test1234",
    #         },
    #         follow=True
    #     )

    #     self.assertRedirects(response, self.home_page_url)
    #     self.assertIn("_auth_user_id", self.client.session)
    #     self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)
        
    def test_login_url(self): 
        url_path = '/account/login/'
        # response = self.client.get(url_path)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    # def test_valid_login(self):
    #     self.client.login(username='test', password='test1234')
    #     response = self.client(reverse('account:login_page'))
    #     self.assertEqual(response.status_code, 200)

        # data = {"username" : "testuser", "password" : "testuserpassword"}
        # response = self.client.post(self.url, data)
        # self.assertRedirects(response, reverse("posts:home_page"))

    def test_logout(self):
        self.client.login(username='testuser', password='testuserpassword')
        response = self.client.get(reverse('posts:home_page'))
        self.assertEqual(response.status_code, 200)



class TestRegisterViews(TestCase):

    def setUp(self):
        self.client = Client()
        # self.user = Custom_User.objects.create_user(username="test", password="test1234")
        # self.login_url = reverse("account:login_page")
        # self.home_page_url = reverse("posts:home_page")
        # self.login_form = LoginForm()
        self.url = reverse('account:login_page')
  
    def test_register(self):
        response = self.client.post(reverse("account:login_page"), {'username': 'test', 'password': 'test1234', 'access_info': 'Sign Up', 'email': 'test@testemail.com'})
        self.assertEqual(response.status_code, 200)
        # user = Custom_User.objects.get(username='test')
        # user.is_active = True
        # user.save()
        self.assertTemplateUsed(response, 'pages/login.html')
        # self.assertEqual(Custom_User.objects.count(), 1)

    


