from rest_framework.views import APIView
from .models import Channel, SocialLink
from rest_framework import status
from rest_framework.views import Response
from user_managment.throttles import CreateChannelThrottle
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import BasePermission
from .serializers import CreateChannelSerializer, EditChannelSerializer, ChannelSerializer, UserSerializer
from django.db import transaction
from search.views import ChannelFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from search.views import SubChannelFilter


class CreateChannelView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CreateChannelThrottle]

    @transaction.atomic
    def post(self, request):
        serializer = CreateChannelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                channel = serializer.save(owner=request.user)
                return Response(CreateChannelSerializer(channel).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"detail": "Something went wrong: " + str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class SubscribeChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        channel = get_object_or_404(Channel, slug=slug)
        user = request.user

        if user in channel.subscribers.all():
            return Response({"detail":"You are already subscribed"}, status=status.HTTP_400_BAD_REQUEST)
        
        channel.subscribers.add(user)
        return Response({"detail":"Subscribed successfully"}, status=status.HTTP_200_OK)
    



class UnsubscribeChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        channel = get_object_or_404(Channel, slug=slug)
        user = request.user

        if user not in channel.subscribers.all():
            return Response({"detail":"You are not subscribed"}, status=status.HTTP_400_BAD_REQUEST)
        
        channel.subscribers.remove(user)
        return Response({"detail":"Unsubscribed successfully"}, status=status.HTTP_200_OK)
    




class EditChannelView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, slug):
        channel = get_object_or_404(Channel, slug=slug)
        user = self.request.user
        if channel.owner != user and user not in channel.admins.all():
            raise PermissionDenied("You do not have permission to edit this channel.")
        return channel
    

    def patch(self, request, slug):
        channel = self.get_object(slug)
        serializer = EditChannelSerializer(channel, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, slug):
        channel = self.get_object(slug)
        serializer = EditChannelSerializer(channel, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class DeleteChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, channel_id):
        channel = get_object_or_404(Channel, channel_id=channel_id)

        if channel.owner != self.request.user:
            raise PermissionDenied("Only the channel owner can delete it.")
        return channel
    

    def delete(self, request, channel_id):
        channel = self.get_object(channel_id)
        channel.delete()
        return Response({"message":"channel delete successfully"}, status=status.HTTP_204_NO_CONTENT)
    





class IsOwnerOrChannelAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_owner = obj.owner == user
        is_admin = obj.admins.filter(slug=user.slug).exist()
        return is_admin or  is_owner




        
class DetailChannelView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrChannelAdmin]

    def get(self, request, channel_id):
        channel = get_object_or_404(Channel, channel_id=channel_id)
        self.check_object_permissions(request, channel)


        serializer = ChannelSerializer(channel)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ChannelFilter
    ordering_fileds = ['date_created', 'title']
    search_fields = ['title', 'bio']





class ChannelSubsVeiwSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ChannelFilter
    ordering_fields = ['date_created', 'title']
    search_fields = ['title', 'bio', 'slug']    