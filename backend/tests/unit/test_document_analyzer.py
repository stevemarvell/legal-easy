import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, date
from app.services.document_analyzer import DocumentAnalyzer
from app.models.document import Document, DocumentAnalysis, KeyInformation


class TestDocumentAnalyzer:
    """Test the DocumentAnalyzer class"""
    
    @pytest.fixture
    def document_analyzer(self):
        """Create a DocumentAnalyzer instance for testing"""
        return DocumentAnalyzer()
    
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
            content_preview="EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen. Position: Senior Safety Engineer...",
            analysis_completed=True,
            full_content_path="backend/app/data/case_documents/case-001/doc-001_employment_contract_sarah_chen.txt"
        )
    
    @pytest.fixture
    def sample_document_content(self):
        """Sample document content for testing"""
        return """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement is entered into on 15 March 2022, between TechCorp Solutions Ltd. and Sarah Chen.
        
        POSITION AND DUTIES
        Employee is hereby employed as Senior Safety Engineer with annual salary of £75,000.
        
        NOTICE PROVISION
        In the event of termination by either party, thirty (30) days written notice shall be provided.
        
        CONFIDENTIALITY
        Employee agrees to maintain strict confidentiality of all proprietary information.
        
        SAFETY REPORTING OBLIGATIONS
        Employee has a duty to report safety violations without fear of retaliation.
        """
    
    def test_init(self, document_analyzer):
        """Test DocumentAnalyzer initialization"""
        assert document_analyzer.legal_keywords is not None
        assert 'contract_terms' in document_analyzer.legal_keywords
        assert 'employment' in document_analyzer.legal_keywords
        assert 'legal_concepts' in document_analyzer.legal_keywords
        assert len(document_analyzer.date_patterns) > 0
        assert len(document_analyzer.amount_patterns) > 0
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_document_content_with_full_path(self, mock_exists, mock_file, document_analyzer, sample_document, sample_document_content):
        """Test loading document content when full_content_path is available"""
        mock_file.return_value.read.return_value = sample_document_content
        
        content = document_analyzer._load_document_content(sample_document)
        
        assert content == sample_document_content
        mock_file.assert_called_once_with(sample_document.full_content_path, 'r', encoding='utf-8')
    
    @patch("os.path.exists", return_value=False)
    def test_load_document_content_fallback_to_preview(self, mock_exists, document_analyzer, sample_document):
        """Test fallback to content preview when file doesn't exist"""
        content = document_analyzer._load_document_content(sample_document)
        
        assert content == sample_document.content_preview
    
    def test_extract_dates(self, document_analyzer):
        """Test date extraction from text"""
        text = """
        This agreement was signed on 15 March 2022 and becomes effective on 2022-04-01.
        The termination date is 12/31/2024. Another date: January 15, 2023.
        """
        
        dates = document_analyzer._extract_dates(text)
        
        assert len(dates) >= 3
        assert date(2022, 3, 15) in dates
        assert date(2022, 4, 1) in dates
        assert date(2024, 12, 31) in dates
    
    def test_extract_parties(self, document_analyzer):
        """Test party extraction from text"""
        text = """
        This agreement is between TechCorp Solutions Ltd. and Sarah Chen.
        Mr. John Smith represents the company. Dr. Maria Gonzalez is the consultant.
        Contact: sarah.chen@techcorp.co.uk
        """
        
        parties = document_analyzer._extract_parties(text)
        
        assert len(parties) > 0
        assert any("TechCorp Solutions Ltd" in party for party in parties)
        assert any("Sarah Chen" in party for party in parties)
    
    def test_extract_amounts(self, document_analyzer):
        """Test financial amount extraction from text"""
        text = """
        The annual salary is £75,000. Additional bonus of $10,000 may be awarded.
        Total contract value: 50,000 dollars.
        """
        
        amounts = document_analyzer._extract_amounts(text)
        
        assert len(amounts) >= 2
        assert any("£75,000" in amount for amount in amounts)
        assert any("$10,000" in amount for amount in amounts)
    
    def test_extract_legal_concepts(self, document_analyzer):
        """Test legal concept extraction from text"""
        text = """
        This employment contract includes liability clauses and termination provisions.
        The agreement covers breach of contract and negligence issues.
        """
        
        concepts = document_analyzer._extract_legal_concepts(text)
        
        assert len(concepts) > 0
        assert "employment" in concepts
        assert "contract" in concepts
        assert "liability" in concepts
        assert "termination" in concepts
    
    def test_classify_document_type_employment_contract(self, document_analyzer):
        """Test document type classification for employment contracts"""
        text = "EMPLOYMENT AGREEMENT between Company and Employee with salary and benefits"
        
        doc_type = document_analyzer._classify_document_type(text, "Contract")
        
        assert doc_type == "Employment Contract"
    
    def test_classify_document_type_email(self, document_analyzer):
        """Test document type classification for emails"""
        text = "From: sender@company.com To: recipient@company.com Subject: Meeting"
        
        doc_type = document_analyzer._classify_document_type(text, "Email")
        
        assert doc_type == "Email Communication"
    
    def test_classify_document_type_fallback(self, document_analyzer):
        """Test document type classification fallback to original type"""
        text = "Some generic document content without specific indicators"
        
        doc_type = document_analyzer._classify_document_type(text, "Legal Brief")
        
        assert doc_type == "Legal Brief"
    
    def test_generate_summary_employment_contract(self, document_analyzer):
        """Test summary generation for employment contracts"""
        text = """
        EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen.
        Position: Senior Safety Engineer. Annual salary: £75,000.
        """
        
        summary = document_analyzer._generate_summary(text, "Employment Contract")
        
        assert "Employment agreement" in summary
        assert len(summary) > 20
    
    def test_extract_key_clauses_employment(self, document_analyzer):
        """Test key clause extraction for employment documents"""
        text = """
        EMPLOYMENT AGREEMENT with 30-day notice provision.
        Annual salary of £75,000 with confidentiality obligations.
        Non-compete clause applies for 12 months.
        """
        
        clauses = document_analyzer._extract_key_clauses(text, "Employment Contract")
        
        assert len(clauses) > 0
        assert any("notice" in clause.lower() for clause in clauses)
        assert any("compensation" in clause.lower() or "salary" in clause.lower() for clause in clauses)
    
    def test_calculate_confidence_scores(self, document_analyzer, sample_document):
        """Test confidence score calculation"""
        analysis_data = {
            'parties': ["Company Inc", "John Doe"],
            'dates': [date(2022, 3, 15)],
            'key_clauses': ["Governing clause", "Relationship terms"],
            'document_type': 'Employment Contract',
            'risk_assessment': {'overall_risk': 'low', 'issues': []},
            'compliance_analysis': {'status': 'compliant'},
            'semantic_analysis': {'intent': 'establishment', 'complexity': 'medium'}
        }
        
        scores = document_analyzer._calculate_confidence_scores(sample_document, analysis_data)
        
        assert 'parties' in scores
        assert 'dates' in scores
        assert 'contract_terms' in scores
        assert 'key_clauses' in scores
        assert 'legal_analysis' in scores
        assert all(0.0 <= score <= 1.0 for score in scores.values())
    
    @patch.object(DocumentAnalyzer, '_load_document_content')
    def test_analyze_document(self, mock_load_content, document_analyzer, sample_document, sample_document_content):
        """Test complete document analysis"""
        mock_load_content.return_value = sample_document_content
        
        analysis = document_analyzer.analyze_document(sample_document)
        
        assert isinstance(analysis, DocumentAnalysis)
        assert analysis.document_id == sample_document.id
        assert len(analysis.key_dates) >= 0
        assert len(analysis.parties_involved) >= 0
        assert analysis.document_type is not None
        assert analysis.summary is not None
        assert len(analysis.key_clauses) >= 0
        assert isinstance(analysis.confidence_scores, dict)
        # Enhanced analysis calls _load_document_content multiple times
        assert mock_load_content.call_count >= 1
        mock_load_content.assert_called_with(sample_document)
    
    def test_extract_key_information(self, document_analyzer):
        """Test key information extraction from raw text"""
        text = """
        Agreement dated 15 March 2022 between TechCorp Solutions Ltd. and Sarah Chen.
        Annual salary: £75,000. This employment contract includes liability provisions.
        """
        
        key_info = document_analyzer.extract_key_information(text)
        
        assert isinstance(key_info, KeyInformation)
        assert len(key_info.dates) >= 1
        assert len(key_info.parties) >= 1
        assert len(key_info.amounts) >= 1
        assert len(key_info.legal_concepts) >= 1
        assert 0.0 <= key_info.confidence <= 1.0
    
    def test_calculate_extraction_confidence(self, document_analyzer):
        """Test extraction confidence calculation"""
        text = "Long document with multiple parties, dates, and legal concepts"
        dates = [date(2022, 1, 1)]
        parties = ["Company Inc"]
        amounts = ["$50,000"]
        concepts = ["contract", "liability"]
        
        confidence = document_analyzer._calculate_extraction_confidence(text, dates, parties, amounts, concepts)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be reasonably confident with all extractions
    
    def test_date_extraction_edge_cases(self, document_analyzer):
        """Test date extraction with various formats and edge cases"""
        text = """
        Invalid dates: 32/13/2022, 2022-13-45
        Valid dates: 01/15/2022, 2022-12-31, 15 January 2023, March 1, 2024
        """
        
        dates = document_analyzer._extract_dates(text)
        
        # Should extract valid dates and ignore invalid ones
        assert len(dates) >= 3
        assert all(isinstance(d, date) for d in dates)
    
    def test_party_extraction_company_patterns(self, document_analyzer):
        """Test party extraction for various company name patterns"""
        text = """
        Companies: TechCorp Solutions Ltd., DataFlow Inc., CloudTech Systems LLC,
        Premier Consulting Limited, StartupXYZ Corporation, MegaCorp Industries Co.
        """
        
        parties = document_analyzer._extract_parties(text)
        
        assert len(parties) > 0
        assert any("TechCorp Solutions" in party for party in parties)
        assert any("DataFlow" in party for party in parties)
    
    def test_amount_extraction_currency_patterns(self, document_analyzer):
        """Test amount extraction for various currency formats"""
        text = """
        Amounts: £75,000, $50,000.00, €25,000, 10,000 dollars, 5,000 pounds
        """
        
        amounts = document_analyzer._extract_amounts(text)
        
        assert len(amounts) >= 3
        assert any("£75,000" in amount for amount in amounts)
        assert any("$50,000" in amount for amount in amounts)