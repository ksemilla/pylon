from django.urls import path

from pylon.users.views import (
    UserCreateView,
)

app_name = "users"
urlpatterns = [
    path("signup/", view=UserCreateView.as_view()),
]
