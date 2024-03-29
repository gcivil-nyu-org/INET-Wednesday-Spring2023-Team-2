# Generated by Django 4.1.6 on 2023-04-17 21:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0010_rename_notification_model_noti_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="noti_model",
            name="content",
        ),
        migrations.AddField(
            model_name="noti_model",
            name="noti_type",
            field=models.CharField(
                choices=[("Invalid", "Invalid"), ("At", "At"), ("Comment", "Comment")],
                default="Invalid",
                max_length=20,
            ),
        ),
    ]
