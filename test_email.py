#!/usr/bin/env python
"""
Test script to verify email configuration
Run this script to test if your Gmail SMTP settings are working correctly
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test the email configuration"""
    print("🔧 Testing Email Configuration...")
    print("=" * 50)
    
    # Check if email settings are loaded
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 50)
    
    # Test email sending
    test_email = input("Enter your email address to send a test email: ").strip()
    
    if not test_email:
        print("❌ No email address provided. Exiting...")
        return
    
    try:
        # Send test email
        send_mail(
            subject='🧪 Test Email - Vendor App',
            message=f"""
            This is a test email from your Vendor App.
            
            If you received this email, your Gmail SMTP configuration is working correctly!
            
            Test Details:
            - From: {settings.DEFAULT_FROM_EMAIL}
            - To: {test_email}
            - Backend: {settings.EMAIL_BACKEND}
            
            You can now use the OTP functionality in your app.
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print("📧 Check your inbox for the test email.")
        print("🎉 Your email configuration is working correctly!")
        
    except Exception as e:
        print("❌ Failed to send test email!")
        print(f"Error: {str(e)}")
        print("\n🔧 Troubleshooting Tips:")
        print("1. Make sure your .env file has the correct Gmail settings")
        print("2. Verify your Gmail App Password is correct")
        print("3. Check if 2FA is enabled on your Gmail account")
        print("4. Ensure your Gmail account allows 'less secure app access' or use App Password")

def show_env_template():
    """Show the required .env template"""
    print("\n📄 Required .env file template:")
    print("=" * 50)
    print("""
# Gmail SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
    """)
    print("=" * 50)
    print("📝 Instructions:")
    print("1. Create a .env file in your project root")
    print("2. Copy the template above and fill in your Gmail credentials")
    print("3. For Gmail App Password:")
    print("   - Go to Google Account settings")
    print("   - Security > 2-Step Verification > App passwords")
    print("   - Generate a new app password for 'Mail'")
    print("4. Run this script again to test")

if __name__ == "__main__":
    print("🚀 Vendor App Email Configuration Test")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = BASE_DIR / '.env'
    if not env_file.exists():
        print("❌ .env file not found!")
        show_env_template()
    else:
        print("✅ .env file found")
        test_email_configuration() 