from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    BooleanField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for pylon."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    is_frozen = BooleanField(default=False)
