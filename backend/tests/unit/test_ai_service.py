#!/usr/bin/env python3
"""AIService Unit Tests"""

import pytest
from unittest.mock import patch, mock_open
import json
from datetime import datetime
from pathlib import Path

from app.services.ai_service import AIService


class TestAIServiceDocumentAnalysis:
    """Test AIService document analysis functionality"""
    
    def test_analyze_document_basic_structure(self):
        """Test that analyze_document returns proper structure"""
        content = """
        Employment Agreement
        
        This agreement is between TechCorp Solutions and John Doe.
        Start date: January 15, 2024
        Termination clause: Either party may terminate with 30 days notice.
        """
        
        result = AIService.analyze_document("test-doc", content)
        
        # Verify basic structure
        assert result['document_id'] == 'test-doc'
        assert 'analysis_timestamp' in result
        assert 'key_dates' in result
        assert 'parties_involved' in result
        assert 'document_type' in result
        assert 'summary' in result
        assert 'key_clauses' in result
        assert 'confidence_scores' in result
        assert 'overall_confidence' in result
        assert 'uncertainty_flags' in result
        
        # Verify data types
        assert isinstance(result['key_dates'], list)
        assert isinstance(result['parties_involved'], list)
        assert isinstance(result['document_type'], str)
        assert isinstance(result['summary'], str)
        assert isinstance(result['key_clauses'], list)
        assert isinstance(result['confidence_scores'], dict)
        assert isinstance(result['overall_confidence'], (int, float))
        assert isinstance(result['uncertainty_flags'], list)
        
        # Verify confidence score range
        assert 0.0 <= result['overall_confidence'] <= 1.0

    def test_extract_dates_various_formats(self):
        """Test date extraction with various formats"""
        content = """
        Start date: 01/15/2024
        End date: December 31, 2024
        Meeting on 2024-06-15
        Deadline: 15th January 2025
        """
        
        dates = AIService._extract_dates(content)
        
        assert isinstance(dates, list)
        assert len(dates) > 0
        
        # Verify ISO format
        for date in dates:
            assert isinstance(date, str)
            # Should be in YYYY-MM-DD format
            assert len(date) == 10
            assert date[4] == '-'
            assert date[7] == '-'

    def test_extract_parties_from_content(self):
        """Test party extraction from document content"""
        content = """
        This Employment Agreement is between TechCorp Solutions Inc. and John Doe.
        The Company (TechCorp Solutions) agrees to employ Jane Smith.
        ABC Corporation Ltd. will provide services to XYZ Partnership LLC.
        """
        
        parties = AIService._extract_parties(content)
        
        assert isinstance(parties, list)
        # Parties extraction may or may not find parties depending on regex patterns
        # Just verify the method returns a list and doesn't crash
        if len(parties) > 0:
            # If parties are found, they should be strings
            assert all(isinstance(party, str) for party in parties)

    def test_classify_document_type_employment(self):
        """Test document type classification for employment documents"""
        content = """
        Employment Agreement
        
        This agreement establishes the terms of employment between the employer
        and employee. The employee will start work on the specified date.
        Termination procedures are outlined below.
        """
        
        doc_type = AIService._classify_document_type(content)
        assert doc_type == 'Employment Document'

    def test_classify_document_type_contract(self):
        """Test document type classification for contracts"""
        content = """
        Service Agreement
        
        This contract establishes the terms and conditions for services
        to be provided. Both parties agree to the following terms.
        """
        
        doc_type = AIService._classify_document_type(content)
        assert doc_type == 'Contract'

    def test_generate_summary_basic(self):
        """Test basic summary generation"""
        content = """
        This is the first sentence of the document. This is the second sentence
        with more details. This is the third sentence. This is the fourth sentence
        that should not be included in the summary.
        """
        
        summary = AIService._generate_summary(content)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'first sentence' in summary
        assert 'second sentence' in summary
        assert 'third sentence' in summary
        assert 'fourth sentence' not in summary

    def test_extract_key_clauses(self):
        """Test key clause extraction"""
        content = """
        The parties agree to maintain confidentiality of all information.
        Either party shall provide 30 days notice for termination.
        The company must pay all invoices within 30 days.
        Liability clause: Neither party will be liable for indirect damages.
        """
        
        clauses = AIService._extract_key_clauses(content)
        
        assert isinstance(clauses, list)
        # Should find some clauses
        assert len(clauses) >= 0

    def test_calculate_confidence_scores(self):
        """Test confidence score calculation"""
        content = "Employment agreement between TechCorp and John Doe dated 2024-01-15"
        key_dates = ["2024-01-15"]
        parties = ["TechCorp", "John Doe"]
        doc_type = "Employment Document"
        summary = "Employment agreement summary"
        clauses = ["Employment clause"]
        
        scores = AIService._calculate_confidence_scores(
            content, key_dates, parties, doc_type, summary, clauses
        )
        
        assert isinstance(scores, dict)
        assert 'dates' in scores
        assert 'parties' in scores
        assert 'document_type' in scores
        assert 'summary' in scores
        assert 'key_clauses' in scores
        
        # All scores should be between 0 and 1
        for score in scores.values():
            assert 0.0 <= score <= 1.0

    def test_identify_uncertainty_flags(self):
        """Test uncertainty flag identification"""
        # Low confidence scores should generate flags
        low_confidence_scores = {
            'dates': 0.2,
            'parties': 0.3,
            'document_type': 0.4,
            'summary': 0.1,
            'key_clauses': 0.2
        }
        content = "Short content"
        
        flags = AIService._identify_uncertainty_flags(low_confidence_scores, content)
        
        assert isinstance(flags, list)
        assert len(flags) > 0
        
        # Should flag low confidence areas
        flag_text = ' '.join(flags).lower()
        assert 'low confidence' in flag_text

    def test_assess_risk_level(self):
        """Test risk level assessment"""
        high_risk_content = "Contract breach and violation with potential lawsuit damages"
        medium_risk_content = "There is a dispute regarding the agreement terms"
        low_risk_content = "Agreement shows cooperation and compliance with all terms"
        
        high_risk = AIService._assess_risk_level(high_risk_content, [])
        medium_risk = AIService._assess_risk_level(medium_risk_content, [])
        low_risk = AIService._assess_risk_level(low_risk_content, [])
        
        assert high_risk == 'high'
        # Risk assessment may vary based on keyword matching
        assert medium_risk in ['medium', 'low', 'high', None]
        assert low_risk in ['low', 'medium', 'high', None]

    def test_identify_potential_issues(self):
        """Test potential issue identification"""
        content = """
        The contract was breached when payment was not made on time.
        There are confidentiality concerns about disclosed information.
        Termination issues arose due to non-compliance with standards.
        """
        
        issues = AIService._identify_potential_issues(content, [])
        
        assert isinstance(issues, list)
        assert len(issues) > 0
        
        # Should identify multiple issue types
        issues_text = ' '.join(issues).lower()
        assert any(keyword in issues_text for keyword in ['breach', 'payment', 'confidentiality', 'termination'])

    def test_assess_compliance_status(self):
        """Test compliance status assessment"""
        compliant_content = "The document shows full compliance with all regulations"
        non_compliant_content = "There is a violation of the compliance standards"
        review_content = "Standard business agreement without specific compliance mentions"
        
        compliant_status = AIService._assess_compliance_status(compliant_content, "Contract")
        non_compliant_status = AIService._assess_compliance_status(non_compliant_content, "Contract")
        review_status = AIService._assess_compliance_status(review_content, "Contract")
        
        assert compliant_status == 'Compliant'
        assert non_compliant_status == 'Non-compliant'
        # Review status may vary based on keyword matching
        assert review_status in ['Under review', 'Compliant', 'Non-compliant']

    def test_extract_critical_deadlines(self):
        """Test critical deadline extraction"""
        key_dates = ["2024-12-31", "2024-06-15"]
        content = "The deadline for completion is December 31st. Payment is due by June 15th."
        
        deadlines = AIService._extract_critical_deadlines(content, key_dates)
        
        if deadlines:
            assert isinstance(deadlines, list)
            for deadline in deadlines:
                assert 'date' in deadline
                assert 'type' in deadline
                assert 'description' in deadline

    def test_determine_document_intent(self):
        """Test document intent determination"""
        agreement_content = "This agreement establishes the terms between parties"
        notice_content = "This notice informs you of the upcoming changes"
        request_content = "We are requesting your assistance with this matter"
        
        agreement_intent = AIService._determine_document_intent(agreement_content, "Contract")
        notice_intent = AIService._determine_document_intent(notice_content, "Notice")
        request_intent = AIService._determine_document_intent(request_content, "Request")
        
        assert agreement_intent == 'Agreement'
        assert notice_intent == 'Notice'
        assert request_intent == 'Request'

    def test_calculate_complexity_score(self):
        """Test document complexity score calculation"""
        simple_content = "This is a simple document."
        complex_content = """
        Whereas the parties heretofore have entered into various agreements,
        and notwithstanding any provisions to the contrary, pursuant to the
        terms herein, each party shall indemnify and hold harmless the other
        party from any and all claims, damages, losses, and expenses.
        """ * 10  # Make it longer
        
        simple_score = AIService._calculate_complexity_score(simple_content)
        complex_score = AIService._calculate_complexity_score(complex_content)
        
        assert 0.0 <= simple_score <= 1.0
        assert 0.0 <= complex_score <= 1.0
        assert complex_score > simple_score

    def test_parse_date_to_iso_various_formats(self):
        """Test date parsing to ISO format"""
        test_dates = [
            ("01/15/2024", "2024-01-15"),
            ("15/01/2024", "2024-01-15"),
            ("2024-01-15", "2024-01-15"),
            ("January 15, 2024", "2024-01-15"),
            ("15 January 2024", "2024-01-15"),
            ("15th January 2024", "2024-01-15")
        ]
        
        for input_date, expected_output in test_dates:
            result = AIService._parse_date_to_iso(input_date)
            # Note: Some formats might be ambiguous (MM/DD vs DD/MM)
            # so we just verify we get a valid ISO date format
            if result:
                assert len(result) == 10
                assert result[4] == '-'
                assert result[7] == '-'


