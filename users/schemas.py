from ninja import ModelSchema, Schema
from typing import Optional
from enum import Enum

from .models import User


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class UserModelSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["password", "groups", "user_permissions"]


class UserSchema(Schema):
    id: Optional[int]
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRole = UserRole.USER


class UserCreateGoogleSchema(Schema):
    access_token: str


class UserCreateSchema(Schema):
    email: str
    password: str


class UserCreateByAdminSchema(Schema):
    email: str
    username: Optional[str]
    role: UserRole = UserRole.USER
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
