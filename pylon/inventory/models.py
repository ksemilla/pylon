from django.db import models
from django.utils.translation import gettext_lazy as _

from pylon.core.models import StampedModel
from pylon.vendors.models import Vendor

class Inventory(StampedModel):
    class Types(models.TextChoices):
        STOCK = 's', _('Stock')
        LABOR = 'l', _('Labor')
        DOCUMENT = 'd', _('Document')
        ASSEMBLY = 'a', _('Assembly')

    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    class Unit(models.TextChoices):
        EACH = 'e', _('Per Unit')
        LENGTH = 'l', _('Per Length')

    type = models.CharField(max_length=64, choices=Types.choices, default=Types.STOCK)
    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    part_number = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.EACH)

    quantity = models.DecimalField(max_digits=32, decimal_places=4, null=True)
    in_order = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)

    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        ordering = ["part_number"]

    def __str__(self):
        return f"{self.part_number} - {self.id}"

class InventoryInstance(StampedModel):
    inventory = models.ForeignKey(Inventory , on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=32, decimal_places=4)
    location = models.CharField(max_length=128, blank=True)
    # photo = models.ImageField(blank=True, null=True)

class InventoryVendor(StampedModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)

class StockManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Inventory.TYPES.STOCK)

class LaborManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Inventory.TYPES.LABOR)

class DocumentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Inventory.TYPES.DOCUMENT)

class AssemblyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Inventory.TYPES.ASSEMBLY)

class Stock(Inventory):
    objects = StockManager

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Inventory.Types.STOCK
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True
    

class Labor(Inventory):
    objects = LaborManager
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Inventory.Types.LABOR
        return super().save(*args, **kwargs)

class Document(Inventory):
    objects = DocumentManager
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Inventory.Types.DOCUMENT
        return super().save(*args, **kwargs)

class Assembly(Inventory):
    objects = AssemblyManager
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Inventory.Types.ASSEMBLY
        return super().save(*args, **kwargs)

class AssemblyItem(StampedModel):
    class Types(models.TextChoices):
        STOCK = 's', _('Stock')
        LABOR = 'l', _('Labor')
        DOCUMENT = 'd', _('Document')

    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=64, choices=Types.choices, default=Types.STOCK)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="assembly_item")
    quantity = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

class AssemblyItemStockManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=AssemblyItem.TYPES.STOCK)

class AssemblyItemLaborManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=AssemblyItem.TYPES.LABOR)

class AssemblyItemDocumentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=AssemblyItem.TYPES.DOCUMENT)

class AssemblyItemStock(Inventory):
    objects = AssemblyItemStockManager
    class Meta:
        proxy = True

class AssemblyItemLabor(Inventory):
    objects = AssemblyItemLaborManager
    class Meta:
        proxy = True

class AssemblyItemDocument(Inventory):
    objects = AssemblyItemDocumentManager
    class Meta:
        proxy = True