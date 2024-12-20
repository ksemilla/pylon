from ninja.pagination import RouterPaginated
from ninja.errors import HttpError
from typing import List
from django.db.models import Q

from core.permissions import permissions, AdminPermisison

from .models import User
from .schemas import UserSchema


user_router = RouterPaginated()


@user_router.get("", response=List[UserSchema])
@permissions([AdminPermisison])
def get_user_list(request, q: str = ""):
    return User.objects.filter(
        Q(first_name__icontains=q)
        | Q(last_name__icontains=q)
        | Q(email__icontains=q)
    )


@user_router.get("{user_id}/", response=UserSchema)
def get_user(request, user_id: int):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
