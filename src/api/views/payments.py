from rest_framework.generics import RetrieveAPIView

from api.serializers.payments import PaymentSerializer


class PaymentRetrieveView(RetrieveAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return self.request.user.payment_list.all()