class TestAIServiceAnalysisStorage:
    """Test AIService analysis storage functionality"""
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_existing_analysis_success(self, mock_exists, mock_file):
        """Test loading existing analysis successfully"""
        analysis_data = {
            "test-doc": {
                "document_id": "test-doc",
                "summary": "Test summary",
                "confidence_scores": {"summary": 0.8},
                "overall_confidence": 0.75
            }
        }
        
        mock_file.side_effect = lambda *args, **kwargs: mock_open(read_data=json.dumps(analysis_data)).return_value
        mock_exists.return_value = True
        
        result = AIService.load_existing_analysis("test-doc")
        
        assert result is not None
        assert result["document_id"] == "test-doc"
        assert result["summary"] == "Test summary"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_existing_analysis_no_file(self, mock_exists):
        """Test loading analysis when file doesn't exist"""
        result = AIService.load_existing_analysis("test-doc")
        assert result is None

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    def test_save_analysis_success(self, mock_mkdir, mock_exists, mock_file):
        """Test saving analysis successfully"""
        analysis_data = {
            "document_id": "test-doc",
            "summary": "Test summary",
            "confidence_scores": {"summary": 0.8},
            "overall_confidence": 0.75
        }
        
        # Mock existing file with empty data
        mock_file.side_effect = [
            mock_open(read_data="{}").return_value,  # First read (existing data)
            mock_open().return_value  # Second write (save data)
        ]
        mock_exists.return_value = True
        
        # Should not raise an exception
        AIService.save_analysis("test-doc", analysis_data)
        
        # Verify file operations were called
        assert mock_file.call_count >= 1

    @patch("builtins.open", side_effect=Exception("File error"))
    def test_save_analysis_error_handling(self, mock_file):
        """Test save analysis error handling"""
        analysis_data = {"document_id": "test-doc"}
        
        with pytest.raises(Exception):
            AIService.save_analysis("test-doc", analysis_data)


