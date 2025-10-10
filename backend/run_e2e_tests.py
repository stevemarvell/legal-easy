#!/usr/bin/env python3
"""
End-to-End Test Runner for Case Document Analysis

This script runs comprehensive end-to-end tests for the case document analysis feature.
It tests both the backend API and the complete user workflow.
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path

def check_backend_health():
    """Check if the backend server is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend_health():
    """Check if the frontend server is running"""
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    backend_dir = Path(__file__).parent
    
    # Start backend server in background
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], cwd=backend_dir)
    
    # Wait for server to start
    for i in range(30):  # Wait up to 30 seconds
        if check_backend_health():
            print("✓ Backend server is running")
            return process
        time.sleep(1)
    
    print("❌ Failed to start backend server")
    process.terminate()
    return None

def run_backend_tests():
    """Run backend end-to-end tests"""
    print("\n" + "="*60)
    print("RUNNING BACKEND END-TO-END TESTS")
    print("="*60)
    
    try:
        # Run the backend E2E tests
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/e2e/test_case_document_analysis.py", 
            "-v", "--tb=short"
        ], cwd=Path(__file__).parent, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Failed to run backend tests: {e}")
        return False

def run_api_smoke_tests():
    """Run quick API smoke tests"""
    print("\n" + "="*60)
    print("RUNNING API SMOKE TESTS")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    tests = [
        ("Health Check", "GET", "/health"),
        ("Root Endpoint", "GET", "/"),
        ("Case Documents", "GET", "/api/documents/cases/case-001/documents"),
        ("Specific Document", "GET", "/api/documents/doc-001"),
        ("Document Content", "GET", "/api/documents/doc-001/content"),
        ("Cases List", "GET", "/api/cases/"),
        ("Specific Case", "GET", "/api/cases/case-001"),
        ("Case Statistics", "GET", "/api/cases/statistics"),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, method, endpoint in tests:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                continue  # Skip non-GET for smoke tests
            
            if response.status_code == 200:
                print(f"✓ {test_name}: {response.status_code}")
                passed += 1
            else:
                print(f"❌ {test_name}: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"❌ {test_name}: {str(e)}")
            failed += 1
    
    print(f"\nSmoke Tests: {passed} passed, {failed} failed")
    return failed == 0

def run_document_analysis_test():
    """Run a specific document analysis test"""
    print("\n" + "="*60)
    print("RUNNING DOCUMENT ANALYSIS TEST")
    print("="*60)
    
    base_url = "http://localhost:8000"
    test_doc_id = "doc-002"  # Use a different document for testing
    
    try:
        # Step 1: Get document details
        print("1. Getting document details...")
        response = requests.get(f"{base_url}/api/documents/{test_doc_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get document: {response.status_code}")
            return False
        
        doc = response.json()
        print(f"✓ Document: {doc['name']}")
        
        # Step 2: Analyze document
        print("2. Analyzing document...")
        response = requests.post(f"{base_url}/api/documents/{test_doc_id}/analyze")
        if response.status_code != 200:
            print(f"❌ Failed to analyze document: {response.status_code}")
            return False
        
        analysis = response.json()
        print(f"✓ Analysis completed: {analysis['document_type']}")
        
        # Step 3: Retrieve stored analysis
        print("3. Retrieving stored analysis...")
        response = requests.get(f"{base_url}/api/documents/{test_doc_id}/analysis")
        if response.status_code != 200:
            print(f"❌ Failed to retrieve analysis: {response.status_code}")
            return False
        
        stored_analysis = response.json()
        print(f"✓ Analysis retrieved: {stored_analysis['document_type']}")
        
        # Step 4: Verify document status updated
        print("4. Verifying document status...")
        response = requests.get(f"{base_url}/api/documents/{test_doc_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get updated document: {response.status_code}")
            return False
        
        updated_doc = response.json()
        if not updated_doc.get('analysis_completed'):
            print("❌ Document analysis status not updated")
            return False
        
        print("✓ Document status updated")
        
        # Cleanup
        print("5. Cleaning up...")
        requests.delete(f"{base_url}/api/documents/{test_doc_id}/analysis")
        print("✓ Cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Document analysis test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Starting End-to-End Tests for Case Document Analysis")
    print("="*60)
    
    # Check if backend is already running
    if not check_backend_health():
        print("Backend not running, starting it...")
        backend_process = start_backend()
        if not backend_process:
            print("❌ Failed to start backend server")
            return 1
    else:
        print("✓ Backend server is already running")
        backend_process = None
    
    try:
        # Run tests
        all_passed = True
        
        # 1. API Smoke Tests
        if not run_api_smoke_tests():
            all_passed = False
        
        # 2. Document Analysis Test
        if not run_document_analysis_test():
            all_passed = False
        
        # 3. Backend E2E Tests
        if not run_backend_tests():
            all_passed = False
        
        # Summary
        print("\n" + "="*60)
        if all_passed:
            print("🎉 ALL TESTS PASSED!")
            print("The case document analysis feature is working correctly.")
        else:
            print("❌ SOME TESTS FAILED!")
            print("Please check the output above for details.")
        print("="*60)
        
        return 0 if all_passed else 1
        
    finally:
        # Cleanup
        if backend_process:
            print("\nStopping backend server...")
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)