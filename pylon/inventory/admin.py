from django.contrib import admin

from .models import (
    Inventory,
    InventoryInstance,
    Stock,
    Labor,
    Document,
    Assembly,
    AssemblyItem
)

admin.site.register(InventoryInstance)
# admin.site.register(Stock)
# admin.site.register(Assembly)
admin.site.register(Inventory)
admin.site.register(AssemblyItem)
# admin.site.register(StockInstance)
# admin.site.register(StockVendor)
# admin.site.register(Labor)
# admin.site.register(Document)
# admin.site.register(Assembly)
# admin.site.register(AssemblyItem)
