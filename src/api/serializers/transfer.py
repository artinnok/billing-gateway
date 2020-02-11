from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from billing.models import Account


class TransferSerializer(serializers.Serializer):
    from_account = serializers.IntegerField()
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    def validate(self, data):
        account_list = self.context['request'].user.account_list.all()
        account = get_object_or_404(account_list, id=data['from_account'])

        if account.balance < data['amount']:
            raise serializers.ValidationError('not_enough_money')

        return data

    def validate_to_account(self, value):
        get_object_or_404(Account.objects.all(), id=value)

        return value
