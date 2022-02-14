import copy
from functools import partial
import json
from pylon.customers.serializers import CustomerAddressSerializer, CustomerContactSerializer, CustomerSerializer

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from pylon.users.models import User

from .models import (
    Customer,
    CustomerContact,
    CustomerAddress
)

class CustomerListCreateView(APIView):
    def get(self, request):
        queryset = Customer.objects.all()
        return Response(CustomerSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        data = copy.deepcopy(request.data)
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerRetrieveUpdateDestroy(APIView):
    def get(self, request, customer_id):
        customer = Customer.objects.get(pk=customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerContactListCreateView(APIView):
    def post(self, request, customer_id):
        data = copy.deepcopy(request.data)
        data['customer'] = customer_id
        serializer = CustomerContactSerializer(data=data)
        if serializer.is_valid():
            customer_contact = serializer.save()
            return Response(CustomerContactSerializer(customer_contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerContactRetrieveUpdateDestroyView(APIView):
    def put(self, request, customer_id, contact_id):
        customer_contact = CustomerContact.objects.get(pk=contact_id)
        data = copy.deepcopy(request.data)
        data['customer'] = customer_id
        serializer = CustomerContactSerializer(customer_contact, data=data, partial=True)
        if serializer.is_valid():
            customer_contact = serializer.save()
            return Response(CustomerContactSerializer(customer_contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerAddressListCreateView(APIView):
    def post(self, request, customer_id):
        data = copy.deepcopy(request.data)
        data['customer'] = customer_id
        serializer = CustomerAddressSerializer(data=data)
        if serializer.is_valid():
            customer_address = serializer.save()
            return Response(CustomerAddressSerializer(customer_address).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerAddressRetrieveUpdateDestroyView(APIView):
    def put(self, request, customer_id, address_id):
        customer_address = CustomerAddress.objects.get(pk=address_id)
        data = copy.deepcopy(request.data)
        data['customer'] = customer_id
        serializer = CustomerAddressSerializer(customer_address, data=data, partial=True)
        if serializer.is_valid():
            customer_address = serializer.save()
            return Response(CustomerAddressSerializer(customer_address).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)