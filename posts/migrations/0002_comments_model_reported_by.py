# Generated by Django 4.1.6 on 2023-03-30 22:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments_model",
            name="reported_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="reported_comment_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
