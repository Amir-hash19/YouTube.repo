from django.db import models
import re




def validate_username_with_special_characters(value):
    if re.match(r'^[a-zA-Z0-9]*$', value):
        raise ValidationError("Username must contain at least one special charactes")


def password_validator(value):
    if len(value) != 8 and not re.match(r'^[a-zA-Z0-9]*$', value):
        raise ValidationError("National ID must be exactly 10 digits.")




class UserAccount(models.Model):
    username = models.CharField(unique=True, max_length=100, validators=[validate_username_with_special_characters])
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(validators=[password_validator], max_length=8)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField()

    GENDER_TYPE = (
        ("female", "FEMALE"),
        ("male", "MALE")
    )

    gender = models.CharField(max_length=6, choices=GENDER_TYPE, null=True, blank=True)
    slug = models.SlugField(unique=True)






class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('website', 'Website'),
        
    ]

    user = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50,  choices=PLATFORM_CHOICES)
    url = models.URLFIELD()

    def __str__(self):
        return f"{self.user.username} - {self.platform}"






class UserAvatar(models.Model):
    user = models.ForeginKey(to=UserAccount,  on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.slug}"