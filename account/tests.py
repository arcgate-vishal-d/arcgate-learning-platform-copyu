from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


from account.models import Project, Role, UserData, Permission, User

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


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.path = "/api/v1/users/"
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
        self.role = Role.objects.create(role=1)
        self.role_admin = Role.objects.create(role=2)
        self.role_manager = Role.objects.create(role=3)
        self.user_data = UserData.objects.create(
            users=self.user,
            permissions=self.permissions,
            project=self.project,
            role=self.role,
            status=True,
        )
        self.user_data_admin = UserData.objects.create(
            users=self.user,
            permissions=self.permissions,
            project=self.project,
            role=self.role_admin,
            status=True,
        )
        self.user_data_manager = UserData.objects.create(
            users=self.user,
            permissions=self.permissions,
            project=self.project,
            role=self.role_manager,
            status=True,
        )


class UserListingTestCase(BaseTestCase):
    def test_admin_view_search_role_admin(self):
        client = APIClient()
        response = client.get(self.path, {"role": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_admin_view_search_role_manager(self):
        client = APIClient()
        response = client.get(self.path, {"role": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_listing_search_without_results(self):
        client = APIClient()
        response = client.get(self.path, {"role": "non-existent-query"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_listing_search_with_no_filter(self):
        client = APIClient()
        response = client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class UserDetailTestCase(BaseTestCase):
    def test_get_existing_user_detail(self):
        permission = Permission.objects.create(read=True, delete=True, update=True)

        role = Role.objects.create(role=Role.superadmin)

        project = Project.objects.create(
            project_name="Project X", project_slug="project-x"
        )

        user = User.objects.create(
            username="testuser", email="testuser@example.com", employee_id="E12345"
        )

        user_data = UserData.objects.create(
            users=user,
            project=project,
            role=role,
            permissions=permission,
            full_name="New User",
            status=True,
        )

        url = reverse("user_detail", kwargs={"user_id": user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_user_detail(self):
        url = reverse("user_detail", kwargs={"user_id": 999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_with_permissions(self):
        user_without_permissions = User.objects.create(
            username="userwithoutperms",
            email="userwithoutperms@example.com",
            employee_id="E56789",
        )

        url = reverse("user_detail", kwargs={"user_id": user_without_permissions.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BulkUpdateUserDataViewTestCase(BaseTestCase):
    def test_bulk_update_existing_user_data(self):
        bulk_update_data = [
            {
                "employee_id": "test-emp-001",
                "status": False,
                "permissions": {"read": False, "delete": False, "update": False},
                "project": "testProject",
            }
        ]

        url = reverse("bulk_update_user_data")
        response = self.client.put(url, data=bulk_update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bulk_update_invalid_data(self):
        invalid_data = [
            {
                "employee_id": "test-emp-001",
            }
        ]

        url = reverse("bulk_update_user_data")
        response = self.client.put(url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bulk_update_nonexistent_user_data(self):
        non_existent_data = [
            {
                "employee_id": "NonExistentEmployeeID",
                "status": False,
                "permissions": {"read": False, "delete": False, "update": False},
                "project": "NonExistentProject",
            }
        ]

        url = reverse("bulk_update_user_data")
        response = self.client.put(url, data=non_existent_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bulk_update_user_data_with_non_matching_employee_id(self):
        user = User.objects.create(
            username="testuser_non_matching",
            email="testuser_non_matching@example.com",
            employee_id="test-emp-004",
        )
        role = Role.objects.create(role=Role.superadmin)
        project = Project.objects.create(
            project_name="testProject_non_matching",
            project_slug="test-project-non-matching",
        )
        permission = Permission.objects.create(read=True, delete=True, update=True)
        user_data = UserData.objects.create(
            users=user,
            project=project,
            role=role,
            permissions=permission,
            full_name="Test User",
            status=True,
        )

        update_data = [
            {
                "employee_id": "NonMatchingUser",
                "status": False,
                "permissions": {"read": False, "delete": False, "update": True},
                "project": "NonMatchingProject",
            }
        ]

        url = reverse("bulk_update_user_data")
        response = self.client.put(url, data=update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
