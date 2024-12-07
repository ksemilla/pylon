from ninja import Schema


class GetTokenSchema(Schema):
    access_token: str


class VerifyTokenSchema(Schema):
    token: str
