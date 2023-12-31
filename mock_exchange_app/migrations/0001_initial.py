# Generated by Django 4.2.2 on 2023-07-02 17:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("asset_id", models.CharField(max_length=10, unique=True)),
                ("blockExplorerUrl", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_type",
                    models.CharField(
                        blank=True, choices=[("BUY", "Buy"), ("SELL", "Sell")]
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("closed_at", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("CLOSED", "Close"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="OPEN",
                    ),
                ),
                (
                    "amount_to_buy",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "amount_to_sell",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "asset_to_buy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="orders_to_buy_asset",
                        to="mock_exchange_app.asset",
                    ),
                ),
                (
                    "asset_to_sell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="orders_to_sell_asset",
                        to="mock_exchange_app.asset",
                    ),
                ),
            ],
            options={
                "db_table": "order",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "balance",
                    models.FloatField(
                        blank=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "vault_account_id",
                    models.IntegerField(
                        blank=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("vault_account_name", models.CharField(blank=True)),
                ("workspace_id", models.CharField(blank=True)),
                (
                    "asset_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="mock_exchange_app.asset",
                    ),
                ),
            ],
            options={
                "db_table": "wallet",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PROCESSING", "Processing"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                            ("FAILED", "Failed"),
                        ],
                        default="PROCESSING",
                    ),
                ),
                ("created_at", models.DateTimeField(blank=True)),
                ("last_status_updated_at", models.DateTimeField(blank=True)),
                (
                    "amount",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("outgoing", models.BooleanField(blank=True)),
                ("tx_hash", models.CharField(blank=True, null=True)),
                (
                    "fee",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("fireblocks_tx_id", models.CharField(blank=True, null=True)),
                (
                    "asset_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="mock_exchange_app.asset",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="mock_exchange_app.order",
                    ),
                ),
                (
                    "wallet_id",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="mock_exchange_app.wallet",
                    ),
                ),
            ],
            options={
                "db_table": "transaction",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="order",
            name="buying_wallet_id",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="orders_buying_wallet",
                to="mock_exchange_app.wallet",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="ordering_wallet_id",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="orders_ordering_wallet",
                to="mock_exchange_app.wallet",
            ),
        ),
    ]
