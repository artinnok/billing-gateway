from rest_framework.generics import RetrieveAPIView

from api.serializers.payments import PaymentSerializer
from billing.models import Payment


class PaymentRetrieveView(RetrieveAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        account_list = self.request.user.account_list.all()

        from_payment_list = Payment.objects.filter(from_account__in=account_list)

        return from_payment_list
