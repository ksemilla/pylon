from django.contrib import admin

from .models import (
    Vendor,
    VendorContact,
    VendorAddress
)

class VendorAddressInline(admin.StackedInline):
    model = VendorAddress
    extra = 2

class VendorContactInline(admin.StackedInline):
    model = VendorContact
    extra = 2

class VendorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id']}),
        ('General Info', {'fields': ['status', 'code', 'name', 'email', 'phone']})
    ]
    inlines = [VendorAddressInline, VendorContactInline]
    readonly_fields = ['id']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorContact)
admin.site.register(VendorAddress)