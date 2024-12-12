from typing import List
from functools import wraps
from django.http import HttpRequest
from ninja.errors import HttpError
from users.models import User


class BasePermission:
    message: str = "Permission denied"

    @classmethod
    def has_permission(cls) -> bool:
        raise NotImplementedError


def permissions(permissions: List[BasePermission]):
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            for permission in permissions:
                res = permission.has_permission(request, *args, **kwargs)
                if not res:
                    raise HttpError(403, permission.message)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class AdminPermisison(BasePermission):
    message = "Only admins have permission"

    def has_permission(request, *args, **kwargs) -> bool:
        return request.user.role != User.Roles.ADMIN
