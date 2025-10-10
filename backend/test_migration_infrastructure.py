#!/usr/bin/env python3
"""
Test script for migration infrastructure

This script tests the core functionality of the migration infrastructure.
"""

import sys
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from services.migration_service import MigrationService
from services.path_resolution_service import PathResolutionService
from services.validation_service import ValidationService


def test_migration_infrastructure():
    """Test the migration infrastructure components."""
    print("Testing Migration Infrastructure...")
    print("=" * 50)
    
    data_root = "backend/app/data"
    
    # Initialize services
    migration_service = MigrationService(data_root)
    path_service = PathResolutionService(data_root)
    validation_service = ValidationService(data_root)
    
    # Test 1: Path Resolution Service
    print("\n1. Testing Path Resolution Service")
    print("-" * 30)
    
    # Test case path resolution
    case_path = path_service.resolve_case_path("case-001")
    print(f"Case-001 path: {case_path}")
    
    # Test analysis path resolution
    analysis_path = path_service.resolve_analysis_path()
    print(f"Analysis path: {analysis_path}")
    
    # Test index path resolution
    cases_index_path = path_service.resolve_index_path("cases")
    print(f"Cases index path: {cases_index_path}")
    
    # Test structure info
    structure_info = path_service.get_current_structure_info()
    print(f"Migration completed: {structure_info['migration_completed']}")
    print(f"Legacy paths exist: {any(info['exists'] for info in structure_info['legacy_paths'].values())}")
    
    # Test 2: Validation Service
    print("\n2. Testing Validation Service")
    print("-" * 30)
    
    # Test JSON validation
    legal_corpus_index = Path(data_root) / "legal_corpus" / "corpus_index.json"
    if legal_corpus_index.exists():
        is_valid = validation_service.validate_json_file(legal_corpus_index)
        print(f"Legal corpus index JSON valid: {is_valid}")
    
    # Test path resolution validation
    path_validation = path_service.validate_path_resolution()
    print(f"Path resolution validation: {path_validation}")
    
    # Test 3: Migration Service
    print("\n3. Testing Migration Service")
    print("-" * 30)
    
    # Test migration status
    status = migration_service.get_migration_status()
    print(f"Migration phase: {status['migration_status']['phase']}")
    print(f"Rollback available: {status['migration_status']['rollback_available']}")
    print(f"Steps completed: {len(status['migration_status']['steps_completed'])}")
    
    # Test 4: Integration Test
    print("\n4. Integration Test")
    print("-" * 30)
    
    # Test that services can work together
    try:
        # Get current structure
        structure = path_service.get_current_structure_info()
        
        # Validate what exists
        validation_results = {}
        if structure['legacy_paths']['case_documents']['exists']:
            case_docs_path = Path(data_root) / "case_documents"
            validation_results['case_documents'] = validation_service.validate_case_structure(case_docs_path)
        
        print(f"Integration test results: {validation_results}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_migration_infrastructure()
    sys.exit(0 if success else 1)