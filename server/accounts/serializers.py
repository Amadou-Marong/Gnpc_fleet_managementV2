from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'password', 'role', 'department', 'is_active', 'is_staff']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
   
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['department'] = user.department
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data["user"] = {
            "id": self.user.id,
            "full_name": self.user.full_name,
            "email": self.user.email,
            "is_active": self.user.is_active,
            "role": self.user.role,
            "department": self.user.department,
        }
        
        return data