from django.contrib import admin

from .models import (
    Stock,
    StockInstance,
    Labor,
    Document,
    Assembly,
    AssemblyItem
)

admin.site.register(Stock)
admin.site.register(StockInstance)
admin.site.register(Labor)
admin.site.register(Document)
admin.site.register(Assembly)
admin.site.register(AssemblyItem)
