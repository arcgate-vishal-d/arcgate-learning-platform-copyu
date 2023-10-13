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




class BasicPagination(PageNumberPagination):
    page_size_query_param = "limit"

class UserListing(APIView, PaginationHandlerMixin):
    
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # auth_token = request.META.get('HTTP_AUTHORIZATION')
        # print(auth_token)
        search_query = self.request.query_params.get("search")

        ordering = self.request.query_params.get("ordering", "id")
        role_filter = self.request.query_params.get("role")
        project_filter = self.request.query_params.get("project")
        status_filter = self.request.query_params.get("status")
        empid_filter = self.request.query_params.get("employee_id")
        username_filter = self.request.query_params.get("username")
        fullName_filter = self.request.query_params.get("fullname")

        valid_ordering_fields = [
            "project__project_name",
            "users__employee_id",
            "status",
            "role__role",
            "fullname",
            "id",
        ]

        if ordering.lstrip("-") not in valid_ordering_fields:
            ordering = "id"

        users_info = UserData.objects.all()
        users_info = users_info.order_by(ordering)
        # paginator = LimitOffsetPagination()
        # users_info = paginator.paginate_queryset(UserData.objects.all(), request, self)
        

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

        if fullName_filter:
            users_info = users_info.filter(
                # users__first_name__icontains=fullName_filter.split()[0],
                # users__last_name__icontains=fullName_filter.split()[1]
                fullname__icontains=fullName_filter
            )
        

        if role_filter:
            users_info = users_info.filter(role__role=role_filter)

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
                return Response(
                    response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            response_data = responses.error_response()
            return Response(response_data, status=status.HTTP_200_OK)


class BulkUpdateUserDataView(generics.UpdateAPIView):
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        updated_data = request.data

        if isinstance(updated_data, list):
            try:
                for item in updated_data:
                    employee_id = item.get("employee_id")
                    new_status = item.get("status")
                    if new_status not in ["Active", "Inactive"]:
                        return Response(
                            {"message": "Invalid value for 'status' field"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    new_permissions_data = item.get("permissions")
                    # if not all(permissions in ["true", "false"] for permissions in new_permissions_data.values()):
                    #     return Response(
                    #         {"message": "Invalid value for permissions field"},
                    #         status=status.HTTP_400_BAD_REQUEST,
                    #     )
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

            except UserData.DoesNotExist:
                response_data = responses.user_data_not_found_response()
                return Response(response_data, status=status.HTTP_200_OK)

            return Response(
                {"message": f"Updated {len(updated_data)} user's data successfully"},
                status=status.HTTP_200_OK,
            )

        response_data = responses.invalid_data_formate_response()
        return Response(response_data, status=status.HTTP_200_OK)


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



# class LogoutView(APIView):
#     authentication_classes = [JWTAuthentication] 
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             # print(refresh_token)
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({"message":"logout succussfully"} ,status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"message":"Something is wrong"},status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)
