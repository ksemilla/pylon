from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import (
    Vendor,
    VendorAddress,
    VendorContact
)

class VendorSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        queryset = obj.vendoraddress_set.all()
        return VendorAddressSerializer(queryset, many=True).data

    def get_contacts(self, obj):
        queryset = obj.vendorcontact_set.all()
        return VendorContactSerializer(queryset, many=True).data

    class Meta:
        model = Vendor
        fields = (
            'id', 'status', 'code', 'name', 'email', 'phone', 'addresses', 'contacts'
        )

class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = (
            'id', 'is_primary', 'address1', 'address2', 'city', 'state', 'country', 'postal_code'
        )

class VendorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContact
        fields = (
            'id', 'name', 'phone', 'email'
        )