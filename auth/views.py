from ninja import Router
from ninja.errors import HttpError
from firebase_admin import auth
from firebase_admin._auth_utils import (
    EmailAlreadyExistsError,
    InvalidIdTokenError,
)
from jwt.exceptions import InvalidSignatureError, DecodeError

from users.schemas import UserCreateGoogleSchema, UserCreateSchema
from users.models import User

from .schemas import (
    GetTokenSchema,
    TokenResponseSchema,
    VerifyTokenResponseSchema,
)
from .authentication import get_encoded_token, verify_token

auth_router = Router()


@auth_router.post("google-login/", auth=None)
def get_token_view(request, data: GetTokenSchema):
    try:
        firebase_user = auth.verify_id_token(data.access_token)
    except InvalidIdTokenError:
        raise HttpError(400, "Invalid google token")

    try:
        user = User.objects.get(email=firebase_user["email"])
    except User.DoesNotExist:
        raise HttpError(404, "User does not exist. Consider signing up.")

    return {"token": get_encoded_token({"userId": user.pk})}


@auth_router.post(
    "verify/", auth=None, response={200: VerifyTokenResponseSchema}
)
def verify_token_view(request, data: TokenResponseSchema):
    try:
        res = verify_token(data.token)
    except InvalidSignatureError:
        raise HttpError(400, "Invalid token")
    except DecodeError:
        raise HttpError(400, "Invalid token")
    return res


@auth_router.post("sign-up/", auth=None, response={200: TokenResponseSchema})
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
    "google-sign-up/", auth=None, response={200: TokenResponseSchema}
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
