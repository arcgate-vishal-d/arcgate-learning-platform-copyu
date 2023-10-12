import re
from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from account.models import User, UserData, Project, Role, Permission


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "is_active", "first_name", "last_name", "email")


class UserDatasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["read", "delete", "update"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("role",)


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("project_name",)


class PermissionsSerializer(serializers.ModelSerializer):
    permissions = UserDatasSerializer()
    user_id = serializers.CharField(source="users.id")
    employee_id = serializers.CharField(source="users.employee_id", read_only=True)

    project = serializers.CharField(source="project.project_name")
    role = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(choices=UserData.STATUS_CHOICES)

    class Meta:
        model = UserData
        fields = [
            "employee_id",
            "user_id",
            "fullname",
            "project",
            "role",
            "status",
            "permissions",
        ]
