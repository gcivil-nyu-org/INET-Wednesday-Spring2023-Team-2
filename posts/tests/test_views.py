from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from posts.views import PostsView, show_curr_post_api_view, home_view, results_view
from posts.models import Post_Model, Options_Model, Comments_Model, UserPostViewTime
from login.models import Custom_User
from django.test import Client


class ResultsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="testuser", password="test"
        )
        self.post = Post_Model.objects.create(
            question_text="Test question?", created_by=self.user, id=1
        )
        self.option1 = Options_Model.objects.create(
            question=self.post, choice_text="option1"
        )
        self.option2 = Options_Model.objects.create(
            question=self.post, choice_text="option2"
        )
        self.post.viewed_by.add(self.user)
        self.post.save()

    def test_results_view(self):
        self.client.login(username="testuser", password="test")
        response = self.client.get(
            reverse("posts:show_curr_post_api", kwargs={"current_pid": 1})
        )

        self.assertEqual(response.status_code, 200)
