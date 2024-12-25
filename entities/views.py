from ninja import Form, File, UploadedFile
from ninja.pagination import RouterPaginated
from typing import List

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
def entity_create_view(
    request,
    data: Form[EntityCreateSchema],
    photo: File[UploadedFile] = None,
    icon: File[UploadedFile] = None,
):
    return Entity.objects.create(**data.dict(), photo=photo, icon=icon)
