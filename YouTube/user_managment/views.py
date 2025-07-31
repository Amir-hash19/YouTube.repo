from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import UserAccount, UserAvatar

from .serializers import( CreateUserAccountSerializer, LoginSerializer,
CreateUserAvatarSerializer, UserAvatarSerializer, EditUserAccountSerializer, DetailUserAccountSerializer, PasswordResetRequestSerializer)

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .throttles import SignUpRateThrottle, LoginRateThrottle
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


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




class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)




class CreateUserAvatar(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateUserAvatarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class EditAvatar(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        ویرایش کامل آواتار کاربر (جایگزینی تصویر)
        """
        try:
            avatar = request.user.image  # OneToOne relation
        except UserAvatar.DoesNotExist:
            return Response({"detail": "Avatar not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAvatarSerializer(avatar, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        ویرایش جزئی آواتار (مثلاً فقط تصویر)
        """
        try:
            avatar = request.user.avatar
        except UserAvatar.DoesNotExist:
            return Response({"detail": "Avatar not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAvatarSerializer(avatar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class EditUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, slug, request):
        user = get_object_or_404(UserAccount, slug=slug)
        if user != request.user:
            return None
        return user

    def patch(self, request):
        serializer = EditUserAccountSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = EditUserAccountSerializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class DeleteUserAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, slug, request):
        user = get_object_or_404(UserAccount, slug=slug)
        if user != request.user:
            raise PermissionDenied("You are not allowed to delete this account")
        return user


    def delete(self, request, slug):
        user = self.get_object(slug, request)
        user.delete()
        return Response({"message":"Your User Account deleted Successfully"})
    





class DeleteUserAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        avatar = get_object_or_404(UserAccount, user=request.user)

        if avatar.image:
            avatar.image.delete(save=False)


        avatar.delete()
        return Response({"message":"Your Avatar deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)        





class DetailAccountView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailUserAccountSerializer

    def get_object(self):
        return self.request.user
    



class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"link for resest password has been sent to your email"})