import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from account.models import UserData, Project, UserPermission


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Username validations
        if not re.match("^[a-z0-9_]{4,20}$", username):
            raise ValidationError(
                "Username must contain only small letters, numbers, and underscores and be between 6 to 20 characters long."
            )

        # Password validation
        min_length = 8
        if len(password) < min_length:
            raise serializers.ValidationError(
                f"Password must be at least {min_length} characters long."
            )

        if not any(char.isupper() for char in password) or not any(
            char.islower() for char in password
        ):
            raise serializers.ValidationError(
                "Password must contain both uppercase and lowercase letters."
            )

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one numeric character."
            )

        special_characters = "!@#$%^&*()-_+=[]{}|;:,.<>?/'\""
        if not any(char in special_characters for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ["read", "write", "delete", "update"]


class AdminViewSerializer(serializers.ModelSerializer):
    permission = PermissionsSerializer()

    class Meta:
        model = UserData
        fields = [
            "permission",
        ]
