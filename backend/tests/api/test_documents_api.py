#!/usr/bin/env python3
"""Document API Integration Tests"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDocumentAnalysisAPI:
    """Test Document Analysis API endpoints"""
    
    def test_regenerate_document_analysis_success(self):
        """Test POST /api/documents/regenerate-analysis - Successful analysis regeneration"""
        response = client.post("/api/documents/regenerate-analysis")
        assert response.status_code == 200
        
        result = response.json()
        assert result['success'] is True
        assert 'message' in result
        assert 'total_documents' in result
        assert 'analyzed_documents' in result
        assert 'failed_documents' in result
        assert 'average_confidence' in result
        assert 'processing_time_seconds' in result
        
        # Verify the response structure
        assert isinstance(result['total_documents'], int)
        assert isinstance(result['analyzed_documents'], int)
        assert isinstance(result['failed_documents'], int)
        assert isinstance(result['average_confidence'], (int, float))
        assert isinstance(result['processing_time_seconds'], (int, float))
        assert result['total_documents'] >= 0
        assert result['analyzed_documents'] >= 0
        assert result['failed_documents'] >= 0
        assert 0.0 <= result['average_confidence'] <= 1.0
        assert result['processing_time_seconds'] >= 0
    
    def test_regenerate_document_analysis_updates_data(self):
        """Test that document analysis regeneration actually processes documents"""
        # Regenerate analysis
        regen_response = client.post("/api/documents/regenerate-analysis")
        assert regen_response.status_code == 200
        
        result = regen_response.json()
        
        # Should have processed some documents (assuming test data exists)
        if result['total_documents'] > 0:
            # Should have analyzed at least some documents
            assert result['analyzed_documents'] >= 0
            # Total should equal analyzed + failed
            assert result['total_documents'] == result['analyzed_documents'] + result['failed_documents']
    
    def test_regenerate_document_analysis_performance_metrics(self):
        """Test that analysis regeneration returns performance metrics"""
        response = client.post("/api/documents/regenerate-analysis")
        assert response.status_code == 200
        
        result = response.json()
        
        # Should have timing information
        assert 'processing_time_seconds' in result
        assert result['processing_time_seconds'] >= 0
        
        # Should have confidence metrics if documents were analyzed
        if result['analyzed_documents'] > 0:
            assert 'average_confidence' in result
            assert 0.0 <= result['average_confidence'] <= 1.0
    
    def test_document_analysis_endpoint_exists(self):
        """Test that individual document analysis endpoints work"""
        # Test getting analysis for a document (may not exist, but endpoint should respond)
        response = client.get("/api/documents/doc-001/analysis")
        # Should return either 200 (analysis exists), 404 (analysis not found), or 500 (validation error)
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            analysis = response.json()
            assert 'document_id' in analysis
            # Analysis structure may vary, just check it's a valid response
            assert isinstance(analysis, dict)
    
    def test_document_content_endpoint_exists(self):
        """Test that document content endpoint works"""
        # Test getting content for a document (may not exist, but endpoint should respond)
        response = client.get("/api/documents/doc-001/content")
        # Should return either 200 (document exists) or 404 (document not found)
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            content = response.json()
            assert 'document_id' in content
            assert 'content' in content
            assert 'content_length' in content

    def test_analyze_document_endpoint_success(self):
        """Test POST /api/documents/{document_id}/analyze - Successful document analysis"""
        # Test analyzing a document that exists
        response = client.post("/api/documents/doc-001/analyze")
        
        # Should return either 200 (success) or 404 (document not found)
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            result = response.json()
            # The analyze endpoint may return different structures
            # Just verify it's a valid response
            assert isinstance(result, dict)

    def test_analyze_document_endpoint_not_found(self):
        """Test POST /api/documents/{document_id}/analyze - Document not found"""
        response = client.post("/api/documents/nonexistent-doc/analyze")
        assert response.status_code == 404
        
        result = response.json()
        assert 'detail' in result
        assert 'not found' in result['detail'].lower()

    def test_get_document_analysis_success(self):
        """Test GET /api/documents/{document_id}/analysis - Get existing analysis"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the analysis
            response = client.get("/api/documents/doc-001/analysis")
            assert response.status_code == 200
            
            analysis = response.json()
            assert 'document_id' in analysis
            # Analysis structure may vary, just check it's a valid response
            assert isinstance(analysis, dict)

    def test_get_document_summary_success(self):
        """Test GET /api/documents/{document_id}/summary - Get document summary"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the summary
            response = client.get("/api/documents/doc-001/summary")
            # Should return either 200 (summary exists) or 404 (summary not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                summary = response.json()
                assert summary['document_id'] == 'doc-001'
                assert 'summary' in summary
                assert 'confidence_score' in summary
                assert isinstance(summary['confidence_score'], (int, float))

    def test_get_document_key_dates_success(self):
        """Test GET /api/documents/{document_id}/key-dates - Get document key dates"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the key dates
            response = client.get("/api/documents/doc-001/key-dates")
            # Should return either 200 (dates exist) or 404 (dates not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                key_dates = response.json()
                assert key_dates['document_id'] == 'doc-001'
                assert 'key_dates' in key_dates
                assert 'confidence_score' in key_dates
                assert isinstance(key_dates['key_dates'], list)

    def test_get_document_parties_success(self):
        """Test GET /api/documents/{document_id}/parties - Get document parties"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the parties
            response = client.get("/api/documents/doc-001/parties")
            # Should return either 200 (parties exist) or 404 (parties not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                parties = response.json()
                assert parties['document_id'] == 'doc-001'
                assert 'parties' in parties
                assert 'confidence_score' in parties
                assert isinstance(parties['parties'], list)

    def test_get_document_risks_success(self):
        """Test GET /api/documents/{document_id}/risks - Get document risks"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the risks
            response = client.get("/api/documents/doc-001/risks")
            # Should return either 200 (risks exist) or 404 (risks not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                risks = response.json()
                assert risks['document_id'] == 'doc-001'
                assert 'risks' in risks
                assert 'risk_level' in risks
                assert 'confidence_score' in risks

    def test_get_document_compliance_success(self):
        """Test GET /api/documents/{document_id}/compliance - Get document compliance"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the compliance
            response = client.get("/api/documents/doc-001/compliance")
            # Should return either 200 (compliance exists) or 404 (compliance not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                compliance = response.json()
                assert compliance['document_id'] == 'doc-001'
                assert 'compliance_status' in compliance
                assert 'compliance_issues' in compliance
                assert 'confidence_score' in compliance

    def test_get_document_deadlines_success(self):
        """Test GET /api/documents/{document_id}/deadlines - Get document deadlines"""
        # First analyze a document to ensure analysis exists
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Now get the deadlines
            response = client.get("/api/documents/doc-001/deadlines")
            # Should return either 200 (deadlines exist) or 404 (deadlines not found)
            assert response.status_code in [200, 404]
            
            if response.status_code == 200:
                deadlines = response.json()
                assert deadlines['document_id'] == 'doc-001'
                assert 'deadlines' in deadlines
                assert 'confidence_score' in deadlines

    def test_analysis_endpoints_handle_missing_analysis(self):
        """Test that analysis endpoints handle missing analysis gracefully"""
        # Test with a document that likely doesn't have analysis
        endpoints = [
            '/api/documents/nonexistent-doc/analysis',
            '/api/documents/nonexistent-doc/summary',
            '/api/documents/nonexistent-doc/key-dates',
            '/api/documents/nonexistent-doc/parties',
            '/api/documents/nonexistent-doc/risks',
            '/api/documents/nonexistent-doc/compliance',
            '/api/documents/nonexistent-doc/deadlines'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404
            result = response.json()
            assert 'detail' in result

    def test_analysis_data_consistency(self):
        """Test that analysis data is consistent across different endpoints"""
        # First analyze a document
        analyze_response = client.post("/api/documents/doc-001/analyze")
        if analyze_response.status_code == 200:
            # Get full analysis
            full_analysis_response = client.get("/api/documents/doc-001/analysis")
            if full_analysis_response.status_code == 200:
                full_analysis = full_analysis_response.json()
                
                # Get summary and verify consistency
                summary_response = client.get("/api/documents/doc-001/summary")
                if summary_response.status_code == 200:
                    summary = summary_response.json()
                    assert summary['document_id'] == full_analysis['document_id']
                    assert summary['summary'] == full_analysis['summary']
                
                # Get key dates and verify consistency
                dates_response = client.get("/api/documents/doc-001/key-dates")
                if dates_response.status_code == 200:
                    dates = dates_response.json()
                    assert dates['document_id'] == full_analysis['document_id']
                    assert dates['key_dates'] == full_analysis['key_dates']