from django.test import TestCase
from core.tests import AuthenticatedAdminClient, AuthenticatedUserClient
from ninja.testing import TestClient
import json

from .models import User
from .views import user_router


class UserListCreateTest(TestCase):
    path: str = ""

    def test_get_users_list_unauthorized(self):
        client = TestClient(user_router)
        response = client.get(self.path)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Unauthorized"})

    def test_get_users_list_permission_denied(self):
        client = AuthenticatedUserClient(user_router)
        response = client.get(self.path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data, {"detail": "Only admins have permission"}
        )

    def test_get_users_list_success(self):
        client = AuthenticatedAdminClient(user_router)
        response = client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "items")
        self.assertContains(response, "count")

    def test_create_user_unauthorized(self):
        client = TestClient(user_router)
        response = client.post(self.path, json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    def test_create_user_incorrect_data_input(self):
        client = AuthenticatedUserClient(user_router)
        response = client.post(self.path, json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    def test_create_user_permission_denied(self):
        client = AuthenticatedUserClient(user_router)
        response = client.post(
            self.path, json.dumps({"email": "test@test.com"})
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.data)

    def test_create_user_object_already_exists(self):
        User.objects.create(email="test@test.com")
        client = AuthenticatedAdminClient(user_router)
        response = client.post(
            self.path, json.dumps({"email": "test@test.com"})
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    def test_create_user_success(self):
        client = AuthenticatedAdminClient(user_router)
        response = client.post(
            self.path, json.dumps({"email": "test@test.com"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "id")
        self.assertContains(response, "email")
