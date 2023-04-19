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
            reverse("posts:post_generation_page", kwargs={"category": "all", "pid": 2})
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
            reverse(
                "posts:show_curr_post_api", kwargs={"category": "all", "current_pid": 2}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_ShowCurrPost_ajax(self):
        response = self.client.post(
            reverse(
                "posts:show_curr_post_api", kwargs={"category": "all", "current_pid": 2}
            ),
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
        url = reverse(
            "posts:get_current_post_url_api",
            kwargs={"category": "all", "current_pid": 2},
        )
        request = self.factory.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = CurrentPostURL.as_view()(request, category="all", current_pid=2)
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
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        response = self.client.get(
            reverse("posts:show_comments_api", kwargs={"current_pid": 1}),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(response.status_code, 200)

    def test_report_post(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        response = self.client.get(
            reverse("posts:report_post", kwargs={"post_id": post4.id}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(
            response.json(), {"report": "success", "message": "Poll has been reported"}
        )

        # Refresh the post object from the database
        post4.refresh_from_db()

        # Check if the post was reported and reported count was incremented
        self.assertIn(user, post4.reported_by.all())
        self.assertEqual(post4.reported_count, 1)

    def test_report_post_already_reported(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        post4.reported_by.add(user)
        response = self.client.get(
            reverse("posts:report_post", args=[post4.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(
            response.json(), {"report": "cancel", "message": "Report has been canceled"}
        )

        # Refresh the post object from the database
        post4.refresh_from_db()

    def test_report_post_not_ajax(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        # Send a non-AJAX request to report the post
        response = self.client.get(reverse("posts:report_post", args=[post4.id]))

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Refresh the post object from the database
        post4.refresh_from_db()

    def test_report_comment(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        response = self.client.get(
            reverse("posts:report_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(
            response.json(),
            {"report": "success", "message": "Comment has been reported"},
        )

        # Refresh the post object from the database
        comment2.refresh_from_db()

        # Check if the post was reported and reported count was incremented
        self.assertIn(user, comment2.reported_by.all())
        self.assertEqual(comment2.reported_count, 1)

    def test_report_comment_already_reported(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )
        comment2.reported_by.add(user)
        response = self.client.get(
            reverse("posts:report_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(
            response.json(),
            {"report": "unreported", "message": "Report has been canceled"},
        )

        # Refresh the post object from the database
        post4.refresh_from_db()

        # Check if reported count remains unchanged
        self.assertEqual(comment2.reported_count, 0)

    def test_report_comment_not_ajax(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        # Send a non-AJAX request to report the post
        response = self.client.get(reverse("posts:report_comment", args=[comment2.id]))

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Refresh the post object from the database
        post4.refresh_from_db()

        # Check if reported count remains unchanged
        self.assertEqual(comment2.reported_count, 0)

    def test_delete_comment_success(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        # Send an AJAX request to delete the comment
        response = self.client.get(
            reverse("posts:delete_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(
            response.json(),
            {"delete": "success", "message": "Comment has been deleted"},
        )

        # Check if the comment is deleted from the database
        with self.assertRaises(Comments_Model.DoesNotExist):
            Comments_Model.objects.get(id=comment2.id)

    def test_redirect_to_home_view(self):
        # Generate URL for named view "go_home"
        url = reverse("go_home")

        # Perform a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 302)

    def test_upvote_comment_success(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        # Send an AJAX request to upvote the comment
        response = self.client.get(
            reverse("posts:upvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(response.json(), {"upvote": "success"})

        # Refresh the comment object from the database
        comment2.refresh_from_db()

        # Check if the user1 is added to upvoted_by and vote_count is updated
        self.assertIn(user, comment2.upvoted_by.all())
        self.assertEqual(comment2.vote_count, 1)

    def test_downvote_comment_success(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        # Send an AJAX request to upvote the comment
        response = self.client.get(
            reverse("posts:downvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        self.assertEqual(response.json(), {"downvote": "success"})

        # Refresh the comment object from the database
        comment2.refresh_from_db()

        # Check if the user1 is added to upvoted_by and vote_count is updated
        self.assertIn(user, comment2.downvoted_by.all())
        self.assertEqual(comment2.vote_count, -1)

    def test_upvote_comment_change_success(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        response = self.client.get(
            reverse("posts:downvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        comment2.refresh_from_db()

        self.assertEqual(comment2.vote_count, -1)

        response = self.client.get(
            reverse("posts:upvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

        # Refresh the comment object from the database

        self.assertEqual(response.json(), {"upvote": "change vote success"})

        comment2.refresh_from_db()

        self.assertNotIn(user, comment2.downvoted_by.all())
        self.assertIn(user, comment2.upvoted_by.all())
        self.assertEqual(comment2.vote_count, 1)

    def test_downvote_comment_change_success(self):
        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post4 = Post_Model.objects.create(
            question_text="bye", created_by=self.user1, id=7
        )
        option1 = Options_Model.objects.create(question=post4, choice_text="option1")
        option2 = Options_Model.objects.create(question=post4, choice_text="option2")
        option1.chosen_by.add(user)
        comment2 = Comments_Model.objects.create(
            comment_text="Test Comment 2", question=post4, commented_by=user
        )

        response = self.client.get(
            reverse("posts:upvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        comment2.refresh_from_db()

        self.assertEqual(comment2.vote_count, 1)

        response = self.client.get(
            reverse("posts:downvote_comment", args=[comment2.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

        # Refresh the comment object from the database

        self.assertEqual(response.json(), {"downvote": "change vote success"})

        comment2.refresh_from_db()

        self.assertNotIn(user, comment2.upvoted_by.all())
        self.assertIn(user, comment2.downvoted_by.all())
        self.assertEqual(comment2.vote_count, -1)

    def test_search_posts_view(self):
        self.url = reverse("posts:search_posts")

        user = Custom_User.objects.create_user(username="test3", password="test1234")
        self.client.force_login(user=user)
        post5 = Post_Model.objects.create(
            question_text="Test question 1", created_by=self.user1, id=7
        )
        post6 = Post_Model.objects.create(
            question_text="Test question 2", created_by=self.user1, id=8
        )

        option1 = Options_Model.objects.create(question=post5, choice_text="1option1")
        option2 = Options_Model.objects.create(question=post5, choice_text="1option2")
        option3 = Options_Model.objects.create(question=post6, choice_text="2option1")
        option3 = Options_Model.objects.create(question=post6, choice_text="2option2")

        response = self.client.get(self.url, {"search": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test question 1")
        self.assertContains(response, "1option1")
        self.assertContains(response, "Test question 2")
        self.assertContains(response, "2option2")

        response = self.client.get(self.url, {"search": "foo"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test question 1")
        self.assertNotContains(response, "1option1")
        self.assertNotContains(response, "Test question 2")
        self.assertNotContains(response, "2option2")

        response = self.client.get(self.url, {"search": ""})
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()["search_results"], [])

    def test_home(self):
        response = self.client.get(
            reverse(
                "go_home",
            ),
        )
        print(response)
        self.assertEqual(response.status_code, 302)
