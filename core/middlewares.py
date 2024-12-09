import threading

_user = threading.local()


class CurrentUserMiddleware:
    """Middleware to save the current user to thread-local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        _user.value = None  # Clean up after the response
        return response


def get_current_user():
    """Helper to retrieve the current user."""
    return getattr(_user, "value", None)
