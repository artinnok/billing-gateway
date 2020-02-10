from rest_framework.serializers import ModelSerializer

from billing.models import Account


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'currency', 'balance',)
