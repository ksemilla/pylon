from ninja.pagination import RouterPaginated
from ninja.errors import HttpError
from typing import List
from slugify import slugify

from django.db.models import Q

from core.permissions import permissions, AdminPermisison
from users.models import User

from .models import Entity, Member
from .schemas import (
    EntitySchema,
    EntityCreateSchema,
    MemberSchema,
    MemberCreateSchema,
    MemberEditSchema,
)
from .permissions import AdminOrMemberPermission

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
@permissions([AdminOrMemberPermission])
def get_entity(request, entity_id: int):
    try:
        return Entity.objects.get(id=entity_id)
    except Entity.DoesNotExist:
        return HttpError(404, "Entity not found")


@entity_router.get("{entity_id}/members/", response=List[MemberSchema])
def get_members(request, entity_id: int, q: str = ""):
    return Member.objects.filter(
        (Q(entity__id=entity_id) & Q(user__email__icontains=q))
    )


@entity_router.post("{entity_id}/members/", response=MemberSchema)
def create_member(request, entity_id: int, data: MemberCreateSchema):

    try:
        user = User.objects.get(email=data.email)
        Member.objects.get(entity__id=entity_id, user__id=user.id)
        raise HttpError(400, "Member already exists")
    except User.DoesNotExist:
        raise HttpError(400, "[DEMO] Email not found")
    except Member.DoesNotExist:
        user = User.objects.get(email=data.email)
        entity = Entity.objects.get(id=entity_id)

    return Member.objects.create(role=data.role, entity=entity, user=user)


@entity_router.get("{entity_id}/members/{member_id}/", response=MemberSchema)
def create_member(request, entity_id: int, member_id: int):
    try:
        return Member.objects.get(id=member_id, entity__id=entity_id)
    except Member.DoesNotExist:
        return HttpError(404, "Member not found")


@entity_router.put("{entity_id}/members/{member_id}/", response=str)
def create_member(request, entity_id: int, member_id: int, data: MemberEditSchema):
    try:
        member = Member.objects.get(id=member_id, entity__id=entity_id)
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(member, attr, value)

        member.save()
        return ""
    except Member.DoesNotExist:
        return HttpError(404, "Member not found")
