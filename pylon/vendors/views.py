import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from pylon.users.models import User

from .models import (
    Vendor
)

from .serializers import (
    VendorSerializer
)

class VendorListCreateView(APIView):
    def get(self, request):

        queryset = Vendor.objects.filter(status="a")

        return Response(
            VendorSerializer(queryset, many=True).data,
            status=status.HTTP_200_OK
        )