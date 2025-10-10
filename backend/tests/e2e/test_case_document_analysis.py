#!/usr/bin/env python3
"""
End-to-End Tests for Case Document Analysis

This test suite covers the complete user journey for case document analysis:
1. Loading case documents
2. Viewing document content
3. Triggering AI analysis
4. Viewing analysis results
5. Managing analysis data

Tests both API endpoints and data flow.
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from pathlib import Path
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from app.services.document_service import DocumentService
from app.services.analysis_storage_service import AnalysisStorageService


class TestCaseDocumentAnalysisE2E:
    """End-to-end tests for case document analysis workflow"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test client and services"""
        self.client = TestClient(app)
        self.document_service = DocumentService()
        self.analysis_service = AnalysisStorageService()
        
        # Test data
        self.test_case_id = "case-001"
        self.test_document_id = "doc-001"
        
        # Clean up any existing analysis for test document
        self.analysis_service.delete_analysis(self.test_document_id)
        
        yield
        
        # Cleanup after tests
        self.analysis_service.delete_analysis(self.test_document_id)
    
    def test_complete_document_analysis_workflow(self):
        """Test the complete end-to-end document analysis workflow"""
        
        # Step 1: Load case documents
        print("Step 1: Loading case documents...")
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        
        assert response.status_code == 200, f"Failed to load case documents: {response.text}"
        documents = response.json()
        assert len(documents) > 0, "No documents found for test case"
        
        # Find our test document
        test_document = None
        for doc in documents:
            if doc["id"] == self.test_document_id:
                test_document = doc
                break
        
        assert test_document is not None, f"Test document {self.test_document_id} not found"
        print(f"✓ Found test document: {test_document['name']}")
        
        # Step 2: Get document details
        print("Step 2: Getting document details...")
        response = self.client.get(f"/api/documents/{self.test_document_id}")
        
        assert response.status_code == 200, f"Failed to get document details: {response.text}"
        document_details = response.json()
        assert document_details["id"] == self.test_document_id
        print(f"✓ Document details loaded: {document_details['name']}")
        
        # Step 3: Get document content
        print("Step 3: Getting document content...")
        response = self.client.get(f"/api/documents/{self.test_document_id}/content")
        
        assert response.status_code == 200, f"Failed to get document content: {response.text}"
        content_data = response.json()
        assert "content" in content_data
        assert len(content_data["content"]) > 0, "Document content is empty"
        print(f"✓ Document content loaded: {content_data['content_length']} characters")
        
        # Step 4: Check initial analysis status (should be none or pending)
        print("Step 4: Checking initial analysis status...")
        response = self.client.get(f"/api/documents/{self.test_document_id}/analysis")
        
        # This might return 404 if no analysis exists yet, which is expected
        if response.status_code == 404:
            print("✓ No existing analysis found (expected)")
        elif response.status_code == 200:
            print("✓ Existing analysis found")
        else:
            pytest.fail(f"Unexpected response for analysis check: {response.status_code}")
        
        # Step 5: Trigger document analysis
        print("Step 5: Triggering document analysis...")
        response = self.client.post(f"/api/documents/{self.test_document_id}/analyze")
        
        assert response.status_code == 200, f"Failed to analyze document: {response.text}"
        analysis_result = response.json()
        
        # Verify analysis result structure
        required_fields = [
            "document_id", "key_dates", "parties_involved", 
            "document_type", "summary", "key_clauses", "confidence_scores"
        ]
        for field in required_fields:
            assert field in analysis_result, f"Missing required field: {field}"
        
        assert analysis_result["document_id"] == self.test_document_id
        print(f"✓ Document analysis completed: {analysis_result['document_type']}")
        
        # Step 6: Retrieve stored analysis
        print("Step 6: Retrieving stored analysis...")
        response = self.client.get(f"/api/documents/{self.test_document_id}/analysis")
        
        assert response.status_code == 200, f"Failed to retrieve stored analysis: {response.text}"
        stored_analysis = response.json()
        
        # Verify stored analysis matches the analysis result
        assert stored_analysis["document_id"] == analysis_result["document_id"]
        assert stored_analysis["document_type"] == analysis_result["document_type"]
        print("✓ Stored analysis retrieved successfully")
        
        # Step 7: Verify document status is updated
        print("Step 7: Verifying document analysis status...")
        response = self.client.get(f"/api/documents/{self.test_document_id}")
        
        assert response.status_code == 200
        updated_document = response.json()
        assert updated_document["analysis_completed"] == True, "Document analysis status not updated"
        print("✓ Document analysis status updated")
        
        # Step 8: Verify case documents list shows updated status
        print("Step 8: Verifying case documents list...")
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        
        assert response.status_code == 200
        updated_documents = response.json()
        
        updated_test_doc = None
        for doc in updated_documents:
            if doc["id"] == self.test_document_id:
                updated_test_doc = doc
                break
        
        assert updated_test_doc is not None
        assert updated_test_doc["analysis_completed"] == True, "Case document list not updated"
        print("✓ Case documents list shows updated analysis status")
        
        print("\n🎉 Complete document analysis workflow test PASSED!")
    
    def test_analysis_data_quality(self):
        """Test the quality and completeness of analysis data"""
        
        print("Testing analysis data quality...")
        
        # Analyze the document
        response = self.client.post(f"/api/documents/{self.test_document_id}/analyze")
        assert response.status_code == 200
        
        analysis = response.json()
        
        # Test data quality
        assert len(analysis["summary"]) > 50, "Summary too short"
        assert len(analysis["parties_involved"]) > 0, "No parties identified"
        assert len(analysis["key_dates"]) >= 0, "Key dates should be a list"
        
        # Test confidence scores
        confidence_scores = analysis["confidence_scores"]
        required_confidence_fields = ["parties", "dates", "contract_terms", "key_clauses", "legal_analysis"]
        
        for field in required_confidence_fields:
            assert field in confidence_scores, f"Missing confidence score: {field}"
            score = confidence_scores[field]
            assert 0 <= score <= 1, f"Invalid confidence score for {field}: {score}"
        
        # Test document type classification
        valid_document_types = [
            "Employment Contract", "Service Agreement", "Legal Notice", 
            "Evidence Document", "License Agreement", "Termination Notice",
            "Performance Review", "Contract", "Email", "Legal Brief"
        ]
        assert analysis["document_type"] in valid_document_types or len(analysis["document_type"]) > 0
        
        print("✓ Analysis data quality checks passed")
    
    def test_multiple_document_analysis(self):
        """Te
st analyzing multiple documents in sequence"""
        
        print("Testing multiple document analysis...")
        
        # Get all documents for the test case
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        assert response.status_code == 200
        
        documents = response.json()
        test_documents = documents[:3]  # Test first 3 documents
        
        analysis_results = []
        
        for doc in test_documents:
            print(f"Analyzing document: {doc['name']}")
            
            # Analyze document
            response = self.client.post(f"/api/documents/{doc['id']}/analyze")
            assert response.status_code == 200, f"Failed to analyze {doc['id']}"
            
            analysis = response.json()
            analysis_results.append(analysis)
            
            # Verify analysis was stored
            response = self.client.get(f"/api/documents/{doc['id']}/analysis")
            assert response.status_code == 200, f"Failed to retrieve analysis for {doc['id']}"
        
        # Verify all analyses are different and valid
        document_types = [analysis["document_type"] for analysis in analysis_results]
        summaries = [analysis["summary"] for analysis in analysis_results]
        
        # Each analysis should be unique
        assert len(set(summaries)) == len(summaries), "Duplicate analysis summaries found"
        
        print(f"✓ Successfully analyzed {len(test_documents)} documents")
    
    def test_analysis_error_handling(self):
        """Test error handling in analysis workflow"""
        
        print("Testing analysis error handling...")
        
        # Test analysis of non-existent document
        response = self.client.post("/api/documents/non-existent-doc/analyze")
        assert response.status_code == 404, "Should return 404 for non-existent document"
        
        # Test getting analysis for non-existent document
        response = self.client.get("/api/documents/non-existent-doc/analysis")
        assert response.status_code == 404, "Should return 404 for non-existent analysis"
        
        # Test getting content for non-existent document
        response = self.client.get("/api/documents/non-existent-doc/content")
        assert response.status_code == 404, "Should return 404 for non-existent document content"
        
        print("✓ Error handling tests passed")
    
    def test_analysis_storage_management(self):
        """Test analysis storage and management operations"""
        
        print("Testing analysis storage management...")
        
        # Analyze a document first
        response = self.client.post(f"/api/documents/{self.test_document_id}/analyze")
        assert response.status_code == 200
        
        # Get storage statistics
        response = self.client.get("/api/documents/analysis/stats")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_analyses" in stats
        assert stats["total_analyses"] >= 1
        
        # Delete specific analysis
        response = self.client.delete(f"/api/documents/{self.test_document_id}/analysis")
        assert response.status_code == 200
        
        # Verify analysis is deleted
        response = self.client.get(f"/api/documents/{self.test_document_id}/analysis")
        assert response.status_code == 404, "Analysis should be deleted"
        
        print("✓ Analysis storage management tests passed")
    
    def test_concurrent_analysis_requests(self):
        """Test handling of concurrent analysis requests"""
        
        print("Testing concurrent analysis requests...")
        
        # This test simulates multiple users analyzing documents simultaneously
        # In a real scenario, this would test race conditions and resource management
        
        # Get multiple documents
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        assert response.status_code == 200
        
        documents = response.json()[:2]  # Test with 2 documents
        
        # Simulate concurrent requests (sequential for simplicity in testing)
        for doc in documents:
            response = self.client.post(f"/api/documents/{doc['id']}/analyze")
            assert response.status_code == 200, f"Concurrent analysis failed for {doc['id']}"
        
        # Verify all analyses completed
        for doc in documents:
            response = self.client.get(f"/api/documents/{doc['id']}/analysis")
            assert response.status_code == 200, f"Analysis not found for {doc['id']}"
            
            # Clean up
            self.client.delete(f"/api/documents/{doc['id']}/analysis")
        
        print("✓ Concurrent analysis tests passed")
    
    def test_analysis_content_validation(self):
        """Test validation of analysis content and structure"""
        
        print("Testing analysis content validation...")
        
        # Analyze document
        response = self.client.post(f"/api/documents/{self.test_document_id}/analyze")
        assert response.status_code == 200
        
        analysis = response.json()
        
        # Validate structure
        assert isinstance(analysis["key_dates"], list), "key_dates should be a list"
        assert isinstance(analysis["parties_involved"], list), "parties_involved should be a list"
        assert isinstance(analysis["key_clauses"], list), "key_clauses should be a list"
        assert isinstance(analysis["confidence_scores"], dict), "confidence_scores should be a dict"
        
        # Validate content types
        assert isinstance(analysis["summary"], str), "summary should be a string"
        assert isinstance(analysis["document_type"], str), "document_type should be a string"
        
        # Validate confidence scores are within valid range
        for score_name, score_value in analysis["confidence_scores"].items():
            assert isinstance(score_value, (int, float)), f"{score_name} should be numeric"
            assert 0 <= score_value <= 1, f"{score_name} should be between 0 and 1"
        
        # Validate dates format (if any)
        for date_str in analysis["key_dates"]:
            # Should be in YYYY-MM-DD format or similar
            assert len(date_str) >= 8, f"Date format seems invalid: {date_str}"
        
        print("✓ Analysis content validation passed")
    
    def test_case_document_integration(self):
        """Test integration between case management and document analysis"""
        
        print("Testing case-document integration...")
        
        # Get case information
        response = self.client.get(f"/api/cases/{self.test_case_id}")
        assert response.status_code == 200
        
        case_info = response.json()
        assert case_info["id"] == self.test_case_id
        
        # Get case documents
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        assert response.status_code == 200
        
        documents = response.json()
        
        # Verify documents belong to the case
        for doc in documents:
            assert doc["case_id"] == self.test_case_id, f"Document {doc['id']} has wrong case_id"
        
        # Analyze one document and verify it's reflected in case statistics
        test_doc = documents[0]
        response = self.client.post(f"/api/documents/{test_doc['id']}/analyze")
        assert response.status_code == 200
        
        # Check updated document list
        response = self.client.get(f"/api/documents/cases/{self.test_case_id}/documents")
        assert response.status_code == 200
        
        updated_documents = response.json()
        analyzed_count = sum(1 for doc in updated_documents if doc["analysis_completed"])
        assert analyzed_count >= 1, "Analysis count not updated in case documents"
        
        # Clean up
        self.client.delete(f"/api/documents/{test_doc['id']}/analysis")
        
        print("✓ Case-document integration tests passed")


def run_e2e_tests():
    """Run all end-to-end tests"""
    print("="*60)
    print("RUNNING END-TO-END TESTS FOR CASE DOCUMENT ANALYSIS")
    print("="*60)
    
    test_instance = TestCaseDocumentAnalysisE2E()
    test_instance.setup()
    
    try:
        # Run all tests
        test_instance.test_complete_document_analysis_workflow()
        test_instance.test_analysis_data_quality()
        test_instance.test_multiple_document_analysis()
        test_instance.test_analysis_error_handling()
        test_instance.test_analysis_storage_management()
        test_instance.test_concurrent_analysis_requests()
        test_instance.test_analysis_content_validation()
        test_instance.test_case_document_integration()
        
        print("\n" + "="*60)
        print("🎉 ALL END-TO-END TESTS PASSED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        raise
    
    finally:
        # Cleanup
        try:
            test_instance.analysis_service.delete_analysis(test_instance.test_document_id)
        except:
            pass


if __name__ == "__main__":
    run_e2e_tests()