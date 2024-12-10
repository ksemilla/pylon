from ninja import ModelSchema, Schema

from .models import User


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"


class UserCreateGoogleSchema(Schema):
    access_token: str


class UserCreateSchema(Schema):
    email: str
    password: str
