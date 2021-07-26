import copy

from django.contrib.auth import get_user_model

from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
)

from .utils import (
    user_exists,
)

User = get_user_model()

class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if user_exists(request.data['email']):
            return Response(
                {'error': 'Email is already in use'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = copy.deepcopy(request.data)
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            # token = TokenObtainPairSerializer(user).validate(UserSerializer(user).data)
            # token['user'] = UserSerializer(user).data
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
