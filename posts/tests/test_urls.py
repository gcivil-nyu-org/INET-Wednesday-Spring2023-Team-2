from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from posts.views import PostsView, show_curr_post_api_view, home_view, results_view
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from login.models import Custom_User
from django.test import Client


#302: Redirect
#200: OK (Rendering HTML)
#301: 


class HomePageTest(TestCase):
    def test_homepage_url(self):
        user1 = Custom_User.objects.create(username='test1', password='test123')
        post1 = Post_Model.objects.create(question_text="hi", created_by=user1)
        # option1 = Options_Model.objects.create(question=post1, choice_text='option1')
        # option2 = Options_Model.objects.create(question=post1, choice_text='option2')

        response = self.client.get(reverse("posts:home_page"))
        # print(response.status_code)
        self.assertEqual(response.status_code, 302)



class PostGenerationTest(TestCase):
    def test_post_generation_page_url(self):
        user1 = Custom_User.objects.create(username='test2', password='test1234')
        post1 = Post_Model.objects.create(question_text="hi2", created_by=user1, id=2)
        # option1 = Options_Model.objects.create(question=post1, choice_text='option1')
        # option2 = Options_Model.objects.create(question=post1, choice_text='option2')

        response = self.client.get(reverse("posts:post_generation_page", kwargs={'pid':2}))
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)



class CreatePollTest(TestCase):
    # def setUp(self):
    #     self.client = Client()
    #     self.user = Custom_User.objects.create_user('test3', 'test1234')
    #     self.client.login(username='test3', password='test1234')

    # def testLogin(self):
    #     self.client.login(username='test3', password='test1234')
    #     response = self.client.get(reverse('account:login_page'))
    #     self.assertEqual(response.status_code, 200)

    def test_create_poll_url_withoutlogin(self):
        # self.client.login(username='test3', password='test1234')
        # response1 = self.client.post(reverse("account:login_page"), {'username': 'test3', 'password': 'test1234', 'access_info': 'Sign In'})
        # print(response1)
        response = self.client.get(reverse('posts:create_poll'))
        # print("create_poll:", response.status_code)
        self.assertEqual(response.status_code, 302)

    def test_create_poll_url_login(self):
        # self.client.login(username='test3', password='test1234')
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        # response1 = self.client.post(reverse("account:login_page"), {'username': 'test3', 'password': 'test1234', 'access_info': 'Sign In'})
        # print(response1)
        response = self.client.get(reverse('posts:create_poll'))
        # print("create_poll:", response.status_code)
        self.assertEqual(response.status_code, 200)
        