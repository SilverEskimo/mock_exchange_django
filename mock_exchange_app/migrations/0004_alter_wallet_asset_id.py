# Generated by Django 4.2.2 on 2023-08-06 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mock_exchange_app", "0003_remove_profile_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="asset_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="asset",
                to="mock_exchange_app.asset",
            ),
        ),
    ]
