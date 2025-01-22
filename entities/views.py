from ninja import Form, File, UploadedFile
from ninja.pagination import RouterPaginated
from ninja.errors import HttpError
from typing import List
from slugify import slugify

from django.db.models import Q

from core.permissions import permissions, AdminPermisison

from .models import Entity
from .schemas import EntitySchema, EntityCreateSchema

entity_router = RouterPaginated()


@entity_router.get("", response=List[EntitySchema])
@permissions([AdminPermisison])
def entity_list_view(request, q: str = ""):
    return Entity.objects.filter(Q(name__icontains=q) | Q(slug__icontains=q))


@entity_router.post("", response=EntitySchema)
@permissions([AdminPermisison])
def entity_create_view(request, data: EntityCreateSchema):
    slug = slugify(data.name)
    _entity = Entity.objects.filter(slug=slug).first()
    if _entity:
        raise HttpError(400, "Cannot create entity - already used slug")
    return Entity.objects.create(**data.dict())


@entity_router.get("{entity_id}/", response=EntitySchema)
@permissions([AdminPermisison])
def get_entity(request, entity_id: int):
    try:
        return Entity.objects.get(id=entity_id)
    except Entity.DoesNotExist:
        return HttpError(404, "Entity not found")
