from rest_framework.serializers import ModelSerializer

from billing.models import Payment


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'status', 'from_account', 'to_account', 'amount', 'fee',)
