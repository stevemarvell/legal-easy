import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_case_data():
    """Sample case data for testing"""
    return {
        "id": "case_001",
        "title": "Employment Dispute - Smith vs ABC Corp",
        "case_type": "Employment Dispute",
        "summary": "Employee termination within protected period with age discrimination concerns",
        "client_name": "John Smith",
        "key_parties": ["John Smith", "ABC Corporation Ltd"],
        "status": "Active",
        "created_date": "2024-01-15"
    }

@pytest.fixture
def sample_document_data():
    """Sample document data for testing"""
    return {
        "id": "doc_001",
        "case_id": "case_001",
        "name": "Employment Agreement",
        "type": "contract",
        "content_preview": "This Employment Agreement is between John Smith and ABC Corporation...",
        "full_content_path": "cases/case_documents/employment_agreement.txt",
        "upload_date": "2024-01-15"
    }

@pytest.fixture
def sample_playbook_data():
    """Sample playbook data for testing"""
    return {
        "id": "employment_playbook",
        "name": "Employment Dispute Playbook",
        "case_type": "Employment Dispute",
        "description": "Playbook for handling employment disputes",
        "rules": [
            {
                "id": "protected_termination",
                "condition": "termination_within_protected_period",
                "weight": 0.9,
                "action": "Investigate protected activity and retaliation claims",
                "description": "Strong case for retaliation if termination occurred within protected period",
                "evidence_required": ["Protected activity documentation", "Termination timeline"]
            },
            {
                "id": "age_discrimination",
                "condition": "age_over_40_and_replaced_by_younger",
                "weight": 0.8,
                "action": "Gather age discrimination evidence",
                "description": "Potential age discrimination case",
                "evidence_required": ["Employee age documentation", "Replacement employee information"]
            }
        ]
    }

@pytest.fixture
def sample_corpus_data():
    """Sample corpus data for testing"""
    return {
        "categories": {
            "employment": {
                "name": "Employment Law",
                "document_ids": ["emp_001", "emp_002"]
            },
            "contracts": {
                "name": "Contract Law", 
                "document_ids": ["con_001", "con_002"]
            }
        },
        "documents": {
            "emp_001": {
                "name": "Employment Rights Act 1996",
                "category": "employment",
                "description": "Primary employment legislation",
                "research_areas": ["employment", "termination", "discrimination"],
                "filename": "employment_rights_act.txt"
            },
            "con_001": {
                "name": "Contract Formation Principles",
                "category": "contracts",
                "description": "Basic contract law principles",
                "research_areas": ["contracts", "formation", "consideration"],
                "filename": "contract_formation.txt"
            }
        },
        "research_areas": ["employment", "contracts", "termination", "discrimination", "formation", "consideration"]
    }