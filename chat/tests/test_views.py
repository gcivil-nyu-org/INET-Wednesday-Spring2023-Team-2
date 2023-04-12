from django.test import TestCase, Client
from django.urls import reverse

from login.models import Custom_User
from chat.views import get_chat_history
from chat.models import (
    Connection_Model,
    Chat_Message,
    Chat_History,
)


class TestChatViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Custom_User.objects.create_user(
            username="test", email="test@testemail.com", password="test1234"
        )
        self.chat_url = reverse("connections:chat_page")
        self.login_url = reverse("account:login_page")
        # user will be friends with user1 and not friends with user2
        self.user1 = Custom_User.objects.create_user(
            username="friend1", email="friend1@testemail.com", password="test1234"
        )
        self.connection = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user, connection_status="Accepted"
        )

        self.user2 = Custom_User.objects.create_user(
            username="nfriend", email="nfriend@testemail.com", password="test1234"
        )

    def test_friend_connection(self):
        self.client.login(username="test", password="test1234")
        self.assertTrue(
            Connection_Model.connection_exists(Connection_Model, self.user1, self.user)
        )
        self.assertTrue(
            Connection_Model.connection_exists(Connection_Model, self.user, self.user1)
        )
        self.assertFalse(
            Connection_Model.connection_exists(Connection_Model, self.user, self.user2)
        )

    def test_chat_page_friendslist(self):
        self.client.login(username="test", password="test1234")
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/chat.html")

        friends = response.context["friends"]
        friend_objects = [friend.get_friend(self.user) for friend in friends]

        self.assertIn(self.user1, friend_objects)
        self.assertNotIn(self.user2, friend_objects)

    def test_chat_page_chathistory_view_valid(self):
        self.client.login(username="test", password="test1234")
        response = self.client.get(
            reverse("connections:get_chat_history_box", args=[self.connection.id]),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/chat_box.html")
        self.assertContains(response, self.user1.username)

        messages = get_chat_history(self.connection.id)
        for message in messages:
            self.assertContains(response, message.message)

    def test_chat_page_chathistory_view_invalid(self):
        self.client.login(username="test", password="test1234")
        response = self.client.get(
            reverse("connections:get_chat_history_box", args=[99999])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thou Shall not Enter!!")
