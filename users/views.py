from ninja.pagination import RouterPaginated
from typing import List

from .models import User
from .schemas import UserSchema


user_router = RouterPaginated()


@user_router.get("", response=List[UserSchema])
def user_list(request):
    return User.objects.all()
