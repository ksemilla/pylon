from ninja import NinjaAPI
from firebase_admin import auth

from .schemas import GetTokenSchema, VerifyTokenSchema
from auth.authentication import get_encoded_token, verify_token

auth_api = NinjaAPI()


@auth_api.post("")
def get_token_view(request, data: GetTokenSchema):
    googleUser = auth.verify_id_token(data.access_token)
    return {
        "token": get_encoded_token(
            {"email": googleUser["email"], "picture": googleUser["picture"]}
        )
    }


@auth_api.post("verify/")
def verify_token_view(request, data: VerifyTokenSchema):
    return verify_token(data.token)
