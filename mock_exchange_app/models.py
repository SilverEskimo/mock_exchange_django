from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class Asset(models.Model):
    asset_id = models.CharField(unique=True, max_length=10)
    blockExplorerUrl = models.CharField()

    class Meta:
        db_table = 'assets'


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    wallet_address = models.CharField()
    asset_id = models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum')])
    balance = models.FloatField(blank=True, validators=[validators.MinValueValidator(0)])
    vault_account_id = models.IntegerField(blank=True, validators=[validators.MinValueValidator(0)])
    vault_account_name = models.CharField(blank=True)
    workspace_id = models.CharField(blank=True)

    class Meta:
        db_table = "wallets"
        ordering = ['id']


class Order(models.Model):
    order_type = models.CharField(
        choices=[
            ("BUY", "Buy"),
            ("SELL", "Sell")
        ],
        blank=True
    )
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField()
    status = models.CharField(
        choices=[
            ("OPEN", "Open"),
            ("CLOSED", "Close"),
            ("CANCELLED", "Cancelled")
        ],
        default="OPEN"
    )
    asset_to_sell = models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="orders_to_sell_asset")
    asset_to_buy = models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="orders_to_buy_asset")
    amount_to_buy = models.FloatField(validators=[validators.MinValueValidator(0)])
    amount_to_sell = models.FloatField(validators=[validators.MinValueValidator(0)])
    ordering_wallet_id = models.ForeignKey(Wallet, on_delete=models.RESTRICT, blank=True, related_name="orders_ordering_wallet")
    buying_wallet_id = models.ForeignKey(Wallet, on_delete=models.RESTRICT, blank=True, related_name="orders_buying_wallet")

    class Meta:
        db_table = "order"
        ordering = ['id']


class Transaction(models.Model):

    asset_id = models.ForeignKey(Asset, on_delete=models.RESTRICT)
    status = models.CharField(
        choices=[
            ("PROCESSING", "Processing"),
            ("COMPLETED", "Completed"),
            ("CANCELLED", "Cancelled"),
            ("FAILED", "Failed")
        ],
        default="PROCESSING",
        blank=True
    )
    created_at = models.DateTimeField(blank=True)
    last_status_updated_at = models.DateTimeField(blank=True)
    amount = models.FloatField(validators=[validators.MinValueValidator(0)])
    outgoing = models.BooleanField(blank=True)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.RESTRICT, blank=True)
    tx_hash = models.CharField(null=True, blank=True)
    fee = models.FloatField(validators=[validators.MinValueValidator(0)], blank=True, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.RESTRICT, blank=True, null=True)
    fireblocks_tx_id = models.CharField(blank=True, null=True)

    class Meta:
        db_table = "transaction"
        ordering = ['id']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile')
    img_url = models.CharField(max_length=1024, null=True)

    class Meta:
        db_table = "profiles"
