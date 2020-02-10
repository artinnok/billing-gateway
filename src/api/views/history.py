from django.conf import settings

from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from api.serializers.history import OperationSerializer
from billing.models import Operation


class OperationFilter(filters.FilterSet):
    amount__gt = filters.NumberFilter(field_name='amount', lookup_expr='gt')
    amount__lt = filters.NumberFilter(field_name='amount', lookup_expr='lt')
    ordering = filters.OrderingFilter(
        fields=(
            ('amount', 'amount',),
            ('direction', 'direction'),
        ),
    )

    class Meta:
        model = Operation
        fields = ['payment', 'account', 'direction']


class OperationListView(ListAPIView):
    serializer_class = OperationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OperationFilter

    def get_queryset(self):
        account_list = self.request.user.account_list.all()
        operation_list = Operation.objects.filter(account__in=account_list)
        # комиссия уже учтена в операциях по трансферу -
        # показывать операцию снятия комисии нет смысла
        return operation_list.exclude(kind=settings.FEE)
