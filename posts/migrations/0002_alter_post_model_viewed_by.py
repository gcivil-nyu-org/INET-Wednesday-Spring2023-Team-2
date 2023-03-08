# Generated by Django 4.1.6 on 2023-03-08 20:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post_model",
            name="viewed_by",
            field=models.ManyToManyField(
                blank=True, related_name="posts_viewed", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
