from django.db import models
from django.utils.translation import gettext_lazy as _

from pylon.core.models import StampedModel
from pylon.vendors.models import Vendor

class Stock(StampedModel):
    class Unit(models.TextChoices):
        EACH = 'e', _('Per Unit')
        LENGTH = 'l', _('Per Length')

    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    part_number = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.EACH)
    quantity = models.DecimalField(max_digits=32, decimal_places=4)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(blank=True)
    vendor = models.ManyToManyField(
        Vendor,
        blank=True,
    )

    def __str__(self):
        return self.part_number

class StockInstance(StampedModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=32, decimal_places=4)
    location = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(blank=True)

class Labor(StampedModel):
    class Unit(models.TextChoices):
        EACH = 'e', _('Per Unit')

    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    part_number = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.EACH)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    photo = models.ImageField(blank=True)

class Document(StampedModel):
    class Unit(models.TextChoices):
        EACH = 'e', _('Per Unit')
    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    part_number = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.EACH)
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    photo = models.ImageField(blank=True)
    file = models.FileField(blank=True)

class Assembly(StampedModel):
    class Unit(models.TextChoices):
        EACH = 'e', _('Per Unit')

    class Status(models.TextChoices):
        ACTIVE = 'a', _('Active')
        INACTIVE = 'i', _('Inactive')

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACTIVE)
    part_number = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.EACH)

class AssemblyItem(StampedModel):
    class Type(models.TextChoices):
        STOCK = 's', _('Stock')
        LABOR = 'l', _('Labor')
        DOCUMENT = 'd', _('Document')

    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    type = models.CharField(max_length=64, choices=Type.choices, default=Type.STOCK)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    list_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True, null=True)
