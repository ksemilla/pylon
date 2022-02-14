import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from pylon.users.models import User

from .models import (
    AssemblyItem,
    Inventory,
    InventoryInstance,
    InventoryVendor,
    Stock,
    Labor,
    Document,
    Assembly,
)

from .serializers import (
    AssemblyItemSerializer,
    AssemblySerializer,
    InventorySerializer,
    InventoryInstanceSerializer,
    InventoryVendorSerializer,
    StockSerializer,
    LaborSerializer,
    DocumentSerializer,
)

class InventoryListCreateView(APIView):
    def get(self, request):
        # queryset = Inventory.objects.filter(status="a")
        queryset = Inventory.objects.all()
        return Response(
            InventorySerializer(queryset, many=True).data,
            status=status.HTTP_200_OK
        )

class StockCreateAPIView(APIView):
    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            stock = serializer.save()

            data['inventory'] = stock.id

            serializer = InventoryInstanceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            

            return Response(StockSerializer(stock).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockRetrieveUpdateDestroyView(APIView):
    def get(self, request, stock_id):
        stock = Inventory.objects.get(pk=stock_id)
        return Response(StockSerializer(stock).data, status=status.HTTP_200_OK)

    def put(self, request, stock_id):
        stock = Inventory.objects.get(pk=stock_id)
        data = copy.deepcopy(request.data)
        serializer = StockSerializer(stock, data=data)
        if serializer.is_valid():
            stock = serializer.save()
            return Response(StockSerializer(stock).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockInstanceListCreateView(APIView):
    def post(self, request, stock_id):
        data = copy.deepcopy(request.data)
        stock = Inventory.objects.get(pk=stock_id)
        data['inventory'] = stock.id
        serializer = InventoryInstanceSerializer(data=data)
        if serializer.is_valid():
            stock_instance = serializer.save()
            return Response(InventoryInstanceSerializer(stock_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockInstanceRetrieveUpdateDestroyView(APIView):
    def put(self, request, stock_id, pk):
        stock_instance = InventoryInstance.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryInstanceSerializer(stock_instance, data=data)
        if serializer.is_valid():
            stock_instance = serializer.save()
            return Response(InventoryInstanceSerializer(stock_instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockVendorListCreateView(APIView):
    def post(self, request, stock_id):
        data = copy.deepcopy(request.data)
        stock = Inventory.objects.get(pk=stock_id)
        data['inventory'] = stock.id
        serializer = InventoryVendorSerializer(data=data)
        if serializer.is_valid():
            stock_vendor = serializer.save()
            return Response(InventoryVendorSerializer(stock_vendor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockVendorRetrieveUpdateDestroyView(APIView):
    def put(self, request, stock_id, pk):
        stock_vendor = InventoryVendor.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryVendorSerializer(stock_vendor, data=data)
        if serializer.is_valid():
            stock_vendor = serializer.save()
            return Response(InventoryVendorSerializer(stock_vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaborListCreateView(APIView):
    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = LaborSerializer(data=data)
        if serializer.is_valid():
            labor = serializer.save()
            return Response(LaborSerializer(labor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaborRetrieveUpdateDestroyView(APIView):
    def get(self, request, labor_id):
        labor = Inventory.objects.get(pk=labor_id)
        return Response(LaborSerializer(labor).data, status=status.HTTP_200_OK)

    def put(self, request, labor_id):
        labor = Labor.objects.get(pk=labor_id)
        data = copy.deepcopy(request.data)
        serializer = LaborSerializer(labor, data=data)
        if serializer.is_valid():
            labor = serializer.save()
            return Response(LaborSerializer(labor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaborVendorListCreateView(APIView):
    def post(self, request, labor_id):
        data = copy.deepcopy(request.data)
        labor = Inventory.objects.get(pk=labor_id)
        data['inventory'] = labor.id
        serializer = InventoryVendorSerializer(data=data)
        if serializer.is_valid():
            labor_vendor = serializer.save()
            return Response(InventoryVendorSerializer(labor_vendor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaborVendorRetrieveUpdateDestroyView(APIView):
    def put(self, request, labor_id, pk):
        labor_vendor = InventoryVendor.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryVendorSerializer(labor_vendor, data=data)
        if serializer.is_valid():
            labor_vendor = serializer.save()
            return Response(InventoryVendorSerializer(labor_vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentListCreateView(APIView):
    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            document = serializer.save()
            
            return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     

class DocumentRetrieveUpdateDestroyView(APIView):
    def get(self, request, document_id):
        document = Inventory.objects.get(pk=document_id)
        return Response(DocumentSerializer(document).data, status=status.HTTP_200_OK)

    def put(self, request, document_id):
        document = Inventory.objects.get(pk=document_id)
        data = copy.deepcopy(request.data)
        serializer = DocumentSerializer(document, data=data)
        if serializer.is_valid():
            document = serializer.save()
            return Response(DocumentSerializer(document).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentVendorListCreateView(APIView):
    def post(self, request, document_id):
        data = copy.deepcopy(request.data)
        document = Inventory.objects.get(pk=document_id)
        data['inventory'] = document.id
        serializer = InventoryVendorSerializer(data=data)
        if serializer.is_valid():
            document_vendor = serializer.save()
            return Response(InventoryVendorSerializer(document_vendor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentVendorRetrieveUpdateDestroyView(APIView):
    def put(self, request, document_id, pk):
        document_vendor = InventoryVendor.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryVendorSerializer(document_vendor, data=data)
        if serializer.is_valid():
            document_vendor = serializer.save()
            return Response(InventoryVendorSerializer(document_vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyListCreateView(APIView):
    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = AssemblySerializer(data=data)
        if serializer.is_valid():
            assembly = serializer.save()

            if 'items' in data:
                for item in data['items']:
                    item['assembly'] = assembly.id
                    serializer = AssemblyItemSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()

            return Response(AssemblySerializer(assembly).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyRetrieveUpdateDestroyView(APIView):
    def get(self, request, assembly_id):
        assembly = Inventory.objects.get(pk=assembly_id)
        return Response(AssemblySerializer(assembly).data, status=status.HTTP_200_OK)

    def put(self, request, assembly_id):
        assembly = Inventory.objects.get(pk=assembly_id)
        data = copy.deepcopy(request.data)
        serializer = AssemblySerializer(assembly, data=data)
        if serializer.is_valid():
            assembly = serializer.save()

            if 'items' in data:
                for item in data['items']:
                    item_obj = AssemblyItem.objects.get(pk=item['id']) if 'id' in item else None
                    item['assembly'] = assembly.id
                    serializer = AssemblyItemSerializer(item_obj, data=item)
                    if serializer.is_valid():
                        serializer.save()

            return Response(AssemblySerializer(assembly).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyInstanceListCreateView(APIView):
    def post(self, request, assembly_id):
        data = copy.deepcopy(request.data)
        assembly = Inventory.objects.get(pk=assembly_id)
        data['inventory'] = assembly.id
        serializer = InventoryInstanceSerializer(data=data)
        if serializer.is_valid():
            assembly_instance = serializer.save()
            return Response(InventoryInstanceSerializer(assembly_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyInstanceRetrieveUpdateDestroyView(APIView):
    def put(self, request, assembly_id, pk):
        assembly_instance = InventoryInstance.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryInstanceSerializer(assembly_instance, data=data)
        if serializer.is_valid():
            assembly_instance = serializer.save()
            return Response(InventoryInstanceSerializer(assembly_instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyVendorListCreateView(APIView):
    def post(self, request, assembly_id):
        data = copy.deepcopy(request.data)
        assembly = Inventory.objects.get(pk=assembly_id)
        data['inventory'] = assembly.id
        serializer = InventoryVendorSerializer(data=data)
        if serializer.is_valid():
            assembly_vendor = serializer.save()
            return Response(InventoryVendorSerializer(assembly_vendor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssemblyVendorRetrieveUpdateDestroyView(APIView):
    def put(self, request, assembly_id, pk):
        assembly_vendor = InventoryVendor.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = InventoryVendorSerializer(assembly_vendor, data=data)
        if serializer.is_valid():
            assembly_vendor = serializer.save()
            return Response(InventoryVendorSerializer(assembly_vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)