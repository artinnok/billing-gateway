from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from tasks import transfer_money
from billing.models import Payment, Account
from api.serializers.transfer import TransferSerializer


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
        amount = serializer.validated_data['amount']
        payment = Payment.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            fee=Payment.calculate_fee(from_account, to_account, amount),
            status=settings.INITIATED,
        )

        settings.QUEUE.enqueue(
            transfer_money,
            payment_id=payment.id,
        )

        return Response({
            'amount': payment.amount,
            'fee': payment.fee,
            'payment': payment.id
        })
