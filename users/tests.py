from django.test import TestCase
from core.tests import AuthenticatedAdminClient, AuthenticatedUserClient
from ninja.testing import TestClient

from .views import user_router


class UserListCreateTest(TestCase):
    path: str = ""

    def test_get_users_list_fail(self):
        client = TestClient(user_router)
        response = client.get(self.path)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Unauthorized"})

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
