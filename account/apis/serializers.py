import re
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from account.models import User, UserData, Project, Role, Permission


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise serializers.ValidationError("Invalid email format")

        if password:
            regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
            pattern = re.compile(regular_expression)
            valid1 = re.search(pattern, password)
            if not valid1:
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
    role = serializers.CharField(source="get_role_display")

    def get_role_display(self):
        return dict(Role.ROLE_CHOICES).get(self.role)

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
    # role = serializers.CharField(source='get_role_display')
    # status = serializers.ChoiceField(choices=UserData.STATUS_CHOICES)
    # role = RoleSerializer()
    # role = serializers.CharField(source="role.role")
    role = serializers.CharField(source="role.get_role_display")
    # status = serializers.CharField(source='get_status_display')

    class Meta:
        model = UserData
        fields = [
            "employee_id",
            "user_id",
            "full_name",
            "project",
            "role",
            "status",
            "permissions",
        ]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": {"Token is expired or Invalid"}}

    def save(self, *args, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
