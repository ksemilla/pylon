from django.db import models
from django.utils.translation import gettext_lazy as _

from pylon.core.models import StampedModel

from pylon.customers.models import Customer
from pylon.inventory.models import Inventory

class Quotation(StampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=512, blank=True)
    notes = models.TextField(blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)

class QuotationItem(StampedModel):
    class Types(models.TextChoices):
        STOCK = 's', _('Stock')
        LABOR = 'l', _('Labor')
        DOCUMENT = 'd', _('Document')
        ASSEMBLY = 'a', _('Assembly')

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=64, choices=Types.choices, default=Types.STOCK)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="quotation_item")
    quantity = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

class QuotationAssemblyItem(StampedModel):
    class Types(models.TextChoices):
        STOCK = 's', _('Stock')
        LABOR = 'l', _('Labor')
        DOCUMENT = 'd', _('Document')
    quotation_item = models.ForeignKey(QuotationItem, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=64, choices=Types.choices, default=Types.STOCK)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="quotationassembly_item")
    quantity = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']