import uuid

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from ..models import Wallet
from .serializers import WalletSerializer
from ..providers import fireblocks

UTXO_DEPOSIT_VAULT = '0'
USER_VAULT_PREFIX = "user_id_"


class WalletsViewSet(ModelViewSet):
    fireblocks_provider = fireblocks.FireblocksProvider()
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_name = self.request.data['wallet']['user_name']
        serializer.save(
           user_name=user_name
        )

    def perform_create(self, serializer):
        asset_id = serializer.validated_data['asset_id']
        new_vault_account = None
        new_wallet = None
        vault_account_name = USER_VAULT_PREFIX + str(self.request.user.id)
        if asset_id == 'BTC':
            asset_id += '_TEST'
            new_wallet = self.fireblocks_provider.create_new_utxo_address(
                UTXO_DEPOSIT_VAULT,
                asset_id,
                vault_account_name
            )
        else:
            asset_id += '_TEST3'
            eth_wallet = self.queryset.filter(user=self.request.user).filter(asset_id='ETH')
            if not eth_wallet:
                new_vault_account = self.fireblocks_provider.create_new_vault_account(vault_account_name)
                new_wallet = self.fireblocks_provider.create_new_wallet(new_vault_account["id"], asset_id)

        serializer.save(
            vault_account_id= new_vault_account["id"] if new_vault_account else int(UTXO_DEPOSIT_VAULT),
            vault_account_name=vault_account_name,
            asset_id=asset_id,
            wallet_address=new_wallet["address"],
            balance=0,
            user_id=self.request.user.id
        )


