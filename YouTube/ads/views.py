from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import mixins
from .models import Advertiser, AdVideo
from rest_framework.permissions import IsAdminUser
from .serializers import AdvertiserSerializer
from .permissions import IsAdvertismentUser


class ListAdvertiserView(GenericAPIView, mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    permission_classes = [IsAdminUser]
    serializer_class = AdvertiserSerializer
    
    def get(self, request, *args, **kwargs):
        """retriveing a list of advertizers"""
        return self.list(request, *args, **kwargs)
    


class AdDetailView(GenericAPIView, mixins.RetrieveModelMixin, 
                mixins.UpdateModelMixin):
    permission_classes = [IsAdvertismentUser]
    serializer_class = AdvertiserSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Advertiser.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


