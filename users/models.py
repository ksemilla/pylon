from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPERUSER = "superuser", _("Super User")
        ADMIN = "admin", _("Admin")
        USER = "user", _("User")

    firebase_uid = models.CharField(max_length=256)
    role = models.CharField(max_length=64, choices=Roles, default=Roles.USER)
