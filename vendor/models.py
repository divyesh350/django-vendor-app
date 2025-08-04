from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import string


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
