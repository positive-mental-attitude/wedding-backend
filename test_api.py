#!/usr/bin/env python3
"""
Test script for the Afterparty RSVP API
This script tests all endpoints to ensure they work correctly.
"""

import requests
import json
import time
import sys

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_rsvp_submission():
    """Test RSVP submission endpoint"""
    print("\nTesting RSVP submission...")
    
    # Test data
    test_data = {
        "name": "Jane Doe",
        "telegram": "@janedoe",
        "phone_number": "+6512345678"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/rsvp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_rsvp_retrieval():
    """Test RSVP retrieval endpoint"""
    print("\nTesting RSVP retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/rsvp")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_invalid_rsvp_submission():
    """Test RSVP submission with invalid data"""
    print("\nTesting invalid RSVP submission...")
    
    # Test with missing fields
    invalid_data = {
        "name": "John Doe"
        # Missing telegram and phone_number
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/rsvp",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_empty_rsvp_submission():
    """Test RSVP submission with empty data"""
    print("\nTesting empty RSVP submission...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/rsvp",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_multiple_rsvps():
    """Test submitting multiple RSVPs"""
    print("\nTesting multiple RSVP submissions...")
    
    test_rsvps = [
        {
            "name": "Alice Smith",
            "telegram": "@alicesmith",
            "phone_number": "+6598765432"
        },
        {
            "name": "Bob Johnson",
            "telegram": "@bobjohnson",
            "phone_number": "+6587654321"
        },
        {
            "name": "Carol Williams",
            "telegram": "@carolwilliams",
            "phone_number": "+6576543210"
        }
    ]
    
    success_count = 0
    for i, rsvp_data in enumerate(test_rsvps, 1):
        print(f"Submitting RSVP {i}...")
        try:
            response = requests.post(
                f"{BASE_URL}/api/rsvp",
                json=rsvp_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                success_count += 1
                print(f"✓ RSVP {i} submitted successfully")
            else:
                print(f"✗ RSVP {i} failed: {response.status_code}")
        except Exception as e:
            print(f"✗ RSVP {i} error: {e}")
    
    print(f"Successfully submitted {success_count}/{len(test_rsvps)} RSVPs")
    return success_count == len(test_rsvps)

def test_wedding_rsvp_yes_submission():
    """Test Wedding RSVP 'yes' submission endpoint"""
    print("\nTesting Wedding RSVP 'yes' submission...")
    
    # Test data for 'yes' response
    test_data = {
        "response_type": "yes",
        "full_name": "Jane Doe",
        "telegram_username": "@janedoe",
        "phone_number": "+6512345678",
        "dietary_restrictions": "Vegetarian, no nuts"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_wedding_rsvp_no_submission():
    """Test Wedding RSVP 'no' submission endpoint"""
    print("\nTesting Wedding RSVP 'no' submission...")
    
    # Test data for 'no' response
    test_data = {
        "response_type": "no",
        "full_name": "John Doe",
        "message": "Sorry, I can't make it"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_wedding_rsvp_maybe_submission():
    """Test Wedding RSVP 'maybe' submission endpoint"""
    print("\nTesting Wedding RSVP 'maybe' submission...")
    
    # Test data for 'maybe' response
    test_data = {
        "response_type": "maybe",
        "full_name": "Bob Smith",
        "note": "I'll confirm closer to the date"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_wedding_rsvp_retrieval():
    """Test Wedding RSVP retrieval endpoint"""
    print("\nTesting Wedding RSVP retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/wedding-rsvp")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_wedding_rsvp_without_dietary():
    """Test Wedding RSVP 'yes' submission without dietary restrictions"""
    print("\nTesting Wedding RSVP 'yes' without dietary restrictions...")
    
    # Test data for 'yes' response without dietary restrictions
    test_data = {
        "response_type": "yes",
        "full_name": "John Smith",
        "telegram_username": "@johnsmith",
        "phone_number": "+6598765432"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_invalid_wedding_rsvp():
    """Test Wedding RSVP submission with invalid data"""
    print("\nTesting invalid Wedding RSVP submission...")
    
    # Test with missing response_type
    invalid_data = {
        "full_name": "John Doe"
        # Missing response_type
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_invalid_wedding_rsvp_yes():
    """Test Wedding RSVP 'yes' submission with missing required fields"""
    print("\nTesting invalid Wedding RSVP 'yes' submission...")
    
    # Test 'yes' response with missing required fields
    invalid_data = {
        "response_type": "yes",
        "full_name": "John Doe"
        # Missing telegram_username and phone_number
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wedding-rsvp",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Afterparty RSVP API Test Suite")
    print("=" * 40)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("RSVP Submission", test_rsvp_submission),
        ("RSVP Retrieval", test_rsvp_retrieval),
        ("Invalid RSVP Submission", test_invalid_rsvp_submission),
        ("Empty RSVP Submission", test_empty_rsvp_submission),
        ("Multiple RSVPs", test_multiple_rsvps),
        ("Wedding RSVP Yes Submission", test_wedding_rsvp_yes_submission),
        ("Wedding RSVP No Submission", test_wedding_rsvp_no_submission),
        ("Wedding RSVP Maybe Submission", test_wedding_rsvp_maybe_submission),
        ("Wedding RSVP Retrieval", test_wedding_rsvp_retrieval),
        ("Wedding RSVP without Dietary", test_wedding_rsvp_without_dietary),
        ("Invalid Wedding RSVP", test_invalid_wedding_rsvp),
        ("Invalid Wedding RSVP Yes", test_invalid_wedding_rsvp_yes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the API implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 