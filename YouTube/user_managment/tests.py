from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import CreateUserAccountView, LoginView
from .serializers import CreateUserAccountSerializer
from rest_framework.exceptions import ValidationError
from .models import UserAccount, UserAvatar


class TestUrl(SimpleTestCase):

    def test_account_signup_resolve(self):
        """tets url of createuseraccountview for user_managment app"""
        url = reverse("signup-user")
        self.assertEqual(resolve(url).func.view_class, CreateUserAccountView)

        """test url of loginview for user_managment app"""
    def test_account_login_resolve(self):
        url = reverse("Login-user")
        self.assertEqual(resolve(url).func.view_class, LoginView)




class TestCreateUserAccountSerializer(TestCase):
    
    def test_valid_data_creates_user(self):
        
        data = {
            "username":"ali@",
            "email":"ali@example.com",
            "birthday": "2000-01-01",
            "gender": "male",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        serializer = CreateUserAccountSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "ali@")
        self.assertTrue(user.check_password("StrongPass123!"))


    def test_password_mismatch(self):

        data = {
            "username": "reza@",
            "email": "reza@example.com",
            "birthday": "1999-01-01",
            "gender": "male",
            "password": "StrongPass123!",
            "password2": "WrongPass123!",
        }

        serializer = CreateUserAccountSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)



    def test_password_validation(self):
        data = {
            "username": "sara",
            "email": "sara@example.com",
            "birthday": "1995-05-05",
            "gender": "female",
            "password": "123",   # خیلی ضعیف
            "password2": "123",
        }    

        serializer = CreateUserAccountSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)        



class TestUserAccountModel(TestCase):

    def test_create_user_with_valid_data(self):

        user = UserAccount.objects.create_user(email="test1@email.com",
        password="strongpassword1", username="test@1")


        self.assertEqual(user.email, "test1@email.com")


    def test_create_avatar_with_valid_data(self):

        user = UserAccount.objects.create_user(email="test1@email.com",
        password="strongpassword1", username="test@1")

        avatar = UserAvatar.objects.create(
            user = user,
            slug="test-slug1"
        )

        self.assertEqual(avatar.slug, "test-slug1")