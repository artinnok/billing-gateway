from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email'].lower().strip()

        user = authenticate(
            request=self.context['request'],
            email=email,
            password=data['password'],
        )

        if not user:
            raise serializers.ValidationError(code='invalid_credential')

        return data


class SignupSerializer(LoginSerializer):
    confirm_password = serializers.CharField()

    def validate(self, data):
        email = data['email'].lower().strip()

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(code='invalid_passwords')

        if USER.objects.filter(email=email).exists():
            raise serializers.ValidationError(code='invalid_credential')

        return data
