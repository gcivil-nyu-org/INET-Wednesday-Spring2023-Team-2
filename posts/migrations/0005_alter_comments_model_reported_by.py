# Generated by Django 4.1.6 on 2023-04-04 18:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0004_comments_model_downvoted_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments_model",
            name="reported_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="reported_post_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
