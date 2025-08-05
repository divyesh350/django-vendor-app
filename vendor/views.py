from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token
from .models import EmailOTP, Document
from .serializers import (
    SendOTPSerializer, VerifyOTPSerializer, SignupSerializer, 
    UserProfileSerializer, DocumentUploadSerializer, DocumentSerializer
)
import logging

# drf-yasg imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)


class SendOTPView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Send OTP to email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email address')
            }
        ),
        responses={
            200: openapi.Response("OTP sent successfully", SendOTPSerializer),
            400: "Bad Request"
        }
    )
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
    
    @swagger_auto_schema(
        operation_description="Verify OTP and return auth token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'otp'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email address'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='6-digit OTP code')
            }
        ),
        responses={
            200: openapi.Response("Login successful", VerifyOTPSerializer),
            400: "Bad Request"
        }
    )
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
    
    @swagger_auto_schema(
        operation_description="Create a new user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'name', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email address'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='User full name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password')
            }
        ),
        responses={
            201: openapi.Response("Signup successful", SignupSerializer),
            400: "Bad Request"
        }
    )
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


class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get profile details for the authenticated user",
        responses={
            200: openapi.Response("Profile details retrieved successfully", UserProfileSerializer),
            500: "Server error"
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Token <your-token>", type=openapi.TYPE_STRING, required=True
            )
        ]
    )
    def get(self, request):
        """Get profile details for the authenticated user"""
        try:
            serializer = UserProfileSerializer(request.user)
            return Response({
                'message': 'Profile details retrieved successfully',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving profile for user {request.user.id}: {str(e)}")
            return Response({
                'error': 'Failed to retrieve profile details. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload a document (Aadhar or PAN card)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['document_type', 'file'],
            properties={
                'document_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['aadhar', 'pan']),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='Document file (PDF, JPG, PNG, JPEG)'),
            },
        ),
        responses={
            201: openapi.Response('Document uploaded', DocumentSerializer),
            400: 'Validation error',
            500: 'Server error',
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Token <your-token>", type=openapi.TYPE_STRING, required=True
            )
        ]
    )
    def post(self, request):
        """Upload a document (Aadhar or PAN card)"""
        serializer = DocumentUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            document_type = serializer.validated_data['document_type']
            file = serializer.validated_data['file']
            
            try:
                # Check if document already exists for this user and type
                existing_doc = Document.objects.filter(
                    user=request.user, 
                    document_type=document_type
                ).first()
                
                if existing_doc:
                    # Update existing document
                    existing_doc.file = file
                    existing_doc.save()
                    document = existing_doc
                    message = f"{document.get_document_type_display()} updated successfully"
                else:
                    # Create new document
                    document = Document.objects.create(
                        user=request.user,
                        document_type=document_type,
                        file=file
                    )
                    message = f"{document.get_document_type_display()} uploaded successfully"
                
                # Serialize the response
                doc_serializer = DocumentSerializer(document, context={'request': request})
                
                return Response({
                    'message': message,
                    'document': doc_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error uploading document for user {request.user.id}: {str(e)}")
                return Response({
                    'error': 'Failed to upload document. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get all documents for the authenticated user",
        responses={
            200: openapi.Response("Documents retrieved successfully", DocumentSerializer(many=True)),
            500: "Server error"
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Token <your-token>", type=openapi.TYPE_STRING, required=True
            )
        ]
    )
    def get(self, request):
        """Get all documents for the authenticated user"""
        try:
            # Get documents for the user
            documents = Document.objects.filter(user=request.user)
            
            # Filter by document type if provided
            document_type = request.query_params.get('document_type')
            if document_type:
                documents = documents.filter(document_type=document_type)
            
            serializer = DocumentSerializer(documents, many=True, context={'request': request})
            
            return Response({
                'message': 'Documents retrieved successfully',
                'documents': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving documents for user {request.user.id}: {str(e)}")
            return Response({
                'error': 'Failed to retrieve documents. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id):
        """Get a specific document by ID"""
        try:
            document = Document.objects.get(id=document_id, user=request.user)
            serializer = DocumentSerializer(document, context={'request': request})
            
            return Response({
                'message': 'Document retrieved successfully',
                'document': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Document.DoesNotExist:
            return Response({
                'error': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving document {document_id} for user {request.user.id}: {str(e)}")
            return Response({
                'error': 'Failed to retrieve document. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
