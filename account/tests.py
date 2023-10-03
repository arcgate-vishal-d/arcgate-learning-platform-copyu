from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APIClient
from account.models import Project, UserPermission, Role, UserData
from account.apis.serializers import AdminViewSerializer


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test123@")

    def test_valid_login(self):
        data = {"username": "testuser", "password": "Test123@"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_invalid_username(self):
        data = {"username": "testuse", "password": "Test123@"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        data = {"username": "testuser", "password": "test123"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_user_exists(self):
    #     user_exists = User.objects.filter(username=self.user.username).exists()
    #     self.assertTrue(user_exists)

    # def test_user_not_exist(self):
    #     user_exists = User.objects.filter(username='adminabc').exists()
    #     self.assertFalse(user_exists)


class UserListing(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test@123")

        self.project = Project.objects.create(
            project_name="TestProject", project_slug="testProject"
        )
        self.permission = UserPermission.objects.create(
            emp_id="test-emp-001", read=True, delete=True, update=False
        )
        self.role = Role.objects.create(
            role=Role.SUPERADMIN, permission=self.permission
        )
        self.user_data = UserData.objects.create(
            users=self.user,
            permission=self.permission,
            project=self.project,
            role=self.role,
            status=1,
        )

    def test_invalid_search(self):
        data = {
            "project_name": "TestProject",
            "project_slug": "testProject",
        }
        response = self.client.post(reverse("user/data/?project=TestProject"))
        self.assertEqual(response.status_code, status.HTTP_100_CONTINUE)
