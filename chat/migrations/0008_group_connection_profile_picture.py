# Generated by Django 4.1.6 on 2023-04-20 16:32

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0007_alter_connection_model_from_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="group_connection",
            name="profile_picture",
            field=models.ImageField(
                default="Group-Profile-Pictures/default-group-profile.jpeg",
                upload_to="Group-Profile-Pictures/",
                validators=[chat.models.validate_image_extension],
            ),
        ),
    ]
