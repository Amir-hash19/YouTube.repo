from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount
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
    



