from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .serializers import AdminViewSerializer
from drf_yasg.utils import swagger_auto_schema
from account.apis.serializers import LoginSerializer, AdminViewSerializer
from account.models import UserData
from account.apis import messages
from account.apis.pagination import PaginationHandlerMixin
from django.db.models import Q


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "message": "Login Successfully!",
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


class AdminView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, *args, **kwargs):
        search_query = self.request.query_params.get("search")

        ordering = self.request.query_params.get("ordering", "id")

        project_filter = self.request.query_params.get("project")
        status_filter = self.request.query_params.get("status")
        empid_filter = self.request.query_params.get("permission")
        username_filter = self.request.query_params.get("username")

        valid_ordering_fields = [
            "project__project_name",
            "permission__emp_id",
            "status",
            "users__username",
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
            users_info = users_info.filter(
                project__project_name=project_filter
            ).order_by("-project_filter")

        if status_filter:
            users_info = users_info.filter(status=status_filter)

        if empid_filter:
            users_info = users_info.filter(permission__emp_id=empid_filter)

        if username_filter:
            users_info = users_info.filter(users__username=username_filter)

        page = self.paginate_queryset(users_info)

        if page is not None:
            serializer = AdminViewSerializer(page, many=True).data
            return self.get_paginated_response(serializer)

        try:
            serializer = AdminViewSerializer(users_info, many=True).data
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
            return Response(
                {
                    "message": messages.get_failed_message(),
                    "error": True,
                    "code": 500,
                    "result": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
