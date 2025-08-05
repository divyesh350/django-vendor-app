from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailOTP


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)
    
    def validate(self, data):
        """Validate OTP format and existence"""
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            raise serializers.ValidationError("Email and OTP are required")
        
        # Check if OTP exists and is valid
        try:
            otp_obj = EmailOTP.objects.get(email=email, otp=otp)
            if otp_obj.is_expired():
                raise serializers.ValidationError("OTP has expired")
            if otp_obj.is_verified:
                raise serializers.ValidationError("OTP has already been used")
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        
        return data


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8, write_only=True)
    
    def validate_email(self, value):
        """Check if email is already registered"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered")
        return value
    
    def validate_name(self, value):
        """Validate name is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip()
    
    def create(self, validated_data):
        """Create a new user"""
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields = ['id', 'username', 'date_joined', 'last_login'] 