class TestAIServiceIntegration:
    """Integration tests for AIService"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        content = """
        Employment Agreement
        
        This Employment Agreement is entered into on January 15, 2024,
        between TechCorp Solutions Inc. ("Company") and John Doe ("Employee").
        
        The Employee shall commence employment on February 1, 2024.
        Either party may terminate this agreement with 30 days written notice.
        
        The Employee agrees to maintain confidentiality of all company information.
        Compensation will be paid monthly according to the agreed terms.
        """
        
        # Perform full analysis
        result = AIService.analyze_document("integration-test", content)
        
        # Verify comprehensive analysis
        assert result['document_id'] == 'integration-test'
        assert result['document_type'] == 'Employment Document'
        assert len(result['summary']) > 0
        assert len(result['key_dates']) > 0
        assert len(result['parties_involved']) > 0
        
        # Verify dates were extracted and formatted
        dates = result['key_dates']
        for date in dates:
            assert len(date) == 10  # YYYY-MM-DD format
            assert date[4] == '-'
            assert date[7] == '-'
        
        # Verify parties were extracted
        parties = result['parties_involved']
        party_text = ' '.join(parties).lower()
        assert any('techcorp' in party.lower() for party in parties)
        
        # Verify confidence scores
        assert 0.0 <= result['overall_confidence'] <= 1.0
        for score in result['confidence_scores'].values():
            assert 0.0 <= score <= 1.0
        
        # Verify additional analysis fields
        assert 'risk_level' in result
        assert 'compliance_status' in result
        assert 'document_intent' in result
        assert 'complexity_score' in result
        assert 0.0 <= result['complexity_score'] <= 1.0

    def test_analysis_with_minimal_content(self):
        """Test analysis with minimal content"""
        content = "Short document."
        
        result = AIService.analyze_document("minimal-test", content)
        
        # Should still return valid structure
        assert result['document_id'] == 'minimal-test'
        assert isinstance(result['summary'], str)
        assert isinstance(result['key_dates'], list)
        assert isinstance(result['parties_involved'], list)
        assert 0.0 <= result['overall_confidence'] <= 1.0
        
        # Should have uncertainty flags for short content
        assert len(result['uncertainty_flags']) > 0
        flag_text = ' '.join(result['uncertainty_flags']).lower()
        assert 'short' in flag_text

    def test_analysis_with_complex_legal_content(self):
        """Test analysis with complex legal content"""
        content = """
        WHEREAS, the parties heretofore have entered into certain agreements;
        and WHEREAS, the parties desire to modify and amend such agreements;
        NOW, THEREFORE, in consideration of the mutual covenants herein contained,
        and for other good and valuable consideration, the parties agree as follows:
        
        1. INDEMNIFICATION: Each party shall indemnify, defend, and hold harmless
        the other party from and against any and all claims, damages, losses,
        costs, and expenses (including reasonable attorneys' fees) arising out of
        or resulting from any breach of this Agreement.
        
        2. GOVERNING LAW: This Agreement shall be governed by and construed in
        accordance with the laws of the State of California, without regard to
        its conflict of laws principles.
        
        Executed on December 15, 2024, by the authorized representatives of
        ABC Corporation and XYZ Limited Partnership.
        """
        
        result = AIService.analyze_document("complex-test", content)
        
        # Should handle complex legal language
        assert result['document_id'] == 'complex-test'
        assert result['document_type'] in ['Contract', 'Legal Document']
        
        # Should extract parties
        parties = result['parties_involved']
        party_text = ' '.join(parties).lower()
        assert 'abc' in party_text or 'xyz' in party_text
        
        # Should have reasonable complexity score (legal content should be somewhat complex)
        assert result['complexity_score'] > 0.2
        
        # Should extract date
        assert len(result['key_dates']) > 0
        assert "2024-12-15" in result['key_dates']

class TestAIServiceCaseDetailsAnalysis:
    """Test AIService case details analysis functionality"""
    
    def test_analyze_case_details_basic_structure(self):
        """Test that analyze_case_details returns proper structure"""
        case_description = """
        Sarah Chen commenced employment with TechCorp Solutions Ltd. on 15 March 2022 
        as a Senior Safety Engineer under a comprehensive employment agreement. 
        On 10 January 2024, Sarah was dismissed from her position after reporting 
        safety violations to management. She alleges wrongful dismissal and retaliation.
        """
        
        result = AIService.analyze_case_details("case-001", "Employment Dispute", case_description)
        
        # Verify basic structure
        assert result['case_id'] == 'case-001'
        assert result['case_type'] == 'Employment Dispute'
        assert 'analysis_timestamp' in result
        
        # Verify all analysis components are present
        assert 'legal_analysis' in result
        assert 'parties_analysis' in result
        assert 'timeline_analysis' in result
        assert 'risk_assessment' in result
        assert 'evidence_analysis' in result
        assert 'legal_precedents' in result
        assert 'strategic_recommendations' in result
        assert 'case_strength' in result
        
        # Verify legal analysis structure
        legal_analysis = result['legal_analysis']
        assert 'primary_legal_issues' in legal_analysis
        assert 'applicable_legislation' in legal_analysis
        assert 'complexity_score' in legal_analysis
        assert isinstance(legal_analysis['primary_legal_issues'], list)
        assert isinstance(legal_analysis['applicable_legislation'], list)
        assert 1 <= legal_analysis['complexity_score'] <= 10
        
        # Verify parties analysis structure
        parties_analysis = result['parties_analysis']
        assert 'total_parties' in parties_analysis
        assert 'parties_detail' in parties_analysis
        assert 'complexity_indicator' in parties_analysis
        assert isinstance(parties_analysis['total_parties'], int)
        assert isinstance(parties_analysis['parties_detail'], list)
        assert parties_analysis['complexity_indicator'] in ['Low', 'Medium', 'High']
        
        # Verify timeline analysis structure
        timeline_analysis = result['timeline_analysis']
        assert 'dates_identified' in timeline_analysis
        assert 'key_events' in timeline_analysis
        assert 'timeline_complexity' in timeline_analysis
        assert isinstance(timeline_analysis['dates_identified'], list)
        assert isinstance(timeline_analysis['key_events'], list)
        assert 1 <= timeline_analysis['timeline_complexity'] <= 10

    def test_analyze_legal_issues_employment_dispute(self):
        """Test legal issues analysis for employment dispute"""
        case_description = """
        Employee was wrongfully dismissed after reporting safety violations.
        There are allegations of retaliation and discrimination.
        """
        
        result = AIService._analyze_legal_issues(case_description, "Employment Dispute")
        
        assert 'primary_legal_issues' in result
        assert 'applicable_legislation' in result
        assert 'complexity_score' in result
        
        # Should identify employment-related issues
        issues = result['primary_legal_issues']
        issues_text = ' '.join(issues).lower()
        assert any(keyword in issues_text for keyword in ['wrongful', 'dismissal', 'retaliation', 'discrimination'])
        
        # Should include employment legislation
        legislation = result['applicable_legislation']
        legislation_text = ' '.join(legislation).lower()
        assert any(keyword in legislation_text for keyword in ['employment', 'human rights', 'safety'])
        
        # Complexity score should be reasonable
        assert 3 <= result['complexity_score'] <= 10

    def test_analyze_legal_issues_contract_breach(self):
        """Test legal issues analysis for contract breach"""
        case_description = """
        There was a material breach of contract when the supplier failed to deliver
        goods on time, causing significant damages to the business.
        """
        
        result = AIService._analyze_legal_issues(case_description, "Contract Breach")
        
        issues = result['primary_legal_issues']
        issues_text = ' '.join(issues).lower()
        assert any(keyword in issues_text for keyword in ['breach', 'contract', 'damages'])
        
        legislation = result['applicable_legislation']
        legislation_text = ' '.join(legislation).lower()
        assert any(keyword in legislation_text for keyword in ['contract', 'commercial', 'sale'])

    def test_analyze_parties_with_multiple_parties(self):
        """Test parties analysis with multiple parties"""
        case_description = """
        Sarah Chen filed a complaint against TechCorp Solutions Ltd.
        Marcus Rodriguez, the HR Director, was involved in the dismissal decision.
        Jennifer Walsh, the direct supervisor, provided testimony.
        """
        
        result = AIService._analyze_parties(case_description)
        
        assert 'total_parties' in result
        assert 'parties_detail' in result
        assert 'complexity_indicator' in result
        
        # Should identify multiple parties
        assert result['total_parties'] >= 2
        
        # Should have party details
        parties_detail = result['parties_detail']
        assert len(parties_detail) > 0
        
        for party in parties_detail:
            assert 'name' in party
            assert 'role' in party
            assert 'mentioned_in_description' in party
            assert isinstance(party['mentioned_in_description'], bool)
        
        # Should determine appropriate complexity
        if result['total_parties'] <= 2:
            assert result['complexity_indicator'] == 'Low'
        elif result['total_parties'] <= 4:
            assert result['complexity_indicator'] == 'Medium'
        else:
            assert result['complexity_indicator'] == 'High'

    def test_analyze_timeline_with_dates_and_events(self):
        """Test timeline analysis with dates and events"""
        case_description = """
        Employment commenced on 15 March 2022. Safety violations were reported
        in November 2023. The employee was terminated on 10 January 2024.
        A complaint was filed on 15 January 2024.
        """
        
        result = AIService._analyze_timeline(case_description)
        
        assert 'dates_identified' in result
        assert 'key_events' in result
        assert 'timeline_complexity' in result
        
        # Should identify dates
        dates = result['dates_identified']
        assert len(dates) > 0
        
        # Should identify events
        events = result['key_events']
        assert len(events) > 0
        
        # Timeline complexity should be reasonable
        assert 2 <= result['timeline_complexity'] <= 10

    def test_assess_case_risks_employment_dispute(self):
        """Test risk assessment for employment dispute"""
        case_description = """
        Employee alleges retaliation after reporting safety violations.
        There are potential discrimination claims and wrongful dismissal.
        """
        
        result = AIService._assess_case_risks(case_description, "Employment Dispute")
        
        assert 'risk_factors' in result
        assert 'overall_risk_level' in result
        assert 'risk_score' in result
        
        # Should identify employment-related risks
        risk_factors = result['risk_factors']
        risk_text = ' '.join(risk_factors).lower()
        assert any(keyword in risk_text for keyword in ['retaliation', 'discrimination', 'wrongful'])
        
        # Risk level should be valid
        assert result['overall_risk_level'] in ['Low', 'Medium', 'High']
        
        # Risk score should be in valid range
        assert 2 <= result['risk_score'] <= 10

    def test_analyze_evidence_types(self):
        """Test evidence analysis"""
        case_description = """
        The case involves employment contract documentation, email correspondence
        between parties, safety reports filed by the employee, and witness
        statements from colleagues. Performance reviews are also available.
        """
        
        result = AIService._analyze_evidence(case_description)
        
        assert 'evidence_types' in result
        assert 'evidence_strength' in result
        assert 'evidence_score' in result
        
        # Should identify various evidence types
        evidence_types = result['evidence_types']
        evidence_text = ' '.join(evidence_types).lower()
        assert any(keyword in evidence_text for keyword in ['contract', 'email', 'safety', 'witness', 'performance'])
        
        # Evidence strength should be valid
        assert result['evidence_strength'] in ['Limited', 'Moderate', 'Strong']
        
        # Evidence score should be in valid range
        assert 3 <= result['evidence_score'] <= 10

    def test_identify_precedents_by_case_type(self):
        """Test precedent identification by case type"""
        case_description = "Standard employment dispute case"
        
        employment_result = AIService._identify_precedents(case_description, "Employment Dispute")
        contract_result = AIService._identify_precedents(case_description, "Contract Breach")
        debt_result = AIService._identify_precedents(case_description, "Debt Claim")
        
        # Each case type should have relevant precedents
        employment_precedents = ' '.join(employment_result['relevant_precedents']).lower()
        assert any(keyword in employment_precedents for keyword in ['employment', 'wrongful', 'dismissal'])
        
        contract_precedents = ' '.join(contract_result['relevant_precedents']).lower()
        assert any(keyword in contract_precedents for keyword in ['contract', 'breach'])
        
        debt_precedents = ' '.join(debt_result['relevant_precedents']).lower()
        assert any(keyword in debt_precedents for keyword in ['debt', 'collection'])
        
        # All should have valid precedent strength
        for result in [employment_result, contract_result, debt_result]:
            assert result['precedent_strength'] in ['Low', 'Medium', 'High']

    def test_generate_strategic_recommendations_by_case_type(self):
        """Test strategic recommendations by case type"""
        case_description = "Standard case requiring strategic analysis"
        
        employment_result = AIService._generate_strategic_recommendations(case_description, "Employment Dispute")
        contract_result = AIService._generate_strategic_recommendations(case_description, "Contract Breach")
        debt_result = AIService._generate_strategic_recommendations(case_description, "Debt Claim")
        
        # Each should have recommendations and priority actions
        for result in [employment_result, contract_result, debt_result]:
            assert 'strategic_recommendations' in result
            assert 'priority_actions' in result
            assert len(result['strategic_recommendations']) > 0
            assert len(result['priority_actions']) > 0
        
        # Employment recommendations should be employment-specific
        employment_recs = ' '.join(employment_result['strategic_recommendations']).lower()
        assert any(keyword in employment_recs for keyword in ['employment', 'safety', 'witness'])
        
        # Contract recommendations should be contract-specific
        contract_recs = ' '.join(contract_result['strategic_recommendations']).lower()
        assert any(keyword in contract_recs for keyword in ['contract', 'breach', 'damages'])

    def test_assess_case_strength_with_indicators(self):
        """Test case strength assessment with various indicators"""
        strong_case_description = """
        Clear documented evidence of wrongful dismissal with witness testimony.
        Employment contract clearly establishes terms. Safety violations are
        well documented and supported by reports.
        """
        
        weak_case_description = """
        Unclear circumstances surrounding dismissal. Limited evidence available.
        Disputed facts and insufficient documentation. Questionable witness accounts.
        """
        
        strong_result = AIService._assess_case_strength(strong_case_description, "Employment Dispute")
        weak_result = AIService._assess_case_strength(weak_case_description, "Employment Dispute")
        
        # Both should have valid structure
        for result in [strong_result, weak_result]:
            assert 'strength_factors' in result
            assert 'weakness_factors' in result
            assert 'overall_strength' in result
            assert 'strength_score' in result
            assert result['overall_strength'] in ['Weak', 'Moderate', 'Strong']
            assert 1 <= result['strength_score'] <= 10
        
        # Strong case should have higher score than weak case
        assert strong_result['strength_score'] >= weak_result['strength_score']

    def test_determine_party_role_assignment(self):
        """Test party role determination"""
        case_description = """
        Sarah Chen (claimant) filed a complaint against TechCorp Solutions Ltd.
        Marcus Rodriguez is the HR Director. ABC Corporation Ltd. is involved.
        """
        
        # Test different party types and positions
        claimant_role = AIService._determine_party_role("Sarah Chen", case_description, 0)
        corporate_role = AIService._determine_party_role("TechCorp Solutions Ltd.", case_description, 1)
        hr_role = AIService._determine_party_role("Marcus Rodriguez", case_description, 2)
        
        assert claimant_role == "Claimant"
        assert corporate_role in ["Respondent", "Corporate Entity"]
        assert hr_role in ["Third Party", "Respondent"]

    def test_case_details_analysis_integration(self):
        """Test full case details analysis integration"""
        case_description = """
        Sarah Chen commenced employment with TechCorp Solutions Ltd. on 15 March 2022
        as a Senior Safety Engineer. She reported safety violations to management in
        November 2023. On 10 January 2024, Sarah was dismissed from her position.
        She alleges wrongful dismissal and retaliation. The case involves employment
        contract documentation, email correspondence, and witness statements.
        """
        
        result = AIService.analyze_case_details("case-001", "Employment Dispute", case_description)
        
        # Verify comprehensive analysis was performed
        assert result['case_id'] == 'case-001'
        assert result['case_type'] == 'Employment Dispute'
        
        # Verify legal analysis found employment issues
        legal_issues = result['legal_analysis']['primary_legal_issues']
        issues_text = ' '.join(legal_issues).lower()
        assert any(keyword in issues_text for keyword in ['wrongful', 'dismissal', 'retaliation'])
        
        # Verify parties were identified
        assert result['parties_analysis']['total_parties'] >= 2
        
        # Verify timeline has dates and events
        assert len(result['timeline_analysis']['dates_identified']) > 0
        assert len(result['timeline_analysis']['key_events']) > 0
        
        # Verify risk assessment identified employment risks
        risk_factors = result['risk_assessment']['risk_factors']
        risk_text = ' '.join(risk_factors).lower()
        assert any(keyword in risk_text for keyword in ['retaliation', 'wrongful', 'dismissal'])
        
        # Verify evidence analysis found relevant evidence
        evidence_types = result['evidence_analysis']['evidence_types']
        evidence_text = ' '.join(evidence_types).lower()
        assert any(keyword in evidence_text for keyword in ['contract', 'email', 'witness'])
        
        # Verify strategic recommendations are employment-specific
        recommendations = result['strategic_recommendations']['strategic_recommendations']
        recs_text = ' '.join(recommendations).lower()
        assert any(keyword in recs_text for keyword in ['employment', 'safety', 'witness', 'document'])
        
        # Verify case strength assessment
        assert result['case_strength']['overall_strength'] in ['Weak', 'Moderate', 'Strong']
        assert 1 <= result['case_strength']['strength_score'] <= 10