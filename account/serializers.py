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

        if not re.match("^[a-z0-9_]{5,20}$", username):
            raise serializers.ValidationError(
                "Username must contain only small letters, numbers, and underscores and be between 5 to 20 characters long."
            )
        if password:
            regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

            # compiling regex to create regex object

            pattern = re.compile(regular_expression)

            # searching regex

            valid1 = re.search(pattern, password)

            # validating conditions

            if not valid1:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long, uppercase and lowercase letters,one numeric character and special character"
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
