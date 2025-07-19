from rest_framework import serializers
from .models import Channel ,SocialLink
from user_managment.models import UserAccount


class CreateChannelSerializer(serializers):
    admins = serializers.SlugRelatedField(
        many=True,
        queryset=UserAccount.objects.all(),
        required=False
    )

    class Meta:
        model = Channel
        fields = ["title", "bio", "admins", "picture"]
        read_only_fields = ["date_created", "slug", "subscribers"]
        