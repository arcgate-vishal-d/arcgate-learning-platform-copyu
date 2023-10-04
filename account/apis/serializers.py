import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from account.models import UserData, Project, UserPermission
from django.contrib.auth.models import User
from rest_framework import status


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not re.match("^[a-z0-9_]{5,20}$", username):
            raise serializers.ValidationError(
                "Username must contain only small letters, numbers, and underscores and 5 to 20 characters long."
            )

        if password:
            regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
            pattern = re.compile(regular_expression)
            valid1 = re.search(pattern, password)
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
        fields = ["project_name"]


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ["read", "delete", "update"]


class UserListingSerializer(serializers.ModelSerializer):
    permission = PermissionsSerializer()
    username = serializers.CharField(source="users.username")
    emp_id = serializers.CharField(source="permission.emp_id")
    project = serializers.CharField(source="project.project_name")

    class Meta:
        model = UserData
        fields = [
            "username",
            "emp_id",
            "project",
            "status",
            "permission",
        ]
