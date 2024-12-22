from ninja import Form, File, UploadedFile
from ninja.pagination import RouterPaginated
from typing import List

from .models import Entity
from .schemas import EntitySchema, EntityCreateSchema

entity_router = RouterPaginated()


@entity_router.get("", response=List[EntitySchema])
def entity_list_view(request):
    return Entity.objects.all()


@entity_router.post("", response=EntitySchema)
def entity_create_view(
    request,
    data: Form[EntityCreateSchema],
    photo: File[UploadedFile] = None,
    icon: File[UploadedFile] = None,
):

    entity = Entity.objects.create(**data.dict(), photo=photo, icon=icon)

    print(entity.photo.path, entity.photo.url)

    return entity
