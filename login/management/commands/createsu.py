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
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not Custom_User.objects.filter(
            username=os.getenv("ADMIN_USERNAME")
        ).exists():
            user_ = Custom_User()
            user_.username = os.getenv("ADMIN_USERNAME")
            user_.email = os.getenv("ADMIN_EMAIL")
            user_.isactive = True
            user_.set_password(os.getenv("ADMIN_PASSWORD"))
            user_.is_superuser = True
            user_.is_staff = True
            user_.save()
            print("Superuser has been created.")
