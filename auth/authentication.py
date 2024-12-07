import jwt
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


def get_encoded_token(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")


class CustomAuthentication(BaseBackend):
    def authenticate(self, request, **kwargs):
        try:
            decoded = verify_token(request.data["token"])
        except:
            return None

        try:
            user = User.objects.get(email=decoded["email"])
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
