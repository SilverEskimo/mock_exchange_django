# Generated by Django 4.2.2 on 2023-07-26 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mock_exchange_app", "0002_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="address",
        ),
    ]
