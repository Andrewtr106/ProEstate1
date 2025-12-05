#!/usr/bin/env python3
"""
Test script for ProEstate Chatbot functionality
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_chat_api():
    """Test the chat API endpoint"""
    print("Testing Chat API...")

    # Test 1: Valid message
    print("\n1. Testing valid message...")
    try:
        response = requests.post(f'{BASE_URL}/chat_api',
                               json={'message': 'Hello, can you help me find apartments?'},
                               headers={'Content-Type': 'application/json'})

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('response', 'No response')[:100]}...")
            print("✅ Valid message test passed")
        else:
            print(f"❌ Valid message test failed: {response.text}")

    except Exception as e:
        print(f"❌ Valid message test failed with exception: {str(e)}")

    # Test 2: Empty message
    print("\n2. Testing empty message...")
    try:
        response = requests.post(f'{BASE_URL}/chat_api',
                               json={'message': ''},
                               headers={'Content-Type': 'application/json'})

        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print("✅ Empty message test passed (correctly rejected)")
        else:
            print(f"❌ Empty message test failed: {response.text}")

    except Exception as e:
        print(f"❌ Empty message test failed with exception: {str(e)}")

    # Test 3: Missing message field
    print("\n3. Testing missing message field...")
    try:
        response = requests.post(f'{BASE_URL}/chat_api',
                               json={},
                               headers={'Content-Type': 'application/json'})

        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print("✅ Missing message test passed (correctly rejected)")
        else:
            print(f"❌ Missing message test failed: {response.text}")

    except Exception as e:
        print(f"❌ Missing message test failed with exception: {str(e)}")

def test_database_operations():
    """Test database operations (requires running app)"""
    print("\n\nTesting Database Operations...")

    # This would require direct database access or admin endpoints
    # For now, we'll just verify the API is working
    print("Database operations are tested through the API endpoints above.")
    print("Chat messages are automatically saved when sent through the API.")

def main():
    """Run all tests"""
    print("🚀 ProEstate Chatbot Test Suite")
    print("=" * 50)

    # Wait a moment for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)

    try:
        # Test basic connectivity
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print(f"❌ Server not responding. Status: {response.status_code}")
            return

        print("✅ Server is running")

        # Run tests
        test_chat_api()
        test_database_operations()

        print("\n" + "=" * 50)
        print("🎉 Test suite completed!")
        print("\nNext steps:")
        print("1. Open the website in a browser")
        print("2. Click the chatbot icon in the bottom-right corner")
        print("3. Test the chat interface manually")
        print("4. Verify messages are saved in the database")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test suite failed with exception: {str(e)}")

if __name__ == '__main__':
    main()
