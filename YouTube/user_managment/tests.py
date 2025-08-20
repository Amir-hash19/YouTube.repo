from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from .views import CreateUserAccountView, LoginView
from .serializers import CreateUserAccountSerializer
from rest_framework.exceptions import ValidationError
from .models import UserAccount, UserAvatar
from rest_framework_simplejwt.tokens import RefreshToken


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


        self.assertTrue(UserAccount.objects.filter(pk=user.id).exists())


    def test_create_avatar_with_valid_data(self):

        user = UserAccount.objects.create_user(email="test1@email.com",
        password="strongpassword1", username="test@1")

        avatar = UserAvatar.objects.create(
            user = user,
            slug="test-slug1"
        )

        self.assertEqual(avatar.slug, "test-slug1")







class TestUserAccountView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserAccount.objects.create_user(
            username="ali@",
            email="ali@example.com",
            password="StrongPass123!"
        )


    def get_jwt_for_user(self, user=None):
        user = user or self.user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    

    def test_useraccount_detail_url_response_200(self):
        url = reverse("detail-user")
        token = self.get_jwt_for_user()
        response = self.client.get(url,
        HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 200)      