from django.urls import path
from .views import CreateUserAccountView, LoginView



urlpatterns = [
    path("User/SignUp/", CreateUserAccountView.as_view(), name="signup-user"),
    path("User/Login/", LoginView.as_view(), name="Login-user")
]

