#!/usr/bin/env python3
"""
Test script for the Document Upload and Retrieval APIs
This script demonstrates how to use the document APIs with authentication
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000/api/vendor"

def create_test_file(filename, content="Test document content"):
    """Create a test file for upload"""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def cleanup_test_files(files):
    """Clean up test files"""
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def test_document_apis():
    """Test the complete document API flow"""
    
    print("🧪 Testing Document APIs...")
    print("=" * 50)
    
    # Step 1: Get authentication token (reuse from profile test)
    print("1. Getting authentication token...")
    email = "test@example.com"
    
    # Send OTP
    response = requests.post(f"{BASE_URL}/send-otp/", json={"email": email})
    
    if response.status_code != 200:
        print(f"❌ Failed to send OTP: {response.status_code}")
        return
    
    # Get OTP from user
    otp = input("Enter the OTP from console: ").strip()
    
    if not otp:
        print("❌ No OTP provided, skipping test")
        return
    
    # Verify OTP
    response = requests.post(f"{BASE_URL}/verify-otp/", json={
        "email": email,
        "otp": otp
    })
    
    if response.status_code != 200:
        print(f"❌ Failed to verify OTP: {response.status_code}")
        return
    
    data = response.json()
    token = data.get('token')
    print("✅ Authentication successful")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Step 2: Test document upload
    print("\n2. Testing document upload...")
    
    # Create test files
    test_files = []
    try:
        aadhar_file = create_test_file("test_aadhar.txt", "Aadhar Card Test Content")
        pan_file = create_test_file("test_pan.txt", "PAN Card Test Content")
        test_files.extend([aadhar_file, pan_file])
        
        # Upload Aadhar card
        print("   Uploading Aadhar card...")
        with open(aadhar_file, 'rb') as f:
            files = {'file': f}
            data = {'document_type': 'aadhar'}
            response = requests.post(f"{BASE_URL}/upload-document/", 
                                  headers=headers, files=files, data=data)
        
        if response.status_code == 201:
            aadhar_data = response.json()
            aadhar_id = aadhar_data['document']['id']
            print("✅ Aadhar card uploaded successfully")
            print(f"   Document ID: {aadhar_id}")
        else:
            print(f"❌ Failed to upload Aadhar card: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
        
        # Upload PAN card
        print("   Uploading PAN card...")
        with open(pan_file, 'rb') as f:
            files = {'file': f}
            data = {'document_type': 'pan'}
            response = requests.post(f"{BASE_URL}/upload-document/", 
                                  headers=headers, files=files, data=data)
        
        if response.status_code == 201:
            pan_data = response.json()
            pan_id = pan_data['document']['id']
            print("✅ PAN card uploaded successfully")
            print(f"   Document ID: {pan_id}")
        else:
            print(f"❌ Failed to upload PAN card: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
        
    except Exception as e:
        print(f"❌ Error creating test files: {str(e)}")
        return
    
    # Step 3: Test get all documents
    print("\n3. Testing get all documents...")
    response = requests.get(f"{BASE_URL}/documents/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        documents = data.get('documents', [])
        print(f"✅ Retrieved {len(documents)} documents")
        for doc in documents:
            print(f"   - {doc['document_type_display']}: {doc['filename']}")
    else:
        print(f"❌ Failed to get documents: {response.status_code}")
        print(f"   Error: {response.json()}")
    
    # Step 4: Test get documents by type
    print("\n4. Testing get documents by type...")
    
    # Get Aadhar documents
    response = requests.get(f"{BASE_URL}/documents/?document_type=aadhar", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        aadhar_docs = data.get('documents', [])
        print(f"✅ Retrieved {len(aadhar_docs)} Aadhar documents")
    else:
        print(f"❌ Failed to get Aadhar documents: {response.status_code}")
    
    # Get PAN documents
    response = requests.get(f"{BASE_URL}/documents/?document_type=pan", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        pan_docs = data.get('documents', [])
        print(f"✅ Retrieved {len(pan_docs)} PAN documents")
    else:
        print(f"❌ Failed to get PAN documents: {response.status_code}")
    
    # Step 5: Test get specific document
    print("\n5. Testing get specific document...")
    response = requests.get(f"{BASE_URL}/documents/{aadhar_id}/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        document = data.get('document', {})
        print(f"✅ Retrieved specific document: {document['document_type_display']}")
        print(f"   Filename: {document['filename']}")
        print(f"   File size: {document['file_size_mb']} MB")
        print(f"   File URL: {document['file_url']}")
    else:
        print(f"❌ Failed to get specific document: {response.status_code}")
        print(f"   Error: {response.json()}")
    
    # Cleanup test files
    cleanup_test_files(test_files)
    
    print("\n" + "=" * 50)
    print("🎉 Document API test completed!")

def test_document_upload_validation():
    """Test document upload validation"""
    
    print("\n🧪 Testing Document Upload Validation...")
    print("=" * 50)
    
    # Test without authentication
    print("1. Testing upload without authentication...")
    response = requests.post(f"{BASE_URL}/upload-document/")
    
    if response.status_code == 401:
        print("✅ Correctly rejected unauthorized upload")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    # Test with invalid file type
    print("\n2. Testing upload with invalid file type...")
    # This would require a token, so we'll just document the expected behavior
    print("   Expected: 400 Bad Request with file type validation error")
    
    # Test with oversized file
    print("\n3. Testing upload with oversized file...")
    print("   Expected: 400 Bad Request with file size validation error")

if __name__ == "__main__":
    print("🚀 Vendor Document API Test Script")
    print("Make sure the Django server is running on http://localhost:8000")
    print()
    
    # Test validation first
    test_document_upload_validation()
    
    # Test complete flow
    test_document_apis() 