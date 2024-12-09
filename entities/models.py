from django.db import models
from slugify import slugify

from core.models import StampedModel


class Entity(StampedModel):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(kwargs["name"])
        super().save(*args, **kwargs)
