import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def sample_random_response():
    """Sample response for random endpoint."""
    return {"value": 42}

@pytest.fixture
def health_response():
    """Sample response for health endpoint."""
    return {"message": "Random Number API. Use /random"}

# Comprehensive test fixtures for all API endpoints

@pytest.fixture
def sample_case():
    """Sample case data for testing"""
    return {
        "id": "case-001",
        "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
        "case_type": "Employment Dispute",
        "client_name": "Sarah Chen",
        "status": "Active",
        "created_date": "2024-01-15T09:00:00Z",
        "summary": "Employee alleges wrongful dismissal after reporting safety violations",
        "key_parties": ["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"],
        "documents": ["doc-001", "doc-002", "doc-003"],
        "playbook_id": "employment-dispute"
    }

@pytest.fixture
def sample_cases():
    """Sample cases list for testing"""
    return [
        {
            "id": "case-001",
            "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
            "case_type": "Employment Dispute",
            "status": "Active"
        },
        {
            "id": "case-002", 
            "title": "Contract Breach - ABC Corp vs XYZ Ltd",
            "case_type": "Contract Dispute",
            "status": "Under Review"
        },
        {
            "id": "case-003",
            "title": "IP Infringement - Tech Innovations vs StartupCo",
            "case_type": "Intellectual Property",
            "status": "Resolved"
        }
    ]

@pytest.fixture
def sample_document():
    """Sample document data for testing"""
    return {
        "id": "doc-001",
        "case_id": "case-001",
        "name": "Employment Contract - Sarah Chen",
        "type": "Contract",
        "size": 245760,
        "upload_date": "2024-01-15T09:30:00Z",
        "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
        "analysis_completed": True
    }

@pytest.fixture
def sample_documents():
    """Sample documents list for testing"""
    return [
        {
            "id": "doc-001",
            "case_id": "case-001",
            "name": "Employment Contract - Sarah Chen",
            "type": "Contract",
            "analysis_completed": True
        },
        {
            "id": "doc-002",
            "case_id": "case-001", 
            "name": "Termination Letter",
            "type": "Letter",
            "analysis_completed": False
        }
    ]

@pytest.fixture
def sample_document_analysis():
    """Sample document analysis data for testing"""
    return {
        "document_id": "doc-001",
        "key_dates": ["2022-03-15", "2024-01-12"],
        "parties_involved": ["Sarah Chen", "TechCorp Solutions Inc."],
        "document_type": "Employment Contract",
        "summary": "At-will employment agreement for Senior Safety Engineer position",
        "key_clauses": ["At-will employment clause", "Safety reporting obligations"],
        "confidence_scores": {"parties": 0.95, "dates": 0.98, "summary": 0.87},
        "overall_confidence": 0.93,
        "uncertainty_flags": []
    }

@pytest.fixture
def sample_corpus_item():
    """Sample corpus item for testing"""
    return {
        "id": "rc-001",
        "name": "Employment Contract Template",
        "filename": "rc-001_employment_template.txt",
        "category": "contracts",
        "document_type": "Contract Template",
        "research_areas": ["Employment Law"],
        "description": "Standard UK employment contract template with key clauses",
        "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
    }

@pytest.fixture
def sample_corpus_items():
    """Sample corpus items list for testing"""
    return [
        {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "category": "contracts",
            "research_areas": ["Employment Law"]
        },
        {
            "id": "rc-002",
            "name": "NDA Template", 
            "category": "contracts",
            "research_areas": ["Contract Law"]
        },
        {
            "id": "rc-003",
            "name": "Termination Clauses",
            "category": "clauses",
            "research_areas": ["Employment Law"]
        }
    ]

@pytest.fixture
def sample_playbook():
    """Sample playbook data for testing"""
    return {
        "id": "employment-dispute",
        "case_type": "Employment Dispute",
        "name": "Employment Law Playbook",
        "rules": [
            {
                "id": "rule-001",
                "condition": "termination_within_protected_period",
                "action": "investigate_victimisation_claim",
                "weight": 0.9,
                "description": "If dismissal occurred within 90 days of protected activity"
            }
        ],
        "decision_tree": {},
        "monetary_ranges": {
            "high": {"range": [200000, 1000000]}
        },
        "escalation_paths": ["Internal HR complaint", "ACAS early conciliation"]
    }

@pytest.fixture
def sample_comprehensive_analysis():
    """Sample comprehensive case analysis for testing"""
    return {
        "case_id": "case-001",
        "case_strength_assessment": {
            "overall_strength": "Moderate",
            "confidence_level": 0.75,
            "key_strengths": ["Strong legal position"],
            "potential_weaknesses": ["Limited evidence"],
            "supporting_evidence": ["Timeline of protected activity"]
        },
        "strategic_recommendations": [
            {
                "id": "negotiate_settlement",
                "title": "Negotiate Favorable Settlement",
                "description": "Reasonable prospects support settlement negotiations",
                "priority": "High"
            }
        ],
        "relevant_precedents": [],
        "applied_playbook": {
            "id": "employment-dispute",
            "name": "Employment Law Playbook"
        },
        "analysis_timestamp": "2024-01-15T10:30:00Z"
    }

@pytest.fixture
def sample_documentation_categories():
    """Sample documentation categories for testing"""
    return {
        "api": {
            "name": "API Documentation",
            "description": "Complete API reference and examples",
            "document_ids": ["api-overview", "api-examples"]
        },
        "architecture": {
            "name": "System Architecture",
            "description": "System design documentation",
            "document_ids": ["arch-overview"]
        }
    }

@pytest.fixture
def mock_data_service():
    """Mock DataService for testing"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_ai_service():
    """Mock AIService for testing"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_playbook_service():
    """Mock PlaybookService for testing"""
    mock = MagicMock()
    return mock