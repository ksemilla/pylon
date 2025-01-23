from core.permissions import BasePermission
from .models import Entity, Member


class AdminOrMemberPermission(BasePermission):
    message = "Only the user or an admin has permission"

    def has_permission(request, *args, **kwargs) -> bool:
        try:
            Member.objects.get(user__id=request.user.id, entity__id=kwargs["entity_id"])
            return True
        except:
            pass
        return False
