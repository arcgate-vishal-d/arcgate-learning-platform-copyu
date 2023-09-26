from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from account.serializers import LoginSerializer, AdminViewSerializer

from account.models import User_data


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "message": "Login Successfully!",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class Login(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = get_tokens_for_user(user)
        return Response({"token": token}, status=status.HTTP_201_CREATED)


class AdminView(APIView):

    def get(self, request, *args, **kwargs):
        # users = User.objects.all()
        users = User_data.objects.all()
        serializer = AdminViewSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)