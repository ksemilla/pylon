from ninja.pagination import RouterPaginated
from ninja.errors import HttpError
from typing import List
from django.db.models import Q

from core.permissions import permissions, AdminPermisison

from .models import User
from .schemas import UserModelSchema, UserSchema, UserCreateByAdminSchema
from .permissions import AdminOrSelfPermission


user_router = RouterPaginated()


@user_router.get("", response=List[UserSchema])
@permissions([AdminPermisison])
def get_user_list(request, q: str = ""):
    return User.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
    )


@user_router.post("", response=UserSchema)
@permissions([AdminPermisison])
def create_user(request, data: UserCreateByAdminSchema):
    data.username = data.email
    _user = User.objects.filter(email=data.email).first()
    if _user:
        raise HttpError(400, "Email already used")

    return User.objects.create(**data.dict())


@user_router.get("{user_id}/", response=UserModelSchema)
@permissions([AdminOrSelfPermission])
def get_user(request, user_id: int):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, "User not found")


@user_router.put("{user_id}/", response=UserModelSchema)
@permissions([AdminPermisison])
def edit_user(request, user_id: int, data: UserSchema):
    try:
        user = User.objects.get(pk=user_id)

        for attr, value in data.dict(exclude_unset=True).items():
            setattr(user, attr, value)

        user.save()

        return user
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
