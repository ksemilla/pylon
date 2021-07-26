from django.shortcuts import render

# Create your views here.
import copy
import jwt

from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from config import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


from .serializers import CustomTokenObtainPairSerializer, CustomVerifyTokenSerializer, CustomRefreshTokenSerializer
from pylon.users.models import User
from pylon.users.serializers import UserSerializer

class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):

        data = copy.deepcopy(request.data)
        user = User.objects.filter(username=data["username"]).first() if "username" in data else None

        token = TokenObtainPairSerializer(user).validate(data)

        if token and user.is_frozen is False:
            token["user"] = UserSerializer(user, context={'request': request}).data
            token["valid"] = True
            return Response(token, status=200)
        elif token and user.is_frozen is True:
            context = {
                "valid": False,
                "error": "This account is frozen"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Make sure to enter correct credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CustomVerifyTokenView(TokenVerifyView):
    serializer_class = CustomVerifyTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = copy.deepcopy(request.data)
            # decoded = jwt.decode(data['token'], settings.local.SECRET_KEY)
            decoded = jwt.decode(data['token'], settings.base.env("DJANGO_SECRET_KEY", default="yI2JP8AYvRNbp5eP9EXerNQizS1uaYWco1YVQ9GapvNODdocm1HFdJJtnrsveR9p"), algorithms=["HS256"])
            user = User.objects.get(id=decoded['user_id'])
            user.last_login = timezone.now()
            user.save()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        temp_data = serializer.validated_data
        temp_data['user'] = UserSerializer(user, context={'request': request}).data

        return Response(temp_data, status=status.HTTP_200_OK)

class CustomRefreshVerifyTokenView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer