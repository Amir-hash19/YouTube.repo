from rest_framework import serializers
from .models import Channel ,SocialLink
from user_managment.models import UserAccount


class CreateChannelSerializer(serializers.ModelSerializer):
    admins = serializers.SlugRelatedField(
        many=True,
        slug_field = "username",
        queryset = UserAccount.objects.all(),
        required = False,
        allow_empty = True

    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Channel
        fields = ["title", "bio", "admins", "picture"]
        read_only_fields = ["date_created", "slug", "subscribers"]





class EditChannelSerializer(serializers.ModelSerializer):
    admins = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        queryset=UserAccount.objects.all(),
        required=False,
        allow_empty=True,
        
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            "title", "bio", "picture", "admins"
        ]
        read_only_field = ["slgu", "date_created", "owner"]


    def get_subscriber_count(self, obj):
        return obj.subscribers_count()

    def validate_admins(self, value):
        request = self.context.get("request")
        channel = self.instance


        if request and channel:
            if channel.owner != request.user:
                raise serializers.ValidationError("Only the owner can change the channel admins.")        
            







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'email']  

class ChannelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    admins = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['channel_id', 'title', 'subscribers', 'owner', 'admins', "bio", "picture"]




