from rest_framework.views import APIView
from rest_framework.response import Response

from billing.models import Account
from api.serializers.transfer import TransferSerializer
from billing.utils import transfer_money, calculate_fee


class TransferView(APIView):
    serializer_class = TransferSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        from_account = Account.objects.get(id=serializer.validated_data['from_account'])
        to_account = Account.objects.get(id=serializer.validated_data['to_account'])

        # TODO перенести в фоновые задачи
        fee = calculate_fee(
            from_account=from_account,
            to_account=to_account,
            amount=serializer.validated_data['amount'],
        )
        money = transfer_money(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=serializer.validated_data['amount'],
            fee=fee,
        )

        return Response({
            'fee': money['fee'],
            'rest_amount': money['rest_amount'],
        })
