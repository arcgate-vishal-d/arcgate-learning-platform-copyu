from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AdminViewSerializer
from account.serializers import LoginSerializer, AdminViewSerializer
from account.models import UserData
from drf_yasg.utils import swagger_auto_schema


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
        return Response({"token": token}, status=status.HTTP_201_CREATED)


class AdminView(APIView):
    def get(self, request, *args, **kwargs):
        users = UserData.objects.all()
        serializer = AdminViewSerializer(users, many=True).data

        try:
            return Response(
                {
                    "message": "sucess",
                    "error": False,
                    "code": 200,
                    "result": {
                        "UserData": serializer,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": "fail",
                    "error": True,
                    "code": 500,
                    "result": {
                        "totalItems": 0,
                        "items": [],
                        "totalPages": 0,
                        "currentPage": 0,
                    },
                }
            )
