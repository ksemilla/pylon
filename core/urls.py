from ninja import NinjaAPI

from auth.authentication import CustomAuthentication
from auth.views import auth_router
from entities.views import entity_router
from users.views import user_router

api = NinjaAPI(auth=CustomAuthentication())

api.add_router("auth/", auth_router)
api.add_router("entities/", entity_router)
api.add_router("users/", user_router)
