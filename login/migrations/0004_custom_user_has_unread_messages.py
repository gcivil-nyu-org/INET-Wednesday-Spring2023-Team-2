# Generated by Django 4.1.6 on 2023-04-27 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0003_alter_custom_user_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="custom_user",
            name="has_unread_messages",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]