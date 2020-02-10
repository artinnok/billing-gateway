from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from api.serializers import auth
from billing.models import Account
from billing.utils import transfer_money


USER = get_user_model()


class SignupView(APIView):
    serializer_class = auth.SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = USER.objects.create_user(
                email=serializer.validated_data['email'].lower().strip(),
                password=serializer.validated_data['password'],
            )
            self._init_account(user)

        return Response({'email': user.email})

    # TODO перенести в фоновые задачи
    def _init_account(self, user):
        for currency in settings.DEFAULT_CURRENCY_LIST:
            account = Account.objects.create(
                user=user,
                currency=currency,
            )
            if currency != settings.USD:
                continue

            internal_account = Account.objects.get(
                code=settings.INTERNAL,
                currency=currency,
            )
            transfer_money(
                from_account_id=internal_account.id,
                to_account_id=account.id,
                amount=settings.DEFAULT_USD_BALANCE,
                fee=settings.ZERO_FEE,
            )


class LoginView(APIView):
    serializer_class = auth.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            email=serializer.validated_data['email'].lower().strip(),
            password=serializer.validated_data['password'],
        )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
