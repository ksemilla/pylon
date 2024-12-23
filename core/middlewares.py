import threading
import jwt
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from users.models import User

_user = threading.local()


class CurrentUserMiddleware:
    """Middleware to save the current user to thread-local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        header = self.get_header(request)
        token = self.get_token(header)
        user = self.validate_token(token)
        if user:
            _user.value = user
            request.user = user
        else:
            request.user = AnonymousUser()
        response = self.get_response(request)

        _user.value = None  # Clean up after the response
        return response

    def get_header(self, request: HttpRequest):
        return request.META.get("HTTP_AUTHORIZATION", "")

    def get_token(self, header: str):
        if header and " " in header:
            _, token = header.split(" ")
            return token
        return ""

    def validate_token(self, token: str):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            return User.objects.get(pk=decoded["userId"])
        except jwt.exceptions.DecodeError:
            return None
        except Exception:
            return None

    def get_user(self, user):
        return user


def get_current_user():
    """Helper to retrieve the current user."""
    return getattr(_user, "value", None)
