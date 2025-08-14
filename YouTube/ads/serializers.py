from rest_framework import serializers
from .models import Advertiser, AdVideo
from user_managment.models import UserAccount



class AdvertiserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=UserAccount.objects.all(),
                       slug_field="username"                 )
    class Meta:
        model = Advertiser
        fields = ["user", "business_name", "contact_email",
                "approved", "date_created"]
