from ninja.pagination import RouterPaginated
from typing import List

from .models import Entity
from .schemas import EntitySchema

entity_router = RouterPaginated()


@entity_router.get("", response=List[EntitySchema])
def entity_list_view(request):
    return Entity.objects.all()
