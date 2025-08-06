from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailOTP, Document, Wallet
import os


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


class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload"""
    document_type = serializers.ChoiceField(choices=Document.DOCUMENT_TYPES)
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("File size must be less than 10MB")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        file_extension = os.path.splitext(value.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return value
    
    def validate_document_type(self, value):
        """Validate document type"""
        if value not in [choice[0] for choice in Document.DOCUMENT_TYPES]:
            raise serializers.ValidationError("Invalid document type")
        return value


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for document retrieval"""
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    filename = serializers.CharField(read_only=True)
    file_size_mb = serializers.FloatField(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'document_type', 'document_type_display', 'filename', 
            'file_size_mb', 'file_url', 'uploaded_at', 'is_verified'
        ]
        read_only_fields = ['id', 'uploaded_at', 'is_verified']
    
    def get_file_url(self, obj):
        """Get the file URL for download"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet model"""

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['id', 'user']