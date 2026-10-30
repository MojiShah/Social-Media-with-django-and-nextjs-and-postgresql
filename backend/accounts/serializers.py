from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    display_name = serializers.CharField(max_length=100,required=True,allow_blank=False,trim_whitespace=True)
    password = serializers.CharField(write_only=True,min_length=8,required=True,
        validators=[validate_password],style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True,required=True,style={"input_type": "password"})
    
    class Meta:
        model = User
        fields = ["id","username","email","display_name","password","password2",]
        read_only_fields = ["id"]
        
    def validate_username(self,value):
        # if not value.strip():
        #     raise serializers.ValidationError("Username cannot be empty.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("این نام کاربری قبلاً ثبت شده است.")

        return value
        
    def validate_email(self,value):
        # return value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("این ایمیل قبلاً ثبت شده است.")

        return value
        
    def validate(self,attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "رمز عبور و تکرار آن یکسان نیستند."})
        
        return attrs
        
    def create(self,validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # user = User.objects.create_user(
        # username=validated_data["username"],
        # email=validated_data["email"],
        # display_name=validated_data["display_name"],
        # password=validated_data["password"],
        # ) the create_user method has differnece with create methaod and that's hashing password automatically
        return user

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email","display_name","bio","avatar","created_at",]
        read_only_fields=["id","username","email","created_at",]
        
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","display_name","bio","avatar","created_at",]
        read_only_fields = fields
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        request = self.context.get("request")
        user = authenticate(
            request=request,
            username=username,
            password=password
        )
        
        if user is None:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
        
        attrs["user"] = user
        return attrs
        