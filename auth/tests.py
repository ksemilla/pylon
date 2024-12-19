from django.test import TestCase
from ninja.testing import TestClient
from unittest.mock import patch
from users.models import User
import json

from .views import auth_router


class GoogleLoginTest(TestCase):
    path: str = "google-login/"

    def test_login_google_incorrect_data_input(self):
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"token": "test"}),
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    def test_login_google_invalid_token(self):
        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"access_token": "test"}),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    @patch("auth.views.auth.verify_id_token")
    def test_login_google_not_existing_user(self, mock_verify_token):
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

    def test_verify_token_incorrect_data_input(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"key": "value"}))

        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    def test_verify_token_invalid_token(self):
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


class SignupTest(TestCase):
    path: str = "sign-up/"

    class MockCreatedUser:
        email = "test@test.com"
        photo_url = "test-photo-url"
        uid = "test-uid"

    def test_sign_up_incorrect_data_input(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"key": "value"}))

        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.data)

    @patch("auth.views.auth.create_user")
    def test_sign_up_missing_required_field(self, mock_create_user):
        mock_create_user.return_value = {"userId": 1}
        client = TestClient(auth_router)
        response = client.post(
            self.path, json.dumps({"email": "test@test.com"})
        )

        self.assertEqual(response.status_code, 422)

    @patch("auth.views.auth.create_user")
    def test_sign_up_success(self, mock_create_user):
        mock_create_user.return_value = self.MockCreatedUser()

        client = TestClient(auth_router)
        response = client.post(
            self.path,
            json.dumps({"email": "test@test.com", "password": "testtest"}),
        )
        users = User.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users.count(), 1)
        self.assertContains(response, "token")


class GoogleSignupTest(TestCase):
    path: str = "google-sign-up/"

    def test_create_user_google_incorrect_data_input(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"key": "value"}))
        self.assertEqual(response.status_code, 422)

    def test_create_user_google_invalid_token(self):
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"access_token": "value"}))
        self.assertEqual(response.status_code, 400)

    @patch("auth.views.auth.verify_id_token")
    def test_create_user_google_user_exists(self, mock_verify_token):
        User.objects.create(email="test@test.com")
        mock_verify_token.return_value = {
            "email": "test@test.com",
            "picture": "test-picture",
            "uid": "test-uid",
        }
        client = TestClient(auth_router)
        response = client.post(self.path, json.dumps({"access_token": "value"}))
        self.assertEqual(response.status_code, 400)

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
