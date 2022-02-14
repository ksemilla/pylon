from django.contrib import admin

from .models import (
    Quotation,
    QuotationItem,
    QuotationAssemblyItem,
)

admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(QuotationAssemblyItem)