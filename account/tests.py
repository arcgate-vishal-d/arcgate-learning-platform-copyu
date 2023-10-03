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
