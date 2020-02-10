from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from tasks import transfer_money
from billing.models import Payment
from api.serializers.transfer import TransferSerializer


class TransferView(APIView):
    serializer_class = TransferSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        payment = Payment.objects.create(
            user=request.user,
            status=settings.INITIATED,
        )
        settings.QUEUE.enqueue(
            transfer_money,
            payment_id=payment.id,
            from_account_id=serializer.validated_data['from_account'],
            to_account_id=serializer.validated_data['to_account'],
            amount=serializer.validated_data['amount'],
        )

        return Response({
            'amount': serializer.validated_data['amount'],
            'payment': payment.id
        })
