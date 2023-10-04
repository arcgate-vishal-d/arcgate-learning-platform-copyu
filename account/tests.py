from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from account.models import Project, UserPermission, Role, UserData


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test123@")

    def test_valid_login(self):
        data = {"username": "testuser", "password": "Test123@"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


class UserListingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.project = Project.objects.create(
            project_name="testProject", project_slug="test-project"
        )
        self.permission = UserPermission.objects.create(
            emp_id="test-emp-001", read=True, delete=True, update=False
        )
        self.role = Role.objects.create(
            role=Role.SUPERADMIN, permission=self.permission
        )
        self.user_data = UserData.objects.create(
            users=self.user,
            fullName= "Test",
            permission=self.permission,
            project=self.project,
            role=self.role,
            status=1,
        )

    def test_admin_view_search_without_result(self):
        client = APIClient()

        url = "/api/v1/user/data/"

        response = client.get(url, {"search": "non-existent-query"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_view_search_with_result(self):
        client = APIClient()

        url = "/api/v1/user/data/"

        response = client.get(url, {"search": "testProject", "fullName": "Tet"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_view_search_with_results(self):
        client = APIClient()

        url = "/api/v1/user/data/"

        response = client.get(url, {"project": "testProject"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_view_ordering_invalid_field(self):
        client = APIClient()

        url = "/api/v1/user/data/"

        response = client.get(url, {"ordering": "invalid_field"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_view_ordering(self):
        client = APIClient()
        url = "/api/v1/user/data/"
        response = client.get(url, {"ordering": "-id"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
