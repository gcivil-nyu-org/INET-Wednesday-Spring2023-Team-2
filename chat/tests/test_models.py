from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from chat.models import Connection_Model
from login.models import Custom_User


class ModelTest(TestCase):
    def setUp(self):
        self.user1 = Custom_User.objects.create(
            username="user1", email="user1@example.com"
        )
        self.user2 = Custom_User.objects.create(
            username="user2", email="user2@example.com"
        )
        self.user3 = Custom_User.objects.create(
            username="user3", email="user3@example.com"
        )

        self.connection1 = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user2
        )
        self.connection2 = Connection_Model.objects.create(
            from_user=self.user2, to_user=self.user3
        )

    def test_connection_creation(self):
        connection = Connection_Model.objects.create(
            from_user=self.user1, to_user=self.user3
        )
        self.assertEqual(
            str(connection), f"{connection.id} => {self.user1} + {self.user3}"
        )

    def test_connection_str(self):
        self.assertEqual(
            str(self.connection1),
            f"{self.connection1.id} => {self.user1} + {self.user2}",
        )

    def test_get_friend(self):
        friend1 = self.connection1.get_friend(user=self.user1)
        friend2 = self.connection1.get_friend(user=self.user2)
        self.assertEqual(friend1, self.user2)
        self.assertEqual(friend2, self.user1)

    def test_connection_exists(self):
        self.assertTrue(
            Connection_Model.connection_exists(
                Connection_Model, from_user=self.user1, to_user=self.user2
            )
        )
        self.assertFalse(
            Connection_Model.connection_exists(
                Connection_Model, from_user=self.user1, to_user=self.user3
            )
        )
