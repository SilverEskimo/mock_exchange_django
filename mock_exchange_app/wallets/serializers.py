from rest_framework.serializers import ModelSerializer

from mock_exchange_app.models import Wallet


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = '__all__'
        depth = 1

    def save(self, **kwargs):
        self.validated_data.update(kwargs)
        super().save(**kwargs)
