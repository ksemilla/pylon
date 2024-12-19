from ninja import Schema


class GetTokenSchema(Schema):
    access_token: str


class TokenResponseSchema(Schema):
    token: str


class VerifyTokenResponseSchema(Schema):
    userId: int
