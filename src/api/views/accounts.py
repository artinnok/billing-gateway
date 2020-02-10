from rest_framework.generics import ListAPIView

from api.serializers.accounts import AccountSerializer


class AccountListView(ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return self.request.user.account_list.all()
