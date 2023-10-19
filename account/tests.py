from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from account.models import Project, Role, UserData, Permission, User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLoginCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test123@")

    def test_invalid_username(self):
        data = {"username": "testuse", "password": "Test123@"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        data = {"username": "testuser", "password": "test123"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserListingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            employee_id="test-emp-001",
        )

        self.project = Project.objects.create(
            project_name="testProject", project_slug="test-project"
        )
        self.permissions = Permission.objects.create(
            read=True, delete=True, update=False
        )
        self.role = Role.objects.create(role="Super Admin")
        self.user_data = UserData.objects.create(
            users=self.user,
            permissions=self.permissions,
            project=self.project,
            role=self.role,
            status="Active",
        )

    def test_admin_view_search_without_result(self):
        client = APIClient()
        url = "/api/v1/users/"
        response = client.get(url, {"role": "non-existent-query"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_listing_search_with_result(self):
        client = APIClient()
        url = "/api/v1/users/"
        response = client.get(url, {"role": "Super Admin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_listing_search_with_results(self):
        client = APIClient()
        url = "/api/v1/users/"
        response = client.get(url, {"project": "testProject"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        project = Project.objects.create(
            project_name="Test Project", project_slug="test-project-slug"
        )
        role = Role.objects.create(user=self.user, role="Super Admin")
        permission = Permission.objects.create(read=True, delete=True, update=True)
        self.user_data = UserData.objects.create(
            users=self.user, project=project, role=role, permissions=permission
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.token.save()

    def test_token_authentication(self):
        url = reverse("user-detail", kwargs={"user_id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        url = reverse("user-detail", kwargs={"user_id": self.user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_logout_missing_refresh_token(self):
        url = reverse("logout")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Refresh token is required."})

    def test_logout_invalid_token(self):
        url = reverse("logout")
        data = {"refresh": "invalid_token"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Invalid Token."})
