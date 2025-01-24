from ninja import ModelSchema, Schema, Field


from users.models import User

from .models import Entity, Member


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
