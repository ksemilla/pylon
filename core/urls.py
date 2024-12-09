from ninja import NinjaAPI

from auth.views import auth_router
from entities.views import entity_router

api = NinjaAPI()

api.add_router("auth/", auth_router)
api.add_router("entities/", entity_router)
