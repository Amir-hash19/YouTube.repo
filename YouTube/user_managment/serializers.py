from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount, UserAvatar
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserAccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    class Meta:
       model = UserAccount
       fields = ["username", "email", "birthday",
        "gender", "password", "password2"]
       


    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password":"passwords do not match"})
        return attrs


    def create(self, validated_data):
        validated_data.pop("password2")
        user = UserAccount.objects.create_user(**validated_data)
        return user    
       




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "username":user.username
            }  
        raise serializers.ValidationError("username is incorrect or password not match!")
    




class CreateUserAvatarSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = UserAvatar
        fields = ["username", "image", "uploaded_at"]
        read_only_fields = ['username', 'uploaded_at']






class UserAvatarSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserAvatar
        fields = ['username', 'image', 'uploaded_at']
        read_only_fields = ['username', 'uploaded_at']

    def update(self, instance, validated_data):
        # حذف آواتار قبلی از فضای ذخیره‌سازی در صورت نیاز
        old_image = instance.image
        new_image = validated_data.get("image", None)

        if new_image and old_image and old_image.name != new_image.name:
            old_image.delete(save=False)

        return super().update(instance, validated_data)
    




class EditUserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAvatar
        fields = ['username', 'email', 'birthday', 'gender']
        read_only_fields = ['date_added']



    def validate_email(self, value):
        """
        بررسی یکتا بودن ایمیل (در صورتی که کاربر ایمیل جدید وارد کرده باشد).
        """
        user = self.instance
        if UserAccount.objects.exclude(slug=user.slug).filter(email=value).exists():
            raise serializers.ValidationError("email already existed!")
        return value

    def update(self, instance, validated_data):
        """
        ویرایش فیلدهای مجاز و ذخیره آن‌ها در مدل User.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance    

