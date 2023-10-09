import re
from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from account.models import User, UserPermission, Project, Role, UserData

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
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
        fields = ('username',"is_active", 'first_name','last_name','email')


class PermissionsSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    role = serializers.StringRelatedField(read_only=True)
    user_id = serializers.StringRelatedField(source="users.id")
    # print(user.username)
    # project = serializers.CharField(source="project.project_name")
    class Meta:
        model = UserPermission
        fields = ('id', 'project', 'user_id','role', 'read', 'delete', 'update')

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_name',)


class UserDataSerializer(serializers.ModelSerializer):
    permission = PermissionsSerializer()
    project = ProjectsSerializer()

    class Meta:
        model = UserData
        fields = ('id','user', 'project', 'permission', 'role', 'status')


class AdminDetailSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField()
    status = serializers.IntegerField()
    permission = PermissionsSerializer()  # Display status choices as integers
    project = ProjectsSerializer()
    class Meta:
        model = UserData
        fields = ("users", "status", "project","permission")



# import re
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from account.models import UserData, Project, UserPermission


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")

       
#         if password:
#             regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
#             pattern = re.compile(regular_expression)
#             valid1 = re.search(pattern, password)
#             if not valid1:
#                 raise serializers.ValidationError(
#                     "Password must be at least 8 characters long, uppercase and lowercase letters,one numeric character and special character"
#                 )

#         user = authenticate(username=username, password=password)
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")

#         data["user"] = user
#         return data


# class ProjectsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ["project_name"]


# class PermissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPermission
#         fields = ["emp_id","read", "delete", "update"]


# class AdminViewSerializer(serializers.ModelSerializer):
#     # status = serializers.SerializerMethodField()
#     # permission = PermissionsSerializer()
#     # # username = serializers.CharField(source="users.username")
#     # # emp_id = serializers.CharField(source="permission.emp_id")
#     # project = serializers.CharField(source="project.project_name")

#     class Meta:
#         model = UserData
#         fields = '__all__'

#     def get_status(self, obj):
#         return "active" if obj.status == 1 else "inactive"


#     def update(self, instance, validated_data):
#         print(validated_data)

#         instance.fullName = validated_data.get('fullName', instance.fullName)
#         # instance.emp_id = validated_data.get('emp_id', instance.emp_id)
#         # instance.project = validated_data.get('project', instance.project)
#         # instance.status = validated_data.get('status', instance.status)
    
#         permission_data = validated_data.get('permission')
#         if permission_data:
#             permission_instance = instance.permission

#             for attr, value in permission_data.items():
#                 setattr(permission_instance, attr, value)

#             permission_instance.save()
    
#         instance.save()
#         return instance
