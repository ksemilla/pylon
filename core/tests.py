from ninja.testing import TestClient
from typing import Any, Dict
from users.models import User

from auth.authentication import get_encoded_token


class MockAdminUser:
    id = 1
    role = User.Roles.ADMIN


class MockUser:
    id = 2
    role = User.Roles.USER


class AuthenticatedClient(TestClient):
    user: User

    def request(self, method, path, data={}, json=None, **request_params: Any):

        headers = {
            "Authorization": f"Bearer {get_encoded_token({"userId": self.user.id})}"
        }
        request_params["headers"] = headers
        return super().request(method, path, data, json, **request_params)

    def get(self, path, data: Dict | None = None, **request_params: Any):
        return super().get(path, data, user=self.user, **request_params)


class AuthenticatedAdminClient(AuthenticatedClient):
    user = MockAdminUser()


class AuthenticatedUserClient(AuthenticatedClient):
    user = MockUser()
