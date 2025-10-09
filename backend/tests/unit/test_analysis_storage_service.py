import pytest
import tempfile
import os
from datetime import date
from pathlib import Path
from app.services.analysis_storage_service import AnalysisStorageService
from app.models.document import DocumentAnalysis


class TestAnalysisStorageService:
    """Test the AnalysisStorageService class"""
    
    @pytest.fixture
    def temp_storage_service(self):
        """Create a temporary storage service for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a service with temporary storage
            service = AnalysisStorageService()
            # Override the storage directory to use temp directory
            service.storage_dir = Path(temp_dir)
            service.storage_file = service.storage_dir / "test_analysis_results.json"
            service._ensure_storage_file()
            yield service
    
    @pytest.fixture
    def sample_analysis(self):
        """Create a sample document analysis for testing"""
        return DocumentAnalysis(
            document_id="test-doc-001",
            key_dates=[date(2024, 1, 15), date(2024, 2, 1)],
            parties_involved=["John Doe", "Company Inc"],
            document_type="Employment Contract",
            summary="Test document analysis summary",
            key_clauses=["Test clause 1", "Test clause 2"],
            confidence_scores={"parties": 0.95, "dates": 0.98, "contract_terms": 0.92}
        )
    
    def test_init_creates_storage_file(self, temp_storage_service):
        """Test that initialization creates the storage file"""
        assert temp_storage_service.storage_file.exists()
        
        # Check file structure
        import json
        with open(temp_storage_service.storage_file, 'r') as f:
            data = json.load(f)
        
        assert "metadata" in data
        assert "analyses" in data
        assert data["metadata"]["total_analyses"] == 0
    
    def test_save_and_retrieve_analysis(self, temp_storage_service, sample_analysis):
        """Test saving and retrieving analysis"""
        # Save analysis
        success = temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        assert success is True
        
        # Retrieve analysis
        retrieved = temp_storage_service.get_analysis("test-doc-001")
        assert retrieved is not None
        assert retrieved.document_id == sample_analysis.document_id
        assert retrieved.parties_involved == sample_analysis.parties_involved
        assert retrieved.key_dates == sample_analysis.key_dates
        assert retrieved.document_type == sample_analysis.document_type
        assert retrieved.summary == sample_analysis.summary
        assert retrieved.key_clauses == sample_analysis.key_clauses
        assert retrieved.confidence_scores == sample_analysis.confidence_scores
    
    def test_has_analysis(self, temp_storage_service, sample_analysis):
        """Test checking if analysis exists"""
        # Initially should not exist
        assert temp_storage_service.has_analysis("test-doc-001") is False
        
        # Save analysis
        temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        
        # Now should exist
        assert temp_storage_service.has_analysis("test-doc-001") is True
        assert temp_storage_service.has_analysis("non-existent") is False
    
    def test_delete_analysis(self, temp_storage_service, sample_analysis):
        """Test deleting analysis"""
        # Save analysis first
        temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        assert temp_storage_service.has_analysis("test-doc-001") is True
        
        # Delete analysis
        success = temp_storage_service.delete_analysis("test-doc-001")
        assert success is True
        assert temp_storage_service.has_analysis("test-doc-001") is False
        
        # Try to delete non-existent analysis
        success = temp_storage_service.delete_analysis("non-existent")
        assert success is False
    
    def test_get_all_analyses(self, temp_storage_service, sample_analysis):
        """Test getting all analyses"""
        # Initially empty
        all_analyses = temp_storage_service.get_all_analyses()
        assert len(all_analyses) == 0
        
        # Save multiple analyses
        analysis1 = sample_analysis
        analysis2 = DocumentAnalysis(
            document_id="test-doc-002",
            key_dates=[date(2024, 3, 1)],
            parties_involved=["Jane Smith"],
            document_type="Legal Brief",
            summary="Another test analysis",
            key_clauses=["Another clause"],
            confidence_scores={"parties": 0.85}
        )
        
        temp_storage_service.save_analysis("test-doc-001", analysis1)
        temp_storage_service.save_analysis("test-doc-002", analysis2)
        
        # Get all analyses
        all_analyses = temp_storage_service.get_all_analyses()
        assert len(all_analyses) == 2
        assert "test-doc-001" in all_analyses
        assert "test-doc-002" in all_analyses
    
    def test_clear_all_analyses(self, temp_storage_service, sample_analysis):
        """Test clearing all analyses"""
        # Save some analyses
        temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        temp_storage_service.save_analysis("test-doc-002", sample_analysis)
        
        # Verify they exist
        assert len(temp_storage_service.get_all_analyses()) == 2
        
        # Clear all
        success = temp_storage_service.clear_all_analyses()
        assert success is True
        
        # Verify they're gone
        assert len(temp_storage_service.get_all_analyses()) == 0
        assert temp_storage_service.has_analysis("test-doc-001") is False
    
    def test_get_storage_stats(self, temp_storage_service, sample_analysis):
        """Test getting storage statistics"""
        # Initially empty
        stats = temp_storage_service.get_storage_stats()
        assert stats["total_analyses"] == 0
        assert stats["storage_available"] is True
        
        # Save analysis
        temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        
        # Check updated stats
        stats = temp_storage_service.get_storage_stats()
        assert stats["total_analyses"] == 1
        assert stats["storage_available"] is True
        assert "last_updated" in stats
        assert "storage_file_size" in stats
    
    def test_retrieve_nonexistent_analysis(self, temp_storage_service):
        """Test retrieving analysis that doesn't exist"""
        result = temp_storage_service.get_analysis("non-existent")
        assert result is None
    
    def test_storage_persistence(self, temp_storage_service, sample_analysis):
        """Test that storage persists across service instances"""
        # Save analysis
        temp_storage_service.save_analysis("test-doc-001", sample_analysis)
        
        # Create new service instance with same storage file
        new_service = AnalysisStorageService()
        new_service.storage_file = temp_storage_service.storage_file
        
        # Should be able to retrieve the analysis
        retrieved = new_service.get_analysis("test-doc-001")
        assert retrieved is not None
        assert retrieved.document_id == sample_analysis.document_id