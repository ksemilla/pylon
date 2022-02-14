from django.db import models
from django.utils.translation import gettext_lazy as _

from pylon.core.models import StampedModel

class Customer(StampedModel):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=32)
    phone = models.CharField(max_length=128, blank=True)
    website = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    credit = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"

class CustomerContact(StampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name}"

class CustomerAddress(StampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True) # province/division/state
    country = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['-is_primary']