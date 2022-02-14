from rest_framework import serializers
from rest_framework import validators
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

    def validate_code(self, value):
        obj = Vendor.objects.filter(code__iexact=value).first()
        if self.instance:
            if obj.id != self.instance.id:
                raise validators.ValidationError("Code must be unique")
        else:
            if obj:
                raise validators.ValidationError("Code must be unique")
        return value

class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = (
            'id', 'vendor', 'is_primary', 'address1', 'address2', 'city', 'state', 'country', 'postal_code'
        )

    def create(self, validated_data):
        vendor_address = VendorAddress.objects.create(**validated_data)
        if vendor_address.is_primary:
            for obj in vendor_address.vendor.vendoraddress_set.all():
                if obj.id != vendor_address.id:
                    obj.is_primary = False
                    obj.save()
        return vendor_address

    def update(self, instance, validated_data):
        if validated_data["is_primary"]:
            for obj in instance.vendor.vendoraddress_set.all():
                if obj.id != instance.id:
                    obj.is_primary = False
                    obj.save()
        return super().update(instance, validated_data)

class VendorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContact
        fields = (
            'id', 'vendor', 'name', 'phone', 'email'
        )