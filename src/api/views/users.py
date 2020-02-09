from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from api.serializers import users
from billing.models import Account


USER = get_user_model()


class SignupView(APIView):
    serializer_class = users.SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        user = USER.objects.create_user(
            email=serializer.validated_data['email'].lower().strip(),
            password=serializer.validated_data['password'],
        )

        self._create_default_account_list(user)

        return Response({'email': user.email})

    # TODO перенести в фоновые задачи
    def _create_default_account_list(self, user):
        with transaction.atomic():
            for currency in settings.DEFAULT_CURRENCY_LIST:
                Account.objects.create(
                    user=user,
                    currency=currency,
                )


class LoginView(APIView):
    serializer_class = users.LoginSerializer
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
