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



class CreateChannelView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CreateChannelThrottle]

    def post(self, request):
        serializer = CreateChannelSerializer(data=request.data)
        if serializer.is_valid():
            try:
               validated_data = serializer.validated_data

               if 'owner' in validated_data and validated_data['owner'] != request.user:
                

                channel = serializer.save(owner = request.user)

                return Response(CreateChannelSerializer(channel).data, status=status.HTTP_201_CREATED)
            
               
            except PermissionDenied as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({"detail": "خطا در ایجاد کانال: " + str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
               
