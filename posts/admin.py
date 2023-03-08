from django.contrib import admin
from .models import Post_Model, Options_Model

# Register your models here.

admin.site.register(Post_Model)
admin.site.register(Options_Model)
