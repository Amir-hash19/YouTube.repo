from django.urls import path
from .views import CreateUserAccountView



urlpatterns = [
    path("User/SignUp/", CreateUserAccountView.as_view(), name="signup-user"),
]

