from re import search
from rest_framework import serializers

from .models import (
    Stock,
    StockInstance,
    Labor,
    Document,
    Assembly,
    AssemblyItem
)

class StockSerializer(serializers.ModelSerializer):
    instances = serializers.SerializerMethodField()

    def get_instances(self, obj):
        queryset = obj.stockinstance_set.all()
        return StockInstanceSerializer(queryset, many=True).data

    class Meta:
        model = Stock
        fields = (
            'id', 'part_number', 'name', 'description', 'unit', 'quantity', 'list_price', 'sell_price', 'location', 'photo', 'instances'
        )

class StockInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInstance
        fields = (
            'id', 'description', 'quantity', 'location', 'photo'
        )

class LaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labor
        fields = (
            'id', 'part_number', 'name', 'description', 'unit', 'list_price', 'sell_price', 'photo'
        )

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id', 'part_number', 'name', 'description', 'unit', 'list_price', 'sell_price', 'photo', 'file'
        )

class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id', 'status', 'part_number', 'name', 'description', 'unit'
        )