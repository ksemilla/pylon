from rest_framework import serializers, validators

from .models import (
    CustomerContact,
    Customer,
    CustomerAddress
)

class CustomerSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()

    def get_contacts(self, obj):
        return CustomerContactSerializer(obj.customercontact_set.all(), many=True).data

    def get_addresses(self, obj):
        return CustomerAddressSerializer(obj.customeraddress_set.all(), many=True).data

    class Meta:
        model = Customer
        fields = (
            'id', 'code', 'name', 'email', 'phone', 'website', 'discount', 'credit', 'addresses', 'contacts'
        )

class CustomerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContact
        fields = (
            'id', 'customer', 'name', 'email', 'phone'
        )

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = (
            'id', 'customer', "is_primary", 'address1', 'address2', 'city', 'state', 'country', 'postal_code'
        )

    def create(self, validated_data):
        customer_address = CustomerAddress.objects.create(**validated_data)
        if customer_address.is_primary:
            for obj in customer_address.customer.customeraddress_set.all():
                if obj.id != customer_address.id:
                    obj.is_primary = False
                    obj.save() 
        return customer_address

    def update(self, instance, validated_data):
        if validated_data["is_primary"]:
            for obj in instance.customer.customeraddress_set.all():
                if obj.id != instance.id:
                    obj.is_primary = False
                    obj.save()
        return super().update(instance, validated_data)