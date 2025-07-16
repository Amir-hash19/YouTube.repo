from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount




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
       





