from ninja import ModelSchema, Schema, Field

from django.conf import settings
from .models import Entity, Member


class EntitySchema(ModelSchema):
    class Meta:
        model = Entity
        fields = "__all__"


class EntityCreateSchema(Schema):
    name: str


class UserMemberSchema(ModelSchema):
    entity: EntitySchema = Field(..., alias="entity")

    class Meta:
        model = Member
        fields = ["id", "role", "permissions", "default"]
