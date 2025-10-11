#!/usr/bin/env python3
"""
Comprehensive test suite for Documents API

This test suite ensures the Documents API works correctly and prevents regressions.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.services.data_service import DataService
from app.services.ai_service import AIService


class TestDocumentsAPI:
    """Comprehensive test suite for Documents API endpoints"""
    
    def setup_method(self):
        """Set up test client and sample data"""
        self.client = TestClient(app)
        self.sample_documents = [
            {
                "id": "doc-001",
                "name": "Employment Contract - John Doe",
                "case_id": "case-001",
                "type": "Contract",
                "size": 15420,
                "upload_date": "2024-01-15T10:30:00Z",
                "content_preview": "EMPLOYMENT AGREEMENT between ABC Corp and John Doe...",
                "analysis_completed": True
            },
            {
                "id": "doc-002",
                "name": "Termination Notice",
                "case_id": "case-001",
                "type": "Legal Brief",
                "size": 8750,
                "upload_date": "2024-01-12T14:15:00Z",
                "content_preview": "NOTICE OF TERMINATION - This letter serves as formal notice...",
                "analysis_completed": False
            }
        ]
        
        self.sample_analysis = {
            "document_id": "doc-001",
            "key_dates": ["2022-03-15", "2024-01-12"],
            "parties_involved": ["John Doe", "ABC Corp"],
            "document_type": "Employment Contract",
            "summary": "Employment agreement for software engineer position...",
            "key_clauses": ["At-will employment clause", "Confidentiality agreement"],
            "confidence_scores": {"parties": 0.95, "dates": 0.98, "summary": 0.87},
            "overall_confidence": 0.93,
            "uncertainty_flags": []
        }
    
    def test_get_case_documents_success(self):
        """Test GET /api/documents/cases/{case_id}/documents returns documents successfully"""
        with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
            response = self.client.get("/api/documents/cases/case-001/documents")
            
            assert response.status_code == 200
            documents = response.json()
            assert len(documents) == 2
            assert documents[0]['id'] == 'doc-001'
            assert documents[1]['id'] == 'doc-002'
    
    def test_get_case_documents_empty_list(self):
        """Test GET /api/documents/cases/{case_id}/documents with no documents"""
        with patch.object(DataService, 'load_case_documents', return_value=[]):
            response = self.client.get("/api/documents/cases/case-001/documents")
            
            assert response.status_code == 200
            assert response.json() == []
    
    def test_get_case_documents_data_service_error(self):
        """Test GET /api/documents/cases/{case_id}/documents when DataService raises exception"""
        with patch.object(DataService, 'load_case_documents', side_effect=Exception("File error")):
            response = self.client.get("/api/documents/cases/case-001/documents")
            
            assert response.status_code == 500
            assert "Failed to get case documents" in response.json()['detail']
    
    def test_get_document_by_id_success(self):
        """Test GET /api/documents/{document_id} returns specific document"""
        # Mock the search through all cases
        sample_cases = [{"id": "case-001", "documents": ["doc-001", "doc-002"]}]
        
        with patch.object(DataService, 'load_cases', return_value=sample_cases):
            with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
                response = self.client.get("/api/documents/doc-001")
                
                assert response.status_code == 200
                document = response.json()
                assert document['id'] == 'doc-001'
                assert document['name'] == 'Employment Contract - John Doe'
    
    def test_get_document_by_id_not_found(self):
        """Test GET /api/documents/{document_id} with nonexistent document"""
        sample_cases = [{"id": "case-001", "documents": ["doc-001", "doc-002"]}]
        
        with patch.object(DataService, 'load_cases', return_value=sample_cases):
            with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
                response = self.client.get("/api/documents/nonexistent-doc")
                
                assert response.status_code == 404
                assert "Document with ID nonexistent-doc not found" in response.json()['detail']
    
    def test_get_document_analysis_success(self):
        """Test GET /api/documents/{document_id}/analysis returns analysis"""
        with patch.object(AIService, 'load_existing_analysis', return_value=self.sample_analysis):
            response = self.client.get("/api/documents/doc-001/analysis")
            
            assert response.status_code == 200
            analysis = response.json()
            assert analysis['document_id'] == 'doc-001'
            assert 'key_dates' in analysis
            assert 'parties_involved' in analysis
    
    def test_get_document_analysis_not_found(self):
        """Test GET /api/documents/{document_id}/analysis when no analysis exists"""
        with patch.object(AIService, 'load_existing_analysis', return_value=None):
            response = self.client.get("/api/documents/doc-001/analysis")
            
            assert response.status_code == 404
            assert "Analysis for document doc-001 not found" in response.json()['detail']
    
    def test_analyze_document_success(self):
        """Test POST /api/documents/{document_id}/analyze performs analysis"""
        mock_content = "Sample document content for analysis"
        
        with patch.object(DataService, 'load_document_content', return_value=mock_content):
            with patch.object(AIService, 'analyze_document', return_value=self.sample_analysis):
                with patch.object(AIService, 'save_analysis'):
                    response = self.client.post("/api/documents/doc-001/analyze")
                    
                    assert response.status_code == 200
                    analysis = response.json()
                    assert analysis['document_id'] == 'doc-001'
    
    def test_analyze_document_not_found(self):
        """Test POST /api/documents/{document_id}/analyze with nonexistent document"""
        with patch.object(DataService, 'load_document_content', return_value=None):
            response = self.client.post("/api/documents/doc-001/analyze")
            
            assert response.status_code == 404
            assert "Document with ID doc-001 not found" in response.json()['detail']
    
    def test_analyze_document_ai_service_error(self):
        """Test POST /api/documents/{document_id}/analyze when AI service fails"""
        mock_content = "Sample document content"
        
        with patch.object(DataService, 'load_document_content', return_value=mock_content):
            with patch.object(AIService, 'analyze_document', side_effect=Exception("AI service error")):
                response = self.client.post("/api/documents/doc-001/analyze")
                
                assert response.status_code == 500
                assert "Failed to analyze document" in response.json()['detail']
    
    def test_get_document_content_success(self):
        """Test GET /api/documents/{document_id}/content returns document content"""
        mock_content = "This is the full document content for testing purposes."
        
        with patch.object(DataService, 'load_document_content', return_value=mock_content):
            response = self.client.get("/api/documents/doc-001/content")
            
            assert response.status_code == 200
            content_response = response.json()
            assert content_response['document_id'] == 'doc-001'
            assert content_response['content'] == mock_content
            assert content_response['content_length'] == len(mock_content)
    
    def test_get_document_content_not_found(self):
        """Test GET /api/documents/{document_id}/content with nonexistent document"""
        with patch.object(DataService, 'load_document_content', return_value=None):
            response = self.client.get("/api/documents/doc-001/content")
            
            assert response.status_code == 404
            assert "Document with ID doc-001 not found" in response.json()['detail']
    
    def test_delete_document_analysis_success(self):
        """Test DELETE /api/documents/{document_id}/analysis removes analysis"""
        with patch.object(AIService, 'load_existing_analysis', return_value=self.sample_analysis):
            response = self.client.delete("/api/documents/doc-001/analysis")
            
            assert response.status_code == 200
            assert "deleted successfully" in response.json()['message']
    
    def test_delete_document_analysis_not_found(self):
        """Test DELETE /api/documents/{document_id}/analysis when no analysis exists"""
        with patch.object(AIService, 'load_existing_analysis', return_value=None):
            response = self.client.delete("/api/documents/doc-001/analysis")
            
            assert response.status_code == 404
            assert "No analysis found for document doc-001" in response.json()['detail']
    
    def test_document_data_structure_consistency(self):
        """Test that document data structure is consistent"""
        with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
            # Test that we can access document data as dictionaries
            documents = DataService.load_case_documents("case-001")
            
            for document in documents:
                # These should work (dictionary access)
                assert 'id' in document
                assert document.get('id') is not None
                assert document['name'] is not None
                
                # Check required fields
                required_fields = ['id', 'name', 'case_id', 'type', 'size', 'upload_date']
                for field in required_fields:
                    assert field in document, f"Missing required field: {field}"
    
    def test_document_response_format(self):
        """Test that document response has correct format"""
        with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
            response = self.client.get("/api/documents/cases/case-001/documents")
            
            assert response.status_code == 200
            documents = response.json()
            
            for document in documents:
                # Check all required fields are present
                required_fields = ['id', 'name', 'case_id', 'type', 'size', 'upload_date']
                
                for field in required_fields:
                    assert field in document, f"Missing required field: {field}"
                
                # Check data types
                assert isinstance(document['id'], str)
                assert isinstance(document['name'], str)
                assert isinstance(document['size'], int)
                assert isinstance(document['analysis_completed'], bool)
    
    def test_edge_cases(self):
        """Test various edge cases"""
        with patch.object(DataService, 'load_case_documents', return_value=self.sample_documents):
            # Test empty document ID
            response = self.client.get("/api/documents/")
            assert response.status_code in [404, 405]  # Depends on FastAPI routing
            
            # Test document ID with special characters
            response = self.client.get("/api/documents/doc-with-special-chars-!@#")
            assert response.status_code == 404
            
            # Test very long document ID
            long_id = "doc-" + "x" * 1000
            response = self.client.get(f"/api/documents/{long_id}")
            assert response.status_code == 404


class TestDocumentAnalysisWorkflow:
    """Test the complete document analysis workflow"""
    
    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_complete_analysis_workflow(self):
        """Test the complete workflow from document upload to analysis"""
        document_id = "doc-001"
        mock_content = "Sample employment contract content"
        mock_analysis = {
            "document_id": document_id,
            "key_dates": ["2024-01-15"],
            "parties_involved": ["Employee", "Company"],
            "document_type": "Contract",
            "summary": "Employment agreement",
            "key_clauses": ["Employment terms"],
            "confidence_scores": {"parties": 0.9},
            "overall_confidence": 0.85,
            "uncertainty_flags": []
        }
        
        # Step 1: Check if analysis exists (should not exist initially)
        with patch.object(AIService, 'load_existing_analysis', return_value=None):
            response = self.client.get(f"/api/documents/{document_id}/analysis")
            assert response.status_code == 404
        
        # Step 2: Perform analysis
        with patch.object(DataService, 'load_document_content', return_value=mock_content):
            with patch.object(AIService, 'analyze_document', return_value=mock_analysis):
                with patch.object(AIService, 'save_analysis'):
                    response = self.client.post(f"/api/documents/{document_id}/analyze")
                    assert response.status_code == 200
                    analysis = response.json()
                    assert analysis['document_id'] == document_id
        
        # Step 3: Retrieve analysis (should now exist)
        with patch.object(AIService, 'load_existing_analysis', return_value=mock_analysis):
            response = self.client.get(f"/api/documents/{document_id}/analysis")
            assert response.status_code == 200
            analysis = response.json()
            assert analysis['document_id'] == document_id
        
        # Step 4: Delete analysis
        with patch.object(AIService, 'load_existing_analysis', return_value=mock_analysis):
            response = self.client.delete(f"/api/documents/{document_id}/analysis")
            assert response.status_code == 200


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"])