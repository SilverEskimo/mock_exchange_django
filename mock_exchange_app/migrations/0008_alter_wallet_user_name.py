# Generated by Django 4.2.2 on 2023-08-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mock_exchange_app", "0007_wallet_user_name_alter_wallet_wallet_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="user_name",
            field=models.CharField(default="My Wallet"),
        ),
    ]
