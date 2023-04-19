from django.contrib import admin
from .models import (
    Post_Model,
    Options_Model,
    Comments_Model,
    UserPostViewTime,
    Noti_Model,
)

# Register your models here.

admin.site.register(Post_Model)
admin.site.register(Options_Model)
admin.site.register(Comments_Model)
admin.site.register(Noti_Model)
admin.site.register(UserPostViewTime)
