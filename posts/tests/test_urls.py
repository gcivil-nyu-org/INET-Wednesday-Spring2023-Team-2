from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from posts.views import PostsView, show_curr_post_api_view, home_view, results_view
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from login.models import Custom_User
from django.test import Client, TestCase, RequestFactory
from rest_framework.test import APITestCase
from rest_framework.views import Response, status
from posts.views import CurrentPostURL


# 302: Redirect
# 200: OK (Rendering HTML)
# 301:


class HomePageTest(TestCase):
    def test_homepage_url(self):
        user1 = Custom_User.objects.create(username="test1", password="test123")
        post1 = Post_Model.objects.create(question_text="hi", created_by=user1)
        # option1 = Options_Model.objects.create(question=post1, choice_text='option1')
        # option2 = Options_Model.objects.create(question=post1, choice_text='option2')

        response = self.client.get(reverse("posts:home_page"))
        # print(response.status_code)
        self.assertEqual(response.status_code, 302)


class PostGenerationTest(TestCase):
    def test_post_generation_page_url(self):
        user1 = Custom_User.objects.create(username="test2", password="test1234")
        post1 = Post_Model.objects.create(question_text="hi2", created_by=user1, id=2)
        # option1 = Options_Model.objects.create(question=post1, choice_text='option1')
        # option2 = Options_Model.objects.create(question=post1, choice_text='option2')

        response = self.client.get(
            reverse("posts:post_generation_page", kwargs={"pid": 2})
        )
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
        response = self.client.get(reverse("posts:create_poll"))
        # print("create_poll:", response.status_code)
        self.assertEqual(response.status_code, 302)

    def test_create_poll_url_login(self):
        # self.client.login(username='test3', password='test1234')
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        # response1 = self.client.post(reverse("account:login_page"), {'username': 'test3', 'password': 'test1234', 'access_info': 'Sign In'})
        # print(response1)
        response = self.client.get(reverse("posts:create_poll"))
        # print("create_poll:", response.status_code)
        self.assertEqual(response.status_code, 200)


class ViewsFunctions(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Custom_User.objects.create(
            username="test1", password="test123", id=1
        )
        self.post1 = Post_Model.objects.create(
            question_text="hi", created_by=self.user1, id=1
        )
        self.post2 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1
        )

    def test_create_poll(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        # data = {
        #     'prefix': 'Test question',
        #     'category': 'sports',
        #     'delay': 'No Delay',
        #     'choice1': 'Option 1',
        #     'choice2': 'Option 2',
        # }

        # response = self.client.post(reverse("posts:create_poll"), data)
        response = self.client.post(
            reverse("posts:create_poll"),
            {
                "prefix": "Show of hands if",
                "category": "sports",
                "delay": "0",
                "choice1": "Option 1",
                "choice2": "Option 2",
                "created_by": user,
            },
            follows=True,
        )
        self.assertEqual(response.status_code, 302)

        post1 = Post_Model.objects.last()
        self.assertEqual(post1.question_text, "Show of hands if")
        self.assertEqual(post1.category, ["sports"])
        self.assertEqual(post1.created_by, user)

    def test_ShowCurrPost_ajax(self):
        response = self.client.post(
            reverse("posts:show_curr_post_api", kwargs={"current_pid": 2})
        )
        self.assertEqual(response.status_code, 200)

    def test_ShowCurrPost_ajax(self):
        response = self.client.post(
            reverse("posts:show_curr_post_api", kwargs={"current_pid": 2}),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(response.status_code, 200)

    def test_show_comments_text_api_get_ajax(self):
        response = self.client.get(
            reverse("posts:show_comments_text_api", kwargs={"current_pid": 2})
        )
        self.assertEqual(response.status_code, 200)

    def test_ajax_get_current_post_url_api(self):
        self.factory = RequestFactory()
        url = reverse("posts:get_current_post_url_api", kwargs={"current_pid": 2})
        request = self.factory.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = CurrentPostURL.as_view()(request, current_pid=2)
        self.assertEqual(response.status_code, 200)

    # def test_non_ajax_get_current_post_url_api(self):
    #     factory = RequestFactory()
    #     url = reverse("posts:get_current_post_url_api", kwargs={"current_pid": 2})
    #     request = factory.get(url)
    #     response = CurrentPostURL.as_view()(request, current_pid=2)
    #     self.assertEqual(response.status_code, 403)

    def test_comments_post_ajax(self):
        # self.client.login(username="test1", password="test123")
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post3 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=6
        )
        response = self.client.post(
            reverse("posts:show_comments_api", kwargs={"current_pid": 6}),
            {"comment_text": "Test Comment 1"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(
            Comments_Model.objects.get(question=post3).comment_text, "Test Comment 1"
        )
        self.assertEqual(response.status_code, 200)

    def test_comments_get_ajax(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text='option1')
        option2 = Options_Model.objects.create(question=post4, choice_text='option2')
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        response = self.client.get(
            reverse("posts:show_comments_api", kwargs={"current_pid": 1}),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(response.status_code, 200)
