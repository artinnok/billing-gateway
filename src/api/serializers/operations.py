from rest_framework.serializers import ModelSerializer

from billing.models import Operation


class OperationSerializer(ModelSerializer):

    class Meta:
        model = Operation
        fields = ('id', 'direction', 'amount', 'fee', 'sender', 'receiver', 'payment', 'account',)
