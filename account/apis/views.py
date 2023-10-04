from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AdminViewSerializer
from drf_yasg.utils import swagger_auto_schema
from account.apis.serializers import LoginSerializer, AdminViewSerializer
from account.models import UserData
from account.apis import messages

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


class AdminView(APIView):

    def get(self, request, *args, **kwargs):
        users_info = UserData.objects.all()
        serializer = AdminViewSerializer(users_info, many=True).data
        try:
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
                    "result": {[]},
                }
            )
