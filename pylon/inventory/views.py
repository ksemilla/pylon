import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from pylon.users.models import User

from .models import (
    Stock,
    Labor,
    Document,
    Assembly
)

from .serializers import (
    AssemblySerializer,
    DocumentSerializer,
    LaborSerializer,
    StockSerializer,
)

class InventoryListView(APIView):
    def get(self, request):

        stocks = Stock.objects.filter(status="a")
        labors = Labor.objects.filter(status="a")
        documents = Document.objects.filter(status="a")
        assemblys = Assembly.objects.filter(status="a")

        queryset = StockSerializer(stocks, many=True).data + LaborSerializer(labors, many=True).data + DocumentSerializer(documents, many=True).data + AssemblySerializer(assemblys, many=True).data
        
        return Response(
            queryset,
            status=status.HTTP_200_OK
        )