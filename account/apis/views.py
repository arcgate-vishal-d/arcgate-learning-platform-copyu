from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from account.apis.serializers import LoginSerializer, PermissionsSerializer
from drf_yasg.utils import swagger_auto_schema
from account.models import UserData, User, Permission
from account.apis import messages, responses
from account.apis.pagination import PaginationHandlerMixin
from django.db import transaction
from django.db.models import F


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


class BasicPagination(PageNumberPagination):
    page_size_query_param = "limit"


class UserListing(APIView, PaginationHandlerMixin):
    def get(self, request, *args, **kwargs):
        users_data = User.objects.get(pk=1)
        print(users_data.last_name)
        search_query = self.request.query_params.get("search")

        ordering = self.request.query_params.get("ordering", "id")

        project_filter = self.request.query_params.get("project")
        status_filter = self.request.query_params.get("status")
        empid_filter = self.request.query_params.get("permission")
        username_filter = self.request.query_params.get("username")
        fullName_filter = self.request.query_params.get("fullName")

        valid_ordering_fields = [
            "project__project_name",
            "permission__emp_id",
            "status",
            "users__username",
            "fullName",
            "id",
        ]
        if ordering.lstrip("-") not in valid_ordering_fields:
            ordering = "id"

        users_info = UserData.objects.all()

        users_info = users_info.order_by(ordering)

        if search_query:
            users_info = users_info.filter(
                project__project_name__icontains=search_query
            )

        if project_filter:
            users_info = users_info.filter(project__project_name=project_filter)

        if status_filter:
            users_info = users_info.filter(status=status_filter)

        if empid_filter:
            users_info = users_info.filter(permission__emp_id=empid_filter)

        if username_filter:
            users_info = users_info.filter(users__username=username_filter)

        if fullName_filter:
            users_info = users_info.filter(fullName__icontains=fullName_filter)

        if users_info.exists():
            page = self.paginate_queryset(users_info)

            if page is not None:
                serializer = PermissionsSerializer(page, many=True).data
                return self.get_paginated_response(serializer)
            try:
                serializer = PermissionsSerializer(users_info, many=True).data

                return Response(
                    {
                        "message": messages.get_success_message(),
                        "error": False,
                        "code": 200,
                        "result": serializer,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response({"msg": "Invalid"})
        else:
            return Response(
                {
                    "message": messages.get_not_found_message(),
                    "error": True,
                    "code": 200,
                    "result": [],
                },
                status=status.HTTP_200_OK,
            )

    # class BulkUpdateUserDataView(generics.UpdateAPIView):
    serializer_class = PermissionsSerializer

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        updated_data = request.data

        if isinstance(updated_data, list):
            user_ids = [item.get("user_id") for item in updated_data]
            new_status = updated_data[0].get(
                "status"
            )  # Assuming all users have the same status
            new_permissions_data = updated_data[0].get("permission")

            try:
                UserData.objects.filter(users__id__in=user_ids).update(
                    status=new_status
                )

                Permission.objects.filter(userdata__users__id__in=user_ids).update(
                    read=new_permissions_data.get("read", F("read")),
                    delete=new_permissions_data.get("delete", F("delete")),
                    update=new_permissions_data.get("update", F("update")),
                )

                return Response(
                    {"message": f"Updated {len(user_ids)} users successfully"},
                    status=status.HTTP_200_OK,
                )

            except UserData.DoesNotExist:
                # Handle the case where some users do not exist
                pass

        return Response(
            {"message": "Invalid input data format"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserDetail(APIView):
    def get(self, request, user_id):
        try:
            user_data = UserData.objects.filter(users_id=user_id)

            if user_data.exists():
                serializer = PermissionsSerializer(user_data, many=True)

                response_data = responses.success_response(serializer.data)
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data = responses.failed_response()
                return Response(response_data, status=status.HTTP_200_OK)
        except:
            response_data = responses.error_response()
            return Response(response_data, status=status.HTTP_200_OK)
