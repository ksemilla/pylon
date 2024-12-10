from ninja import Router
from firebase_admin import auth

from users.schemas import UserCreateGoogleSchema, UserSchema, UserCreateSchema
from users.models import User

from .schemas import GetTokenSchema, VerifyTokenSchema
from .authentication import get_encoded_token, verify_token

auth_router = Router()


@auth_router.post("", auth=None)
def get_token_view(request, data: GetTokenSchema):
    firebase_user = auth.verify_id_token(data.access_token)
    return {
        "token": get_encoded_token(
            {
                "email": firebase_user["email"],
                "picture": firebase_user["picture"],
            }
        )
    }


@auth_router.post("verify/", auth=None)
def verify_token_view(request, data: VerifyTokenSchema):
    return verify_token(data.token)


@auth_router.post("sign-up/", auth=None, response=UserSchema)
def sign_up_view(request, data: UserCreateSchema):
    firebase_user = auth.create_user(email=data.email, password=data.password)
    return User.objects.create(
        email=firebase_user.email,
        picture=firebase_user.photo_url,
        firebase_uid=firebase_user.uid,
    )


@auth_router.post("google-sign-up/", auth=None, response=UserSchema)
def sign_up_view(request, data: UserCreateGoogleSchema):
    firebase_user = auth.verify_id_token(data.access_token)
    print(firebase_user)
    return User.objects.create(
        email=firebase_user.email,
        picture=firebase_user.photo_url,
        uid=firebase_user.uid,
    )
