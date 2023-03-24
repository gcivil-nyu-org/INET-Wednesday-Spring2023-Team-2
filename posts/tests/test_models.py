from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from posts.views import PostsView, show_curr_post_api_view, home_view, results_view
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from login.models import Custom_User
from django.test import Client
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime


# 302: Redirect
# 200: OK (Rendering HTML)
# 301:


class ModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user("test4", "test1234")
        self.client.login(username="test4", password="test1234")
        self.model1_param = {"question_text": "q1", "created_by": self.user}
        self.model1 = Post_Model.objects.create(**self.model1_param)
        self.model1.save()

        self.option1_param = {"question": self.model1, "choice_text": "op1"}
        self.option1 = Options_Model.objects.create(**self.option1_param)
        self.option1.save()

        self.comment1_param = {
            "question": self.model1,
            "comment_text": "hello",
            "commented_by": self.user,
        }
        self.comment1 = Comments_Model.objects.create(**self.comment1_param)
        self.comment1.save()

        self.user_post_view_time1_param = {"user": self.user, "post": self.model1}
        self.user_post_view_time1 = UserPostViewTime.objects.create(
            **self.user_post_view_time1_param
        )
        self.user_post_view_time1.save()

    def test_post_create(self):
        self.assertEqual(self.model1.question_text, self.model1_param["question_text"])
        self.assertEqual(self.model1.created_by, self.model1_param["created_by"])
        self.assertEqual(self.model1.category, "misc")

    def test_option_created(self):
        self.assertEqual(self.option1.question, self.option1_param["question"])
        self.assertEqual(self.option1.choice_text, self.option1_param["choice_text"])
        self.assertEqual(self.option1.votes, 0)
        self.assertEqual(self.option1.color, "AED9E0")

    def test_comment_created(self):
        self.assertEqual(self.comment1.question, self.comment1_param["question"])
        self.assertEqual(
            self.comment1.comment_text, self.comment1_param["comment_text"]
        )
        self.assertEqual(
            self.comment1.commented_by, self.comment1_param["commented_by"]
        )

    def user_post_view_time_created(self):
        self.assertEqual(
            self.user_post_view_time1.user, self.user_post_view_time1_param["user"]
        )
        self.assertEqual(
            self.user_post_view_time1.post, self.user_post_view_time1_param["post"]
        )
