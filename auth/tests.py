from django.test import TestCase
from ninja.testing import TestClient
from unittest.mock import patch
from users.models import User
import json

from .views import auth_router


class GoogleLoginTest(TestCase):
    path: str = "google-login/"

    def test_login_google_fail_1(self):
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"token": "test"}),
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    def test_login_google_fail_2(self):
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"access_token": "test"}),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    @patch("auth.views.auth.verify_id_token")
    def test_login_google_fail_3(self, mock_verify_token):
        mock_verify_token.return_value = {
            "email": "test@test.com",
            "picture": "test-picture",
            "uid": "test-uid",
        }
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"access_token": "test"}),
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.data)

    @patch("auth.views.auth.verify_id_token")
    def test_login_google_success(self, mock_verify_token):
        mock_verify_token.return_value = {
            "email": "test@test.com",
            "picture": "test-picture",
            "uid": "test-uid",
        }
        User.objects.create(email="test@test.com")
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"access_token": "test"}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token")


class VerifyTokenTest(TestCase):
    path: str = "verify/"

    def test_verify_token_fail_1(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"key": "value"}))

        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    def test_verify_token_fail_2(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"token": "value"}))

        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    @patch("auth.views.verify_token")
    def test_verify_token_success(self, mock_verify_token):
        mock_verify_token.return_value = {"userId": 1}
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"token": "value"}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "userId")


class GoogleSignupTest(TestCase):
    path: str = "google-sign-up/"

    @patch("auth.views.auth.verify_id_token")
    def test_create_user_google_success(self, mock_verify_token):
        mock_verify_token.return_value = {
            "email": "test@test.com",
            "picture": "test-picture",
            "uid": "test-uid",
        }
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"access_token": "test"}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token")
