from ninja import ModelSchema

from .models import Entity


class EntitySchema(ModelSchema):
    class Meta:
        model = Entity
        fields = "__all__"
