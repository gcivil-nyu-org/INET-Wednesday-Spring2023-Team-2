# from django.contrib.auth import get_user_model
from login.models import Custom_User
from django.core.management.base import BaseCommand
from showofhands.settings import BASE_DIR
import os

from dotenv import load_dotenv

env_path = os.path.join(BASE_DIR, "showofhands")
load_dotenv(env_path)


# User = get_user_model()


class Command(BaseCommand):
    help = "Creates Test Party Users"

    def handle(self, *args, **options):
        users = [
            "test_prof",
            "test_ta",
            "test_user1",
            "test_user2",
            "test_user3",
            "test_user4",
            "test_user5",
            "ajt9616",
            "bc3177",
            "jsw9232",
            "jz5348",
            "jg6269",
            "lre250",
            "mm13064",
            "ng2451",
            "rs8117",
            "vs2476",
            "yc3346",
        ]
        for user in users:
            if not Custom_User.objects.filter(username=user).exists():
                user_ = Custom_User()
                user_.username = user
                user_.isactive = True
                user_.set_password(os.getenv("TPU_PASSWORD"))
                user_.save()
                print(f"User with username '{user}' has been created.")
