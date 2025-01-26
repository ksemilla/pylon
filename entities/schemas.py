from ninja import ModelSchema, Schema, Field
from enum import Enum
from typing import Optional

from users.models import User

from .models import Entity, Member


class MemberRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class MemberUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "email"]


class EntitySchema(ModelSchema):
    class Meta:
        model = Entity
        fields = "__all__"


class EntityCreateSchema(Schema):
    name: str


class MemberSchema(ModelSchema):
    user: MemberUserSchema = Field(..., alias="user")

    class Meta:
        model = Member
        fields = "__all__"


class MemberCreateSchema(Schema):
    email: str
    role: MemberRole = MemberRole.USER


class MemberEditSchema(Schema):
    role: Optional[MemberRole] = None
    is_active: Optional[bool] = None
