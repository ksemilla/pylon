from ninja import ModelSchema, Schema, Field
from pydantic import (
    field_serializer,
)

from django.conf import settings
from .models import Entity, Member


class EntitySchema(ModelSchema):
    class Meta:
        model = Entity
        fields = "__all__"

    @field_serializer("photo", check_fields=False)
    def serialize_photo(self, value):
        return f"{settings.BASE_DIR}{value}" if settings.DEBUG else value


class EntityCreateSchema(Schema):
    name: str


class UserMemberSchema(ModelSchema):
    entity: EntitySchema = Field(..., alias="entity")

    class Meta:
        model = Member
        fields = ["id", "role"]
