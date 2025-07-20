from rest_framework.views import APIView
from .models import Channel, SocialLink
from rest_framework import status
from rest_framework.views import Response
from user_managment.throttles import SignUpRateThrottle, LoginRateThrottle, CreateChannelThrottle
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CreateChannelSerializer
from django.db import transaction



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

