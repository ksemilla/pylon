import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    QuotationSerializer,
    QuotationItemSerializer,
    QuotationAssemblyItemSerializer
)

from .models import (
    Quotation,
    QuotationItem,
    QuotationAssemblyItem
)

class QuotationListCreateView(APIView):
    def get(self, request):
        queryset = Quotation.objects.all()
        serializer = QuotationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuotationSerializer(data=request.data)
        if serializer.is_valid():
            quotation = serializer.save()
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuotationRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        quotation = Quotation.objects.filter(pk=pk).first()
        if quotation:
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        quotation = Quotation.objects.filter(pk=pk).first()

        serializer = QuotationSerializer(quotation, data=request.data)
        if serializer.is_valid():
            quotation = serializer.save()
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
