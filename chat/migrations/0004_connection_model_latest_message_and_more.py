# Generated by Django 4.1.6 on 2023-04-16 23:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_connection_model_blocked_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="connection_model",
            name="latest_message",
            field=models.CharField(blank=True, max_length=23),
        ),
        migrations.AddField(
            model_name="connection_model",
            name="latest_message_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]