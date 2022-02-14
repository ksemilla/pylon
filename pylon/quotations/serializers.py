from rest_framework import serializers, validators

from pylon.customers.serializers import (
    CustomerSerializer
)

from pylon.users.serializers import UserSerializer
from pylon.inventory.serializers import InventorySerializer

from .models import (
    Quotation,
    QuotationItem,
    QuotationAssemblyItem
)

class QuotationSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer_detail = serializers.SerializerMethodField()

    def get_items(self, obj):
        return QuotationItemSerializer(obj.quotationitem_set.all(), many=True).data

    def get_customer_detail(self, obj):
        return CustomerSerializer(obj.customer).data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = UserSerializer(instance.created_by).data
        return rep
        
    class Meta:
        model = Quotation
        fields = (
            'id', 'customer', 'discount', 'address', 'notes', 'items', 'created', 'customer_detail', 'valid_until', 'created_by'
        )
        read_only_fields = ['id', 'created_by']

    def validate(self, attrs):
        print("zax")
        for item in attrs['items']:
            serializer = QuotationItemSerializer(data=item)
            if serializer.is_valid():
                print("YAY")
            else:
                print(serializer.errors)
                raise validators.ValidationError(f"invalid quotation is not valid")
        return super().validate(attrs)

    def to_internal_value(self, data):
        internal_value = super(QuotationSerializer, self).to_internal_value(data)
        items = data.get("items")
        internal_value.update({
            "items": items
        })
        return internal_value

    def create(self, validated_data):
        quotation_items = validated_data.pop("items")
        quotation = Quotation.objects.create(**validated_data)
        quotation.save()

        for item in quotation_items:
            serializer = QuotationItemSerializer(data=item)
            if serializer.is_valid():
                quotation_item = serializer.save(quotation=quotation)
                # quotation_item.quotation = quotation.id
                # quotation_item.save()

        return quotation

    def update(self, instance, validated_data):
        quotation_items = validated_data.pop("items")
        quotation = super(QuotationSerializer,self).update(instance, validated_data)

        retain_ids = []
        for item in quotation_items:
            quotation_item = QuotationItem.objects.filter(pk=item['id']).first() if 'id' in item else None
            serializer = QuotationItemSerializer(quotation_item, data=item)
            if serializer.is_valid():
                quotation_item = serializer.save(quotation=quotation)
                retain_ids.append(quotation_item.id)

        for item in quotation.quotationitem_set.all():
            if item.id not in retain_ids:
                item.delete()

        quotation.save()

        return quotation

class QuotationItemSerializer(serializers.ModelSerializer):
    item_detail = serializers.SerializerMethodField()
    assembly_items = serializers.SerializerMethodField()

    def get_item_detail(self, obj):
        return InventorySerializer(obj.item).data

    def get_assembly_items(self, obj):
        return QuotationAssemblyItemSerializer(obj.quotationassemblyitem_set.all(), many=True).data

    class Meta:
        model = QuotationItem
        fields = (
            'id', 'quotation', 'order', 'type', 'item', 'quantity', 'list_price', \
            'sell_price', 'discount', 'description', 'item_detail', 'assembly_items'
        )
        read_only_fields = ['id', 'quotation']

    def validate(self, attrs):
        for item in attrs['assembly_items']:
            serializer = QuotationAssemblyItemSerializer(data=item)
            if serializer.is_valid():
                pass
            else:
                print(item, serializer.errors)
                raise validators.ValidationError(f"invalid quotation item is not valid")
        return super().validate(attrs)

    def to_internal_value(self, data):
        internal_value = super(QuotationItemSerializer, self).to_internal_value(data)
        assembly_items = data.get("assembly_items")
        internal_value.update({
            "assembly_items": assembly_items
        })
        return internal_value

    def create(self, validated_data):
        assembly_items = validated_data.pop("assembly_items")
        quotation_item = QuotationItem.objects.create(**validated_data)
        quotation_item.save()

        for assembly_item in assembly_items:
            serializer = QuotationAssemblyItemSerializer(data=assembly_item)
            if serializer.is_valid():
                assembly_item_obj = serializer.save(quotation_item=quotation_item)

        return quotation_item

    def update(self, instance, validated_data):
        assembly_items = validated_data.pop("assembly_items")
        quotation_item = super(QuotationItemSerializer,self).update(instance, validated_data)

        retain_ids = []
        for item in assembly_items:
            assembly_item = QuotationAssemblyItem.objects.filter(pk=item['id']).first() if 'id' in item else None
            serializer = QuotationAssemblyItemSerializer(assembly_item, data=item)
            if serializer.is_valid():
                assembly_item = serializer.save(quotation_item=quotation_item)
                retain_ids.append(assembly_item.id)

        for item in quotation_item.quotationassemblyitem_set.all():
            if item.id not in retain_ids:
                item.delete()

        quotation_item.save()

        return quotation_item

class QuotationAssemblyItemSerializer(serializers.ModelSerializer):
    item_detail = serializers.SerializerMethodField()

    def get_item_detail(self, obj):
        return InventorySerializer(obj.item).data

    class Meta:
        model = QuotationAssemblyItem
        fields = (
            'id', 'quotation_item', 'order', 'type', 'item', 'quantity', 'list_price', \
            'sell_price', 'discount', 'description', 'item_detail'
        )
        read_only_fields = ['id', 'quotation_item']

    # def create(self, validated_data):
    #     quotation_assembly_item = QuotationAssemblyItem.objects.create(**validated_data)
    #     quotation_assembly_item.save()
    #     return quotation_assembly_item