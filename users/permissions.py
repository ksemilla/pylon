from core.permissions import BasePermission
from .models import User


class AdminOrSelfPermission(BasePermission):
    message = "Only the user or an admin has permission"

    def has_permission(request, *args, **kwargs) -> bool:
        id = kwargs.get("user_id", 0)
        return request.user.role == User.Roles.ADMIN or request.user.id == id
