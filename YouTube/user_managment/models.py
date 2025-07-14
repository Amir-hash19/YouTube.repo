from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from .exceptions import (MissingEmailError, EmailAlreadyExistsError, InvalidGenderError,
MissingUsernameError, UsernameAlreadyExistsError, WeakPasswordError)
import re



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username=None, birthday=None, gender=None):
        if not email:
            raise MissingEmailError()

        if self.model.objects.filter(email=email).exists():
            raise EmailAlreadyExistsError()
        
        email = self.normalize_email(email)

        if len(password) != 8:
            raise WeakPasswordError()
        
        allowed_genders = ["male", "female"]
        if gender and gender not in allowed_genders:
            raise InvalidGenderError()
        

        user = self.model(
            email=email,
            username=username,
            birthday=birthday,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,password=None, **extra_fields):
        if not username:
            raise MissingUsernameError()
        
        if self.model.objects.filter(username=username).exists():
            raise UsernameAlreadyExistsError()
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        user = self.model(username=username, email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        




def validate_username_with_special_characters(value):
    if re.match(r'^[a-zA-Z0-9]*$', value):
        raise ValidationError("Username must contain at least one special charactes")





class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100, validators=[validate_username_with_special_characters])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    is_advertiser = models.BooleanField(default=False)
    is_channel_admin = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)

    GENDER_TYPE = (
        ("female", "FEMALE"),
        ("male", "MALE")
    )

    gender = models.CharField(max_length=6, choices=GENDER_TYPE, null=True, blank=True)
    slug = models.SlugField(unique=True)


    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    def get_username(self):
        return f"The Username is  {self.username}"

    def __str__(self):
        return f"{self.username}"





class UserAvatar(models.Model):
    user = models.ForeignKey(to=UserAccount,  on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.slug}"






