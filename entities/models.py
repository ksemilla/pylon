from django.db import models

from core.models import StampedModel


class Entity(StampedModel):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=256, blank=True)
