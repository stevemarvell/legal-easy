#!/usr/bin/env python3
"""
Direct API endpoint testing script

This script tests the actual FastAPI endpoints to identify 500 errors.
"""

import requests
import json
import sys
from datetime import datetime


class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health_check(self):
        """Test basic API connectivity"""
        print("🔍 Testing API health check...")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API is accessible")
                return True
            else:
                print(f"❌ API returned status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API - is the server running?")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def test_cases_list(self):
        """Test GET /api/cases endpoint"""
        print("\n🔍 Testing GET /api/cases...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/cases")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                cases = response.json()
                print(f"✅ Cases list successful - {len(cases)} cases")
                
                if cases:
                    print(f"   First case: {cases[0].get('id', 'unknown')} - {cases[0].get('title', 'unknown')}")
                
                return cases
            else:
                print(f"❌ Cases list failed")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Cases list error: {e}")
            return None
    
    def test_specific_case(self, case_id):
        """Test GET /api/cases/{case_id} endpoint"""
        print(f"\n🔍 Testing GET /api/cases/{case_id}...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/cases/{case_id}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                case = response.json()
                print(f"✅ Case detail successful")
                print(f"   Case: {case.get('title', 'unknown')}")
                print(f"   Client: {case.get('client_name', 'unknown')}")
                print(f"   Status: {case.get('status', 'unknown')}")
                return case
            elif response.status_code == 404:
                print(f"❌ Case not found")
                print(f"   Response: {response.text}")
                return None
            elif response.status_code == 500:
                print(f"❌ Internal server error (500)")
                print(f"   Response: {response.text}")
                
                # Try to extract error details
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        print(f"   Error detail: {error_data['detail']}")
                except:
                    pass
                
                return None
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Case detail error: {e}")
            return None
    
    def test_all_cases_individually(self, cases):
        """Test each case individually to find problematic ones"""
        print(f"\n🔍 Testing all {len(cases)} cases individually...")
        
        failed_cases = []
        
        for i, case in enumerate(cases):
            case_id = case.get('id', f'case-{i+1}')
            print(f"\n   Testing case {i+1}/{len(cases)}: {case_id}")
            
            result = self.test_specific_case(case_id)
            if result is None:
                failed_cases.append(case_id)
        
        if failed_cases:
            print(f"\n❌ Failed cases: {failed_cases}")
        else:
            print(f"\n✅ All cases tested successfully")
        
        return failed_cases
    
    def test_nonexistent_case(self):
        """Test with a case ID that doesn't exist"""
        print(f"\n🔍 Testing nonexistent case...")
        
        result = self.test_specific_case("nonexistent-case-id")
        if result is None:
            print("✅ Nonexistent case handled correctly (404 expected)")
        else:
            print("❌ Nonexistent case should return 404")
    
    def test_malformed_case_id(self):
        """Test with malformed case IDs"""
        print(f"\n🔍 Testing malformed case IDs...")
        
        malformed_ids = [
            "",  # Empty string
            "case with spaces",  # Spaces
            "case/with/slashes",  # Slashes
            "case-with-very-long-id-that-might-cause-issues-" + "x" * 100,  # Very long
            "case-with-unicode-🚀",  # Unicode
        ]
        
        for case_id in malformed_ids:
            print(f"   Testing: '{case_id}'")
            try:
                response = self.session.get(f"{self.base_url}/api/cases/{case_id}")
                print(f"      Status: {response.status_code}")
            except Exception as e:
                print(f"      Error: {e}")


def main():
    """Run all API tests"""
    print("🚀 Starting API Endpoint Testing\n")
    
    # Check if server URL is provided
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing API at: {base_url}")
    
    tester = APITester(base_url)
    
    # Test 1: Health check
    if not tester.test_health_check():
        print("\n🛑 Stopping: API not accessible")
        print("💡 Make sure the backend server is running:")
        print("   cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Test 2: Cases list
    cases = tester.test_cases_list()
    if cases is None:
        print("\n🛑 Stopping: Cannot get cases list")
        return
    
    if not cases:
        print("\n⚠️  No cases found in the system")
        return
    
    # Test 3: First case detail
    first_case_id = cases[0].get('id')
    if first_case_id:
        tester.test_specific_case(first_case_id)
    
    # Test 4: All cases (if not too many)
    if len(cases) <= 10:
        tester.test_all_cases_individually(cases)
    else:
        print(f"\n⚠️  Skipping individual case tests ({len(cases)} cases is too many)")
    
    # Test 5: Error cases
    tester.test_nonexistent_case()
    tester.test_malformed_case_id()
    
    print("\n✅ API testing complete!")


if __name__ == "__main__":
    main()