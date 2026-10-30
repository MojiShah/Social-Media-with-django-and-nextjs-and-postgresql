from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True,min_length=8,style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True,style={"input_type": "password"})
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "password",
            "password_confirm",
        ]
        
        def validate_username(self,value):
            if not value.strip():
                raise serializers.ValidationError("Username cannot be empty.")
            
            return value
        
        def validate_email(self,value):
            return value.lower()
        
        def validate(self,attrs):
            if attrs["password"] != attrs["password_confirm"]:
                raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
            
            return attrs
        
        def create(self,validated_data):
            validated_data.pop("password_confirm")
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "bio",
            "avatar",
            "created_at",
        ]
        read_only_fields=[
            "id",
            "username",
            "email",
            "created_at",
        ]
        
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "display_name",
            "bio",
            "avatar",
            "created_at",
        ]
        
    