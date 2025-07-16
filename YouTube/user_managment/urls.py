from django.urls import path
from .views import CreateUserAccountView, LoginView, CreateUserAvatar



urlpatterns = [
    path("User/SignUp/", CreateUserAccountView.as_view(), name="signup-user"),
    path("User/Login/", LoginView.as_view(), name="Login-user"),
    path("User/create-avatar/", CreateUserAvatar.as_view(), name="user-createavatar"),

]

