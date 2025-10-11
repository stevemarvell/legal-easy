#!/usr/bin/env python3
"""
Diagnostic script to identify the root cause of Cases API 500 errors

This script will test each component individually to isolate the issue.
"""

import json
import traceback
from pathlib import Path
from datetime import datetime
from pydantic import ValidationError

# Import the components we need to test
from app.services.data_service import DataService
from app.models.case import Case


def test_file_access():
    """Test if we can access the cases index file"""
    print("🔍 Testing file access...")
    
    cases_file = Path("data/cases/cases_index.json")
    
    if not cases_file.exists():
        print(f"❌ Cases file not found: {cases_file}")
        return False
    
    try:
        with open(cases_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ File accessible, size: {len(content)} bytes")
        return True
    except Exception as e:
        print(f"❌ File access error: {e}")
        return False


def test_json_parsing():
    """Test if we can parse the JSON file"""
    print("\n🔍 Testing JSON parsing...")
    
    try:
        cases_file = Path("data/cases/cases_index.json")
        with open(cases_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON parsed successfully")
        print(f"   Data type: {type(data)}")
        print(f"   Length: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and data:
            print(f"   First item keys: {list(data[0].keys())}")
        
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def test_data_service():
    """Test the DataService.load_cases method"""
    print("\n🔍 Testing DataService.load_cases()...")
    
    try:
        cases = DataService.load_cases()
        print(f"✅ DataService.load_cases() successful")
        print(f"   Returned {len(cases)} cases")
        return cases
    except Exception as e:
        print(f"❌ DataService error: {e}")
        traceback.print_exc()
        return None


def test_case_model_validation(cases_data):
    """Test Case model validation with actual data"""
    print("\n🔍 Testing Case model validation...")
    
    if not cases_data:
        print("❌ No cases data to validate")
        return False
    
    validation_results = []
    
    for i, case_data in enumerate(cases_data):
        try:
            case = Case(**case_data)
            print(f"✅ Case {i+1} ({case_data.get('id', 'unknown')}): Valid")
            validation_results.append(True)
        except ValidationError as e:
            print(f"❌ Case {i+1} ({case_data.get('id', 'unknown')}): Validation error")
            print(f"   Error: {e}")
            validation_results.append(False)
        except Exception as e:
            print(f"❌ Case {i+1} ({case_data.get('id', 'unknown')}): Unexpected error")
            print(f"   Error: {e}")
            validation_results.append(False)
    
    success_count = sum(validation_results)
    total_count = len(validation_results)
    print(f"\n📊 Validation Summary: {success_count}/{total_count} cases valid")
    
    return all(validation_results)


def test_specific_case_lookup(cases_data, case_id="case-001"):
    """Test looking up a specific case"""
    print(f"\n🔍 Testing case lookup for '{case_id}'...")
    
    if not cases_data:
        print("❌ No cases data available")
        return None
    
    try:
        case = next((c for c in cases_data if c.get('id') == case_id), None)
        
        if case is None:
            print(f"❌ Case '{case_id}' not found")
            available_ids = [c.get('id', 'unknown') for c in cases_data]
            print(f"   Available case IDs: {available_ids}")
            return None
        
        print(f"✅ Case '{case_id}' found")
        print(f"   Title: {case.get('title', 'Unknown')}")
        
        # Test Case model validation for this specific case
        try:
            case_model = Case(**case)
            print(f"✅ Case model validation successful")
            return case_model
        except Exception as e:
            print(f"❌ Case model validation failed: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Case lookup error: {e}")
        return None


def test_date_parsing(cases_data):
    """Test date parsing for all cases"""
    print("\n🔍 Testing date parsing...")
    
    if not cases_data:
        print("❌ No cases data available")
        return False
    
    date_issues = []
    
    for i, case_data in enumerate(cases_data):
        case_id = case_data.get('id', f'case-{i+1}')
        created_date = case_data.get('created_date')
        
        if not created_date:
            date_issues.append(f"Case {case_id}: Missing created_date")
            continue
        
        try:
            # Test different date parsing methods
            dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
            print(f"✅ Case {case_id}: Date parsed successfully ({dt})")
        except Exception as e:
            date_issues.append(f"Case {case_id}: Date parsing error - {e}")
    
    if date_issues:
        print(f"\n❌ Date parsing issues found:")
        for issue in date_issues:
            print(f"   {issue}")
        return False
    
    print(f"✅ All dates parsed successfully")
    return True


def test_api_endpoint_simulation():
    """Simulate the API endpoint logic"""
    print("\n🔍 Simulating API endpoint logic...")
    
    try:
        # Simulate the get_case endpoint logic
        case_id = "case-001"
        
        # Step 1: Load cases
        cases = DataService.load_cases()
        print(f"✅ Step 1: Loaded {len(cases)} cases")
        
        # Step 2: Find specific case
        case = next((c for c in cases if c.get('id') == case_id), None)
        
        if case is None:
            print(f"❌ Step 2: Case '{case_id}' not found")
            return False
        
        print(f"✅ Step 2: Found case '{case_id}'")
        
        # Step 3: Validate and return (this is where FastAPI would serialize)
        case_model = Case(**case)
        print(f"✅ Step 3: Case model created successfully")
        
        # Step 4: Convert to dict (simulate JSON serialization)
        try:
            case_dict = case_model.model_dump()  # Pydantic v2
        except AttributeError:
            case_dict = case_model.dict()  # Pydantic v1 fallback
        print(f"✅ Step 4: Case serialized to dict")
        
        # Step 5: Convert to JSON (simulate FastAPI response)
        case_json = json.dumps(case_dict, default=str)
        print(f"✅ Step 5: Case serialized to JSON")
        
        return True
        
    except Exception as e:
        print(f"❌ API simulation failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all diagnostic tests"""
    print("🚀 Starting Cases API Diagnostic\n")
    
    # Test 1: File access
    if not test_file_access():
        print("\n🛑 Stopping: Cannot access cases file")
        return
    
    # Test 2: JSON parsing
    cases_data = test_json_parsing()
    if cases_data is None:
        print("\n🛑 Stopping: Cannot parse JSON")
        return
    
    # Test 3: DataService
    service_cases = test_data_service()
    if service_cases is None:
        print("\n🛑 Stopping: DataService failed")
        return
    
    # Test 4: Case model validation
    test_case_model_validation(cases_data)
    
    # Test 5: Specific case lookup
    test_specific_case_lookup(cases_data)
    
    # Test 6: Date parsing
    test_date_parsing(cases_data)
    
    # Test 7: API endpoint simulation
    test_api_endpoint_simulation()
    
    print("\n✅ Diagnostic complete!")
    print("\n💡 If all tests pass but you still get 500 errors, the issue might be:")
    print("   - FastAPI/Uvicorn configuration")
    print("   - CORS settings")
    print("   - Import/module issues")
    print("   - Runtime environment differences")


if __name__ == "__main__":
    main()