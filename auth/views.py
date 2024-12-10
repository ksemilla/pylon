from ninja import Router
from ninja.errors import HttpError
from firebase_admin import auth
from firebase_admin._auth_utils import (
    EmailAlreadyExistsError,
    EmailNotFoundError,
)

from users.schemas import UserCreateGoogleSchema, UserSchema, UserCreateSchema
from users.models import User

from .schemas import GetTokenSchema, TokenResponseSchema
from .authentication import get_encoded_token, verify_token

auth_router = Router()


@auth_router.post("google-login/", auth=None)
def get_token_view(request, data: GetTokenSchema):
    firebase_user = auth.verify_id_token(data.access_token)

    try:
        user = User.objects.get(email=firebase_user["email"])
    except User.DoesNotExist:
        raise HttpError(404, "User does not exist. Consider signing up.")

    return {"token": get_encoded_token({"userId": user.pk})}


@auth_router.post("verify/", auth=None)
def verify_token_view(request, data: TokenResponseSchema):
    return verify_token(data.token)


@auth_router.post("sign-up/", auth=None, response={201: TokenResponseSchema})
def sign_up_view(request, data: UserCreateSchema):
    try:
        firebase_user = auth.create_user(
            email=data.email, password=data.password
        )
    except EmailAlreadyExistsError:
        raise HttpError(400, "Email already exists")

    user = User.objects.create(
        username=firebase_user.email,
        email=firebase_user.email,
        picture=firebase_user.photo_url,
        firebase_uid=firebase_user.uid,
    )

    return {"token": get_encoded_token({"userId": user.pk})}


@auth_router.post(
    "google-sign-up/", auth=None, response={201: TokenResponseSchema}
)
def sign_up_view(request, data: UserCreateGoogleSchema):
    firebase_user = auth.verify_id_token(data.access_token)

    _user = User.objects.filter(email=firebase_user["email"]).first()
    if _user:
        raise HttpError(400, "Email already exists. Try logging in.")

    user = User.objects.create(
        username=firebase_user["email"],
        email=firebase_user["email"],
        picture=firebase_user["picture"],
        firebase_uid=firebase_user["uid"],
    )

    return {"token": get_encoded_token({"userId": user.pk})}
