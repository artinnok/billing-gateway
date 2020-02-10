from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from api.serializers import auth
from tasks import create_init_account


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

        settings.QUEUE.enqueue(
            create_init_account,
            email=serializer.validated_data['email'].lower().strip(),
            password=serializer.validated_data['password'],
        )

        return Response({'email': serializer.validated_data['email']})


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
