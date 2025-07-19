from django.urls import path
from .views import( CreateUserAccountView, LoginView, CreateUserAvatar,
EditAvatar, EditUserAccountView, DeleteUserAccountView, DeleteUserAvatarView)



urlpatterns = [
    path("User/SignUp/", CreateUserAccountView.as_view(), name="signup-user"),
    path("User/Login/", LoginView.as_view(), name="Login-user"),
    path("User/create-avatar/", CreateUserAvatar.as_view(), name="user-createavatar"),
    path("User/edit-picture/", EditAvatar.as_view(), name="edit-avatar"),
    path("User/Edit/slug:slug/",EditUserAccountView.as_view(), name="edit-useraccount"),
    path("User/slug:slug/delete/", DeleteUserAccountView.as_view(), name="delete-useraccount"),
    path("User/slug:slug/avatar/",DeleteUserAvatarView.as_view(), name="delete-user-avatar")

]

