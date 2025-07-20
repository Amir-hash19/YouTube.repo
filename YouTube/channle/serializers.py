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
        