from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from mock_exchange_app.models import Wallet
from mock_exchange_app.wallets.serializers import WalletSerializer


class WalletsViewSet(ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permission_classes = [IsAuthenticated]