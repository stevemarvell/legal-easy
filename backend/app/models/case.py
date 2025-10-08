from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Case(BaseModel):
    """Core case data model"""
    id: str
    title: str
    case_type: str  # "Employment Dispute", "Contract Breach", "Debt Claim"
    client_name: str
    status: str  # "Active", "Under Review", "Resolved"
    created_date: datetime
    summary: str
    key_parties: List[str]
    documents: List[str]  # Document IDs
    playbook_id: str


class CaseStatistics(BaseModel):
    """Dashboard statistics model"""
    total_cases: int
    active_cases: int
    resolved_cases: int
    under_review_cases: int
    recent_activity_count: int