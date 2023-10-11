import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from account.models import User, UserData, Project, Role, Permission


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise serializers.ValidationError("Invalid email format")
        if password:
            regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
            pattern = re.compile(regular_expression)
            validations = re.search(pattern, password)
            if not validations:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long, uppercase and lowercase letters,one numeric character and special character"
                )

        user = authenticate(email=email, password=password)
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
    permission = UserDatasSerializer()
    username = serializers.CharField(source="users.username", read_only=True)
    user_id = serializers.CharField(source="users.id", read_only=True)
    project = serializers.CharField(source="project.project_name")
    role = serializers.StringRelatedField(read_only=True)
    fullname = serializers.SerializerMethodField(
        method_name="get_fullname", read_only=True
    )

    class Meta:
        model = UserData
        fields = [
            "user_id",
            "username",
            "fullname",
            "project",
            "role",
            "status",
            "permission",
        ]

    def get_fullname(self, obj):
        return f"{obj.users.first_name} {obj.users.last_name}"
