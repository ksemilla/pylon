import jwt
from django.conf import settings
from ninja.security import HttpBearer


def get_encoded_token(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")


class CustomAuthentication(HttpBearer):
    def authenticate(self, request, token):
        return request.user.is_authenticated
