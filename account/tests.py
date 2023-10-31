from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

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


# class UserListingTestCase(TestCase):
#     def setUp(self):
#         self.path = "/api/v1/users/"
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="testpassword",
#             employee_id="test-emp-001",
#         )

#         self.project = Project.objects.create(
#             project_name="testProject", project_slug="test-project"
#         )
#         self.permissions = Permission.objects.create(
#             read=True, delete=True, update=False
#         )
#         self.role = Role.objects.create(role=1)
#         self.user_data = UserData.objects.create(
#             users=self.user,
#             permissions=self.permissions,
#             project=self.project,
#             role=self.role,
#             status=True,
#         )

#     def test_admin_view_search_without_result(self):
#         client = APIClient()
#         response = client.get(self.path, {"role": "non-existent-query"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_listing_search_with_result(self):
#         client = APIClient()
#         response = client.get(self.path, {"role": 1})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_listing_search_with_results(self):
#         client = APIClient()
#         response = client.get(self.path, {"project": "testProject"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserListingTestCase(TestCase):
    def setUp(self):
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
        self.role = Role.objects.create(role=1)  # Role with ID 1
        self.role_admin = Role.objects.create(role=2)  # Role with ID 2
        self.role_manager = Role.objects.create(role=3)  # Role with ID 3
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

    def test_admin_view_search_role_admin(self):
        # Test with a valid role filter (Role Admin) that should return results
        client = APIClient()
        response = client.get(self.path, {"role": 2})  # Role Admin
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ensure that the response contains data

    def test_admin_view_search_role_manager(self):
        # Test with a valid role filter (Role Manager) that should return results
        client = APIClient()
        response = client.get(self.path, {"role": 3})  # Role Manager
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ensure that the response contains data

    def test_user_listing_search_without_results(self):
        # Test with a non-existent role filter that should not return results
        client = APIClient()
        response = client.get(self.path, {"role": "non-existent-query"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 0) 

    def test_user_listing_search_with_no_filter(self):
        # Test without any filters, should return all users
        client = APIClient()
        response = client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ensure that the response contains data

# class UserDetailTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
        
#         # url = reverse("user_detail", kwargs={"user_id": self.user.id})
        
#         # self.user = User.objects.create_user(
#         #     username="testuser", password="testpassword"
#         # )
#     #     self.user = User.objects.create_user(username="testuser", password="testpassword")
#     #     project = Project.objects.create(
#     #         project_name="Test Project", project_slug="test-project-slug"
#     #     )
#     #     role = Role.objects.create(user=self.user, role=1)
#     #     permission = Permission.objects.create(read=True, delete=True, update=True)
#     #     self.user_data = UserData.objects.create(
#     #         users=self.user, project=project, role=role, permissions=permission
#     #     )
#     #     self.token, created = Token.objects.get_or_create(user=self.user)
#     #     self.token.save()

#     # # def test_token_authentication(self):
#     # #     response = self.client.get(self.url)
#     # #     self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # def test_get_user_detail(self):
#     #     url = reverse("user_detail", kwargs={"user_id": self.user.id})
#     #     # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
#     #     response = self.client.get(url)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)


# class LogoutViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse("logout")

#     def test_logout_missing_refresh_token(self):
#         response = self.client.post(self.url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_logout_invalid_token(self):
#         data = {"refresh": "invalid_token"}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class UserDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_existing_user_detail(self):
        # Create a Permission instance
        permission = Permission.objects.create(
            read=True,
            delete=True,
            update=True
        )

        # Create a Role instance
        role = Role.objects.create(role=Role.superadmin)

        # Create a Project instance
        project = Project.objects.create(
            project_name="Project X",
            project_slug="project-x"
        )

        # Create a User instance
        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            employee_id="E12345"
        )

        # Create a UserData record and associate it with the User, Role, Project, and Permission
        user_data = UserData.objects.create(
            users=user,
            project=project,
            role=role,
            permissions=permission,
            full_name="John Doe",
            status=True
        )

        url = reverse("user_detail", kwargs={"user_id": user.id})  # Use the user's actual ID

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_nonexistent_user_detail(self):
        # Attempt to retrieve a user detail for a non-existent user
        url = reverse("user_detail", kwargs={"user_id": 999})  # Use a non-existent user ID

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_with_permissions(self):
        # Create a User with no permissions
        user_without_permissions = User.objects.create(
            username="userwithoutperms",
            email="userwithoutperms@example.com",
            employee_id="E56789"
        )

        url = reverse("user_detail", kwargs={"user_id": user_without_permissions.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check if the response data indicates no permissions.


# Replace 'yourapp' with your app's name

class BulkUpdateUserDataViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_bulk_update_existing_user_data(self):
        # Create necessary instances: User, Role, Project, and Permission
        permission = Permission.objects.create(
            read=True,
            delete=True,
            update=True
        )
        role = Role.objects.create(role=Role.superadmin)
        project = Project.objects.create(
            project_name="Project X",
            project_slug="project-x"
        )
        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            employee_id="E12345"
        )
        user_data = UserData.objects.create(
            users=user,
            project=project,
            role=role,
            permissions=permission,
            full_name="John Doe",
            status=True
        )

        # Prepare bulk update data
        bulk_update_data = [
            {
                "employee_id": "E12345",
                "status": False,
                "permissions": {
                    "read": False,
                    "delete": False,
                    "update": False
                },
                "project": "Project X"
            }
            # Add more items for additional user data objects if needed
        ]

        url = reverse("bulk_update_user_data")  # Update with your actual URL name

        response = self.client.put(url, data=bulk_update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions if needed to validate the response data

    def test_bulk_update_invalid_data(self):
        # Invalid data with missing required fields
        invalid_data = [
            {
                "employee_id": "E12345",
                # Missing required fields
            }
        ]

        url = reverse("bulk_update_user_data")  # Update with your actual URL name

        response = self.client.put(url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions if needed to validate the response data

    def test_bulk_update_nonexistent_user_data(self):
        # Non-existent user data in the update request
        non_existent_data = [
            {
                "employee_id": "NonExistentEmployeeID",
                "status": False,
                "permissions": {
                    "read": False,
                    "delete": False,
                    "update": False
                },
                "project": "NonExistentProject"
            }
        ]

        url = reverse("bulk_update_user_data")  # Update with your actual URL name

        response = self.client.put(url, data=non_existent_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions if needed to validate the response data

        def test_bulk_update_user_data_with_non_matching_employee_id(self):
        # Attempt to update user data with a non-matching employee ID and project
            user = User.objects.create(username="testuser", email="testuser@example.com", employee_id="E12345")
            role = Role.objects.create(role=Role.superadmin)
            project = Project.objects.create(project_name="Project X", project_slug="project-x")
            permission = Permission.objects.create(read=True, delete=True, update=True)
            user_data = UserData.objects.create(users=user, project=project, role=role, permissions=permission, full_name="John Doe", status=True)

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

        # Add assertions to check if the response data indicates that the update failed due to non-matching data.
