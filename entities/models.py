from django.db import models
from slugify import slugify
from django.utils.translation import gettext_lazy as _

from core.models import StampedModel
from users.models import User


class Entity(StampedModel):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=256, unique=True, null=True)
    photo = models.FileField(upload_to="uploads/", blank=True, null=True)
    icon = models.FileField(upload_to="uploads/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Member(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "admin", _("Admin")
        USER = "user", _("User")

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=Roles, default=Roles.USER)
