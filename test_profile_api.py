#!/usr/bin/env python3
"""
Test script for the new Profile API
This script demonstrates how to use the profile API with authentication
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/vendor"

def test_profile_api():
    """Test the complete flow: send OTP, verify OTP, get profile"""
    
    print("🧪 Testing Profile API...")
    print("=" * 50)
    
    # Step 1: Send OTP
    print("1. Sending OTP...")
    email = "test@example.com"
    
    response = requests.post(f"{BASE_URL}/send-otp/", json={"email": email})
    
    if response.status_code == 200:
        print("✅ OTP sent successfully")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Failed to send OTP: {response.status_code}")
        print(f"   Error: {response.json()}")
        return
    
    # Step 2: Get OTP from console (in real scenario, user would check email)
    print("\n2. Please check the Django console for the OTP code")
    print("   (In development, emails are printed to console)")
    
    # For testing, we'll simulate getting an OTP
    # In real scenario, user would input the OTP from email
    otp = input("Enter the OTP from console: ").strip()
    
    if not otp:
        print("❌ No OTP provided, skipping verification")
        return
    
    # Step 3: Verify OTP
    print("\n3. Verifying OTP...")
    response = requests.post(f"{BASE_URL}/verify-otp/", json={
        "email": email,
        "otp": otp
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print("✅ OTP verified successfully")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Failed to verify OTP: {response.status_code}")
        print(f"   Error: {response.json()}")
        return
    
    # Step 4: Get Profile
    print("\n4. Getting profile details...")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Profile retrieved successfully")
        print("   Profile Details:")
        profile = data.get('profile', {})
        for key, value in profile.items():
            print(f"     {key}: {value}")
    else:
        print(f"❌ Failed to get profile: {response.status_code}")
        print(f"   Error: {response.json()}")
    
    print("\n" + "=" * 50)
    print("🎉 Profile API test completed!")

def test_profile_without_auth():
    """Test profile API without authentication (should fail)"""
    
    print("\n🧪 Testing Profile API without authentication...")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/profile/")
    
    if response.status_code == 401:
        print("✅ Correctly rejected unauthorized request")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"   Response: {response.json()}")

if __name__ == "__main__":
    print("🚀 Vendor Profile API Test Script")
    print("Make sure the Django server is running on http://localhost:8000")
    print()
    
    # Test profile without auth first
    test_profile_without_auth()
    
    # Test complete flow
    test_profile_api() 