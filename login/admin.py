from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Custom_User

# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     form = Custom_User
#     model = Custom_User
#     list_display = ["email", "username",]

admin.site.register(Custom_User)
