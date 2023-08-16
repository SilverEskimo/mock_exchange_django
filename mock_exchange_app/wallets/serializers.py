from rest_framework.serializers import ModelSerializer

from mock_exchange_app.models import Wallet


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['asset_id', 'balance', 'wallet_address']
        depth = 1
