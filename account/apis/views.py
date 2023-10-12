from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.apis.serializers import LoginSerializer, PermissionsSerializer
from drf_yasg.utils import swagger_auto_schema
from account.models import UserData, User, Permission
from account.apis import messages, responses
from account.apis.pagination import PaginationHandlerMixin
from django.db import transaction
from django.db.models import F
# from account.apis.permissions import IsAuthenticatedUser, IsAdminUser
from rest_framework.permissions import IsAuthenticated


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


class TokenRefreshView(APIView):   
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                access_token = str(refresh_token_obj.access_token)
                
                return Response({'access': access_token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

class UserListing(APIView, PaginationHandlerMixin):
    # permission_classes = [IsAuthenticatedUser]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]

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
                        "results": serializer,
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
                    "results": [],
                },
                status=status.HTTP_200_OK,
            )


class BulkUpdateUserDataView(generics.UpdateAPIView):
    serializer_class = PermissionsSerializer
    # permission_classes = [IsAdminUser]

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        updated_data = request.data

        if isinstance(updated_data, list):
            try:
                for item in updated_data:
                    user_id = item.get("user_id")
                    new_status = item.get("status")
                    new_permissions_data = item.get("permission")
                    project_name = item.get("project")
                    user_data_objects = UserData.objects.filter(
                        users__id=user_id, project__project_name=project_name
                    )

                    if user_data_objects.exists():
                        user_data = user_data_objects.first()

                        user_data.status = new_status
                        user_data.save()

                        permission = user_data.permission
                        permission.read = new_permissions_data.get(
                            "read", permission.read
                        )
                        permission.delete = new_permissions_data.get(
                            "delete", permission.delete
                        )
                        permission.update = new_permissions_data.get(
                            "update", permission.update
                        )
                        permission.save()

            except UserData.DoesNotExist:
                pass

            return Response(
                {"message": f"Updated {len(updated_data)} users successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Invalid input data format"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserDetail(APIView):
    # permission_classes = [IsAuthenticatedUser]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user_data =  UserData.objects.filter(users_id=user_id)

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



class LogoutView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"logout succussfully"} ,status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message":"Something is wrong"},status=status.HTTP_400_BAD_REQUEST)


