import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, date
from app.services.ai_analysis_service import AIAnalysisService
from app.services.document_analyzer import DocumentAnalyzer
from app.models.document import Document, DocumentAnalysis, KeyInformation


class TestAIAnalysisService:
    """Test the AIAnalysisService class"""
    
    @pytest.fixture
    def ai_analysis_service(self):
        """Create an AIAnalysisService instance for testing"""
        return AIAnalysisService()
    
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing"""
        return Document(
            id="doc-001",
            case_id="case-001",
            name="Employment Contract - Sarah Chen",
            type="Contract",
            size=245760,
            upload_date=datetime(2024, 1, 15, 9, 30, 0),
            content_preview="EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
            analysis_completed=True,
            full_content_path="backend/app/data/case_documents/case-001/doc-001_employment_contract_sarah_chen.txt"
        )
    
    @pytest.fixture
    def sample_document_analysis(self):
        """Create a sample document analysis for testing"""
        return DocumentAnalysis(
            document_id="doc-001",
            key_dates=[date(2022, 3, 15), date(2024, 1, 12)],
            parties_involved=["Sarah Chen", "TechCorp Solutions Ltd."],
            document_type="Employment Contract",
            summary="Employment agreement for Senior Safety Engineer position...",
            key_clauses=["Notice period requirements", "Compensation provisions"],
            confidence_scores={"parties": 0.95, "dates": 0.98, "contract_terms": 0.92}
        )
    
    @pytest.fixture
    def sample_key_information(self):
        """Create sample key information for testing"""
        return KeyInformation(
            dates=[date(2022, 3, 15)],
            parties=["Sarah Chen", "TechCorp Solutions Ltd."],
            amounts=["£75,000"],
            legal_concepts=["employment", "contract", "termination"],
            confidence=0.92
        )
    
    def test_init(self, ai_analysis_service):
        """Test AIAnalysisService initialization"""
        assert ai_analysis_service.document_analyzer is not None
        assert isinstance(ai_analysis_service.document_analyzer, DocumentAnalyzer)
    
    @patch.object(DocumentAnalyzer, 'analyze_document')
    def test_analyze_document(self, mock_analyze, ai_analysis_service, sample_document, sample_document_analysis):
        """Test document analysis delegation to DocumentAnalyzer"""
        mock_analyze.return_value = sample_document_analysis
        
        result = ai_analysis_service.analyze_document(sample_document)
        
        assert result == sample_document_analysis
        assert isinstance(result, DocumentAnalysis)
        assert result.document_id == sample_document.id
        mock_analyze.assert_called_once_with(sample_document)
    
    @patch.object(DocumentAnalyzer, 'extract_key_information')
    def test_extract_key_information(self, mock_extract, ai_analysis_service, sample_key_information):
        """Test key information extraction delegation to DocumentAnalyzer"""
        test_text = "Sample legal document text with parties and dates"
        mock_extract.return_value = sample_key_information
        
        result = ai_analysis_service.extract_key_information(test_text)
        
        assert result == sample_key_information
        assert isinstance(result, KeyInformation)
        assert len(result.parties) > 0
        assert len(result.dates) > 0
        mock_extract.assert_called_once_with(test_text)
    
    def test_generate_case_assessment_not_implemented(self, ai_analysis_service):
        """Test that case assessment generation is not yet implemented"""
        # This method should be implemented in a later task
        result = ai_analysis_service.generate_case_assessment(None)
        assert result is None
    
    @patch.object(DocumentAnalyzer, 'analyze_document')
    def test_analyze_document_error_handling(self, mock_analyze, ai_analysis_service, sample_document):
        """Test error handling in document analysis"""
        mock_analyze.side_effect = Exception("Analysis failed")
        
        with pytest.raises(Exception, match="Analysis failed"):
            ai_analysis_service.analyze_document(sample_document)
    
    @patch.object(DocumentAnalyzer, 'extract_key_information')
    def test_extract_key_information_error_handling(self, mock_extract, ai_analysis_service):
        """Test error handling in key information extraction"""
        mock_extract.side_effect = Exception("Extraction failed")
        
        with pytest.raises(Exception, match="Extraction failed"):
            ai_analysis_service.extract_key_information("test text")
    
    def test_service_integration(self, ai_analysis_service):
        """Test that the service properly integrates with DocumentAnalyzer"""
        # Verify that the service has a properly initialized DocumentAnalyzer
        assert hasattr(ai_analysis_service, 'document_analyzer')
        assert hasattr(ai_analysis_service.document_analyzer, 'legal_keywords')
        assert hasattr(ai_analysis_service.document_analyzer, 'date_patterns')
        assert hasattr(ai_analysis_service.document_analyzer, 'amount_patterns')