from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import string
import os


class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.email} - {self.otp}"
    
    def is_expired(self):
        """Check if OTP is expired (5 minutes)"""
        return self.created_at < timezone.now() - timedelta(minutes=5)
    
    @classmethod
    def generate_otp(cls):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def create_otp(cls, email):
        """Create a new OTP for the given email"""
        # Delete any existing OTPs for this email
        cls.objects.filter(email=email).delete()
        
        # Generate new OTP
        otp = cls.generate_otp()
        
        # Create new OTP record
        return cls.objects.create(email=email, otp=otp)


class Document(models.Model):
    """Model for storing user documents like Aadhar and PAN cards"""
    
    DOCUMENT_TYPES = [
        ('aadhar', 'Aadhar Card'),
        ('pan', 'PAN Card'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'document_type']
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"
    
    def filename(self):
        """Get the filename from the file path"""
        return os.path.basename(self.file.name)
    
    def file_size(self):
        """Get file size in bytes"""
        if self.file:
            return self.file.size
        return 0
    
    def file_size_mb(self):
        """Get file size in MB"""
        return round(self.file_size() / (1024 * 1024), 2)
