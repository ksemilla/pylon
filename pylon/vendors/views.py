import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from pylon.users.models import User

from .models import (
    Vendor,
    VendorAddress,
    VendorContact,
)

from .serializers import (
    VendorAddressSerializer,
    VendorSerializer,
    VendorContactSerializer,
)

class VendorListCreateView(APIView):
    def get(self, request):
        queryset = Vendor.objects.filter(status="a")
        return Response(
            VendorSerializer(queryset, many=True).data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(VendorSerializer(vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        data = copy.deepcopy(request.data)
        serializer = VendorSerializer(vendor, data=data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(VendorSerializer(vendor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorAddressCreateView(APIView):
    def post(self, request, vendor_id):
        data = copy.deepcopy(request.data)
        data['vendor'] = vendor_id
        serializer = VendorAddressSerializer(data=data)
        if serializer.is_valid():
            vendor_address = serializer.save()
            return Response(VendorAddressSerializer(vendor_address).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorAddressRetrieveUpdateDestroyView(APIView):
    def put(self, request, vendor_id, pk):
        data = copy.deepcopy(request.data)
        data['vendor'] = vendor_id
        vendor_address = VendorAddress.objects.get(pk=pk)
        serializer = VendorAddressSerializer(vendor_address, data=data)
        if serializer.is_valid():
            vendor_address = serializer.save()
            return Response(VendorAddressSerializer(vendor_address).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorContactCreateView(APIView):
    def post(self, request, vendor_id):
        data = copy.deepcopy(request.data)
        data['vendor'] = vendor_id
        serializer = VendorContactSerializer(data=data)
        if serializer.is_valid():
            vendor_contact = serializer.save()
            return Response(VendorContactSerializer(vendor_contact).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorContactRetrieveUpdateDestroyView(APIView):
    def put(self, request, vendor_id, pk):
        data = copy.deepcopy(request.data)
        data['vendor'] = vendor_id
        vendor_contact = VendorContact.objects.get(pk=pk)
        serializer = VendorContactSerializer(vendor_contact, data=data)
        if serializer.is_valid():
            vendor_contact = serializer.save()
            return Response(VendorContactSerializer(vendor_contact).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)