import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_registration():
    print("\nTesting User Registration...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone_number": "+1234567890",
        "license_plate_number": "ABC123",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error in registration: {e}")
        return None

def test_login():
    print("\nTesting Login...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error in login: {e}")
        return None

def test_request_otp(token):
    print("\nTesting OTP Request...")
    url = f"{BASE_URL}/auth/request-otp"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error in OTP request: {e}")
        return None

def test_verify_otp(token, otp):
    print("\nTesting OTP Verification...")
    url = f"{BASE_URL}/auth/verify-otp"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test@example.com",
        "otp": otp
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error in OTP verification: {e}")
        return None

def main():
    print("Starting API Tests...")
    
    # Test registration
    registration_response = test_registration()
    if not registration_response:
        print("Registration failed. Stopping tests.")
        return
    
    # Test login
    login_response = test_login()
    if not login_response or "access_token" not in login_response:
        print("Login failed. Stopping tests.")
        return
    
    token = login_response["access_token"]
    
    # Test OTP request
    otp_response = test_request_otp(token)
    if not otp_response:
        print("OTP request failed. Stopping tests.")
        return
    
    # For OTP verification, you'll need to input the OTP manually
    # since it's sent to the email
    otp = input("\nPlease enter the OTP received in your email: ")
    test_verify_otp(token, otp)

if __name__ == "__main__":
    main()