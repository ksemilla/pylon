from rest_framework import serializers, validators

from pylon.vendors.serializers import VendorSerializer

from .models import (
    Inventory,
    InventoryInstance,
    InventoryVendor,
    Stock,
    Labor,
    Document,
    Assembly,
    AssemblyItem
)

class InventorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return AssemblyItemSerializer(obj.assemblyitem_set.all(), many=True).data

    class Meta:
        model = Inventory
        fields = (
            'id', 'status', 'type', 'part_number', 'name', 'description', 'unit', 'quantity', 'in_order', 'list_price', 'sell_price', 'items'
        )

    def validate_quantity(self, value):
        if self.instance.type == 'stock' and not value:
            raise validators.ValidationError("This is a required field for stocks")
        return value

class InventoryInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryInstance
        fields = (
            'id', 'inventory', 'description', 'quantity', 'location'
        )

class InventoryVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryVendor
        fields = (
            'id', 'inventory', 'vendor', 'list_price'
        )

class StockSerializer(serializers.ModelSerializer):
    instances = serializers.SerializerMethodField()
    vendors = serializers.SerializerMethodField()

    def get_instances(self, obj):
        return InventoryInstanceSerializer(obj.inventoryinstance_set.all(), many=True).data

    def get_vendors(self, obj):
        return InventoryVendorSerializer(obj.inventoryvendor_set.all(), many=True).data

    class Meta:
        model = Stock
        fields = (
            'id', 'status', 'part_number', 'name', 'description', 'unit', 'quantity', 'list_price', 'sell_price', 'type', 'in_order', 'instances', 'vendors'
        )

class LaborSerializer(serializers.ModelSerializer):
    instances = serializers.SerializerMethodField()
    vendors = serializers.SerializerMethodField()

    def get_instances(self, obj):
        return InventoryInstanceSerializer(obj.inventoryinstance_set.all(), many=True).data

    def get_vendors(self, obj):
        return InventoryVendorSerializer(obj.inventoryvendor_set.all(), many=True).data

    class Meta:
        model = Labor
        fields = (
            'id', 'part_number', 'name', 'description', 'unit', 'list_price', 'sell_price', 'type', 'vendors', 'instances'
        )

class DocumentSerializer(serializers.ModelSerializer):
    instances = serializers.SerializerMethodField()
    vendors = serializers.SerializerMethodField()

    def get_instances(self, obj):
        return InventoryInstanceSerializer(obj.inventoryinstance_set.all(), many=True).data

    def get_vendors(self, obj):
        return InventoryVendorSerializer(obj.inventoryvendor_set.all(), many=True).data

    class Meta:
        model = Document
        fields = (
            'id', 'part_number', 'name', 'description', 'unit', 'list_price', 'sell_price', 'type', 'vendors', 'instances'
        )

class AssemblyItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyItem
        fields = (
            'id', 'order', 'type', 'list_price', 'sell_price', 'item', 'quantity'
        )

    def to_internal_value(self, data):
        internal_value = super(AssemblyItemCreateSerializer, self).to_internal_value(data)
        item = data.get("item")
        internal_value.update({
            "item": item
        })
        return internal_value

    def validate(self, attrs):
        if not attrs["item"]:
            raise validators.ValidationError("Assembly item is not valid")
        else:
            item_obj = Inventory.objects.get(pk=attrs['item'])
            if item_obj.type == 'a':
                raise validators.ValidationError("Assembly item can not be an assembly")
        return super().validate(attrs)

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['item'] = InventorySerializer(instance.item).data
    #     return rep

class AssemblyItemSerializer(serializers.ModelSerializer):
    item_detail = serializers.SerializerMethodField()

    def get_item_detail(self, obj):
        return InventorySerializer(obj.item).data

    class Meta:
        model = AssemblyItem
        fields = (
            'id', 'assembly', 'order', 'type', 'list_price', 'sell_price', 'item', 'quantity', 'item_detail'
        )

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['item'] = InventorySerializer(instance.item).data
    #     return rep

class AssemblySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    instances = serializers.SerializerMethodField()
    vendors = serializers.SerializerMethodField()

    def get_items(self, obj):
        return AssemblyItemSerializer(obj.assemblyitem_set.all(), many=True).data

    def get_instances(self, obj):
        return InventoryInstanceSerializer(obj.inventoryinstance_set.all(), many=True).data
    
    def get_vendors(self, obj):
        return InventoryVendorSerializer(obj.inventoryvendor_set.all(), many=True).data

    class Meta:
        model = Assembly
        fields = (
            'id', 'status', 'part_number', 'name', 'description', 'unit', 'items', 'quantity', 'in_order', 'instances', 'vendors'
        )

    def validate(self, attrs):
        for item in attrs['items']:
            item_obj = None
            if "id" in item: # if object exsists
                item_obj = AssemblyItem.objects.filter(pk=item['id']).first()
            serializer = AssemblyItemCreateSerializer(item_obj, data=item)
            if not serializer.is_valid():
                print(serializer.errors)
                raise validators.ValidationError(f"Item {item['order']} is not valid")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('items')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('items')
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        internal_value = super(AssemblySerializer, self).to_internal_value(data)
        items = data.get("items")
        internal_value.update({
            "items": items
        })
        return internal_value



