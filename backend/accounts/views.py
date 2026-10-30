from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (RegisterSerializer,PublicUserSerializer,MyProfileSerializer,LoginSerializer)

# Create your views here.

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = PublicUserSerializer(user)
            return Response(response_serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data = request.data,context={"request":request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "user" : PublicUserSerializer(user).data,
                "access_token" : str(refresh.access_token),
                "refresh_token" : str(refresh)
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MyProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    
    def get(self,request):
        serializer = MyProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        serializer = MyProfileSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PublicUserProfileAPIView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,username):
        user = get_object_or_404(user,username__iexact=username,is_active=True)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class LogoutAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({"detail": "Refresh token is required."},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."},status=status.HTTP_200_OK)
        
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token."},status=status.HTTP_400_BAD_REQUEST)
        