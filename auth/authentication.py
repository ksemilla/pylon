import jwt
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ninja.security import HttpBearer


def get_encoded_token(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")


class CustomAuthentication(HttpBearer):
    def authenticate(self, request, token):
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            return True
        except jwt.exceptions.DecodeError:
            return False
        except Exception as e:
            return False
