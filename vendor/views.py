from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token
from .models import EmailOTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, SignupSerializer
import logging

logger = logging.getLogger(__name__)


class SendOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Send OTP to email"""
        serializer = SendOTPSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                # Create OTP
                otp_obj = EmailOTP.create_otp(email)
                
                # Render HTML email template
                html_message = render_to_string('vendor/email/otp_email.html', {
                    'otp_code': otp_obj.otp,
                    'email': email
                })
                
                # Create plain text version
                plain_message = f"""
                Your OTP Code: {otp_obj.otp}
                
                This OTP will expire in 5 minutes.
                Do not share this code with anyone.
                
                If you didn't request this OTP, please ignore this email.
                
                Best regards,
                Vendor App Team
                """
                
                # Send email with both HTML and plain text versions
                send_mail(
                    subject='🔐 Your OTP Code - Vendor App',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                logger.info(f"OTP sent successfully to {email}")
                
                return Response({
                    'message': 'OTP sent to your email.',
                    'email': email
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f"Failed to send OTP to {email}: {str(e)}")
                return Response({
                    'error': 'Failed to send OTP. Please check your email configuration.',
                    'details': str(e) if settings.DEBUG else None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Verify OTP and return auth token"""
        serializer = VerifyOTPSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                # Get OTP object
                otp_obj = EmailOTP.objects.get(email=email, otp=otp)
                
                # Check if OTP is expired
                if otp_obj.is_expired():
                    return Response({
                        'error': 'OTP has expired'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Check if OTP is already used
                if otp_obj.is_verified:
                    return Response({
                        'error': 'OTP has already been used'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Mark OTP as verified
                otp_obj.is_verified = True
                otp_obj.save()
                
                # Get or create user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': email,
                        'first_name': email.split('@')[0]  # Use email prefix as name
                    }
                )
                
                # Get or create token
                token, _ = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Login successful',
                    'token': token.key
                }, status=status.HTTP_200_OK)
                
            except EmailOTP.DoesNotExist:
                return Response({
                    'error': 'Invalid OTP'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': 'An error occurred. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Create a new user account"""
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Create user
                user = serializer.save()
                
                return Response({
                    'message': 'Signup successful'
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'error': 'Failed to create account. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
