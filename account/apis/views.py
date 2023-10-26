from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from account.apis.serializers import (
    LoginSerializer,
    PermissionsSerializer,
)
from account.models import UserData
from account.apis import responses
from account.apis.pagination import PaginationHandlerMixin


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "message": "Login Successfully!",
        "username": user.username,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class Login(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = get_tokens_for_user(user)
        return Response({"token": token}, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                access_token = str(refresh_token_obj.access_token)

                return Response({"access": access_token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Invalid or expired refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            response_data = responses.refresh_token_required_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                response_data = responses.refresh_token_required_response()
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            response_data = responses.logout_response()
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = responses.invalid_token_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class BasicPagination(PageNumberPagination):
    page_size_query_param = "limit"


class UserListing(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_query = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering", "id")
        role_filter = self.request.query_params.get("role")
        project_filter = self.request.query_params.get("project")
        status_filter = self.request.query_params.get("status")
        empid_filter = self.request.query_params.get("employee_id")
        full_name_filter = self.request.query_params.get("full_name")

        valid_ordering_fields = [
            "project__project_name",
            "users__employee_id",
            "status",
            "role__role",
            "full_name",
            "id",
        ]

        if ordering.lstrip("-") not in valid_ordering_fields:
            ordering = "id"

        users_info = UserData.objects.all()

        if search_query:
            users_info = users_info.filter(
                project__project_name__icontains=search_query
            )

        if project_filter:
            users_info = users_info.filter(project__project_name=project_filter)

        if status_filter:
            users_info = users_info.filter(status=status_filter)

        if empid_filter:
            users_info = users_info.filter(users__employee_id=empid_filter)

        if full_name_filter:
            users_info = users_info.filter(full_name__icontains=full_name_filter)

        if role_filter:
            users_info = users_info.filter(role__role__icontains=role_filter)

        users_info = users_info.order_by(ordering)

        if users_info.exists():
            page = self.paginate_queryset(users_info)

            if page is not None:
                serializer = PermissionsSerializer(page, many=True).data
                return self.get_paginated_response(serializer)
            try:
                serializer = PermissionsSerializer(users_info, many=True).data

                response_data = responses.success_response()
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as exe:
                error_message = f"Error: {str(exe)}"
                response_data = {"error": error_message}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = responses.error_response()
            return Response(response_data, status=status.HTTP_200_OK)


class BulkUpdateUserDataView(generics.UpdateAPIView):
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        updated_data = request.data
        updated_users = []

        if isinstance(updated_data, list):
            try:
                for item in updated_data:
                    employee_id = item.get("employee_id")
                    new_status = item.get("status")

                    new_permissions_data = item.get("permissions")
                    project_name = item.get("project")
                    user_data_objects = UserData.objects.filter(
                        users__employee_id=employee_id,
                        project__project_name=project_name,
                    )

                    if user_data_objects.exists():
                        user_data = user_data_objects.first()

                        user_data.status = new_status
                        user_data.save()

                        permissions = user_data.permissions
                        permissions.read = new_permissions_data.get(
                            "read", permissions.read
                        )
                        permissions.delete = new_permissions_data.get(
                            "delete", permissions.delete
                        )
                        permissions.update = new_permissions_data.get(
                            "update", permissions.update
                        )
                        permissions.save()

                        updated_users.append(user_data)
                response_data = responses.bulk_update_success_response(
                    updated_users, len(updated_data)
                )
                return Response(response_data, status=status.HTTP_200_OK)

            except UserData.DoesNotExist:
                response_data = responses.failed_response()
                return Response(response_data, status=status.HTTP_200_OK)

        response_data = responses.failed_response()
        return Response(response_data, status=status.HTTP_200_OK)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user_data = UserData.objects.filter(users_id=user_id)

            if user_data.exists():
                serializer = PermissionsSerializer(user_data, many=True)

                if serializer.data:
                    common_data = {
                        "employee_id": serializer.data[0]["employee_id"],
                        "user_id": serializer.data[0]["user_id"],
                        "full_name": serializer.data[0]["full_name"],
                    }

                project_data = []
                for item in serializer.data:
                    project_data.append(
                        {
                            "project": item["project"],
                            "permissions": item["permissions"],
                        }
                    )

                response_data = responses.detail_success_response(
                    common_data, project_data
                )

                response_data = responses.success_response(serializer.data)
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data = responses.failed_response()
                return Response(response_data, status=status.HTTP_200_OK)
        except:
            response_data = responses.error_response()
            return Response(response_data, status=status.HTTP_200_OK)
