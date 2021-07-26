from rest_framework import serializers

from .models import (
    User,
)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'password',
        )
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["username"] = validated_data.get("email")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'first_name', 'last_name', 'email'
        )