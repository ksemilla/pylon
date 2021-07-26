from django.db import models
from django.utils.translation import gettext_lazy as _

from pylon.core.models import StampedModel

class Vendor(StampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, blank=True)
    phone = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name

class VendorContact(StampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name}"

class VendorAddress(StampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True) # province/division/state
    country = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)