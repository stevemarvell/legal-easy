#!/usr/bin/env python3
"""
Test FastAPI server startup and basic functionality
"""

import sys
import traceback
from fastapi.testclient import TestClient

def test_app_import():
    """Test if we can import the FastAPI app"""
    print("🔍 Testing app import...")
    
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        return app
    except Exception as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        traceback.print_exc()
        return None

def test_app_startup(app):
    """Test if the app can start up"""
    print("\n🔍 Testing app startup...")
    
    try:
        client = TestClient(app)
        print("✅ TestClient created successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to create TestClient: {e}")
        traceback.print_exc()
        return None

def test_root_endpoint(client):
    """Test the root endpoint"""
    print("\n🔍 Testing root endpoint...")
    
    try:
        response = client.get("/")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        traceback.print_exc()
        return False

def test_cases_endpoints(client):
    """Test the cases endpoints"""
    print("\n🔍 Testing cases endpoints...")
    
    # Test cases list
    try:
        response = client.get("/api/cases")
        print(f"   GET /api/cases - Status: {response.status_code}")
        
        if response.status_code == 200:
            cases = response.json()
            print(f"✅ Cases list working - {len(cases)} cases")
            
            if cases:
                # Test individual case
                first_case_id = cases[0]['id']
                response = client.get(f"/api/cases/{first_case_id}")
                print(f"   GET /api/cases/{first_case_id} - Status: {response.status_code}")
                
                if response.status_code == 200:
                    case = response.json()
                    print(f"✅ Individual case working - {case.get('title', 'Unknown')}")
                    return True
                else:
                    print(f"❌ Individual case failed: {response.text}")
                    return False
            else:
                print("⚠️  No cases found")
                return True
        else:
            print(f"❌ Cases list failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Cases endpoints error: {e}")
        traceback.print_exc()
        return False

def test_error_handling(client):
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    try:
        # Test 404
        response = client.get("/api/cases/nonexistent-case")
        print(f"   GET /api/cases/nonexistent-case - Status: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 404 handling working")
        else:
            print(f"⚠️  Expected 404, got {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all server tests"""
    print("🚀 Starting FastAPI Server Testing\n")
    
    # Test 1: Import app
    app = test_app_import()
    if app is None:
        print("\n🛑 Stopping: Cannot import app")
        return
    
    # Test 2: Create test client
    client = test_app_startup(app)
    if client is None:
        print("\n🛑 Stopping: Cannot create test client")
        return
    
    # Test 3: Root endpoint
    if not test_root_endpoint(client):
        print("\n🛑 Stopping: Root endpoint failed")
        return
    
    # Test 4: Cases endpoints
    if not test_cases_endpoints(client):
        print("\n🛑 Cases endpoints failed")
        return
    
    # Test 5: Error handling
    test_error_handling(client)
    
    print("\n✅ All server tests passed!")
    print("\n💡 The FastAPI server appears to be working correctly.")
    print("   If you're still getting 500 errors, the issue might be:")
    print("   - Network connectivity")
    print("   - Server not running on the expected port")
    print("   - Environment differences between test and runtime")

if __name__ == "__main__":
    main()