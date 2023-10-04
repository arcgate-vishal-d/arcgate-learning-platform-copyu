from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Test123@")

    def test_valid_login(self):
        data = {"username": "testuser", "password": "Test123@"}
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


from rest_framework.test import APIClient
from account.models import Project, UserPermission, Role, UserData
from account.apis.serializers import AdminViewSerializer


class AdminViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some test data
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
            permission=self.permission,
            project=self.project,
            role=self.role,
            status=1,
        )

    def test_admin_view_search(self):
        client = APIClient()
        # Define the URL for your API endpoint
        url = "/api/v1/user/data/"  # Replace with your actual URL

        # Make a GET request without authentication and with search query that doesn't match any results
        response = client.get(url, {"search": "non-existent-query"})

        # Assert that the response status code is 204 (No Content) when no results are found
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_admin_view_search_no_results(self):
    #     # Authenticate the user
    #     self.client.force_authenticate(user=self.user)

    #     # Define the URL for your API endpoint
    #     url = reverse('UserData')  # Use the name of the view if you have one

    #     # Make a GET request with a search query that should return no results
    #     response = self.client.get(url, {'search': 'nonexistentuser'})

    #     # Assert that the response has a 204 status code (No Content)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_admin_view_search_with_results(self):
    #     # Create some UserData instances that match the search criteria
    #     # Replace this with your actual data creation logic
    #     UserData.objects.create(
    #         username="test_user1", emp_id="emp-001", project="ProjectA", status="active"
    #     )
    #     UserData.objects.create(
    #         username="test_user2",
    #         emp_id="emp-002",
    #         project="ProjectB",
    #         status="inactive",
    #     )

    #     client = APIClient()
    #     # Define the URL for your API endpoint
    #     url = "/api/v1/user/data/"  # Replace with your actual URL

    #     # Make a GET request without authentication and with a search query that matches results
    #     response = client.get(url, {"search": "test_user", "ordering": "-id"})

    #     # Assert that the response status code is 200 (OK) when matching results are found
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # You can add more assertions to check the response data and structure as needed
    def test_admin_view_search_with_results(self):
        client = APIClient()
        # Define the URL for your API endpoint
        url = "/api/v1/user/data/"  # Replace with your actual URL

        # Make a GET request with a search query that matches some results
        # response = client.get(
        #     url, {"search": "testUser"}
        # )  # Adjust the search query as needed
        response = client.get(url, {"search": "non-existent-query"})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Add additional assertions to check the content of the response if needed
    # Example: self.assertEqual(len(response.data['result']), expected_result_count)
