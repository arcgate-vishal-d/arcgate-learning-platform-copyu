from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from account.models import User_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

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


class AdminViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_data
        fields = "__all__"