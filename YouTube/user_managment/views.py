from rest_framework.generics import CreateAPIView
from .models import UserAccount
from .serializers import CreateUserAccountSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .throttles import SignUpRateThrottle
from django.db import transaction




# class CreateUserAccountView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = CreateUserAccountSerializer
#     queryset = UserAccount.objects.all()
    
    
class CreateUserAccountView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [SignUpRateThrottle]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateUserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "detail":"User account created Successfully.",
                "access":str(refresh.access_token),
                "refresh":str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
