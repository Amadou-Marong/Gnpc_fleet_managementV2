from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from utils.permissions import IsAdminOrCreateReadOnly
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser
User = get_user_model()
# Create your views here.


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
        
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Invalidate the token by blacklisting it
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCreateReadOnly]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCreateReadOnly]

    def get_permissions(self):
        # If the request is DELETE (deleting a user), require admin rights
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        # For GET (retrieving) and PUT/PATCH (updating), allow anyone
        return [AllowAny()]
    
class UserFormOptionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        roles = [
            {'value': value, 'label': label} for value, label in CustomUser.ROLE_CHOICES
        ]
        departments = [
            {'value': value, 'label': label} for value, label in CustomUser.DEPARTMENT_CHOICES
        ]
        
        return Response({
            'roles': roles,
            'departments': departments
        })
        