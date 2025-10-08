from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Case(BaseModel):
    """Core case data model representing a legal case in the system"""
    
    id: str = Field(..., description="Unique identifier for the case", example="case-001")
    title: str = Field(..., description="Descriptive title of the case", example="Wrongful Dismissal - Sarah Chen vs TechCorp Solutions")
    case_type: str = Field(..., description="Type of legal case", example="Employment Dispute", enum=["Employment Dispute", "Contract Breach", "Debt Claim"])
    client_name: str = Field(..., description="Name of the client", example="Sarah Chen")
    status: str = Field(..., description="Current status of the case", example="Active", enum=["Active", "Under Review", "Resolved"])
    created_date: datetime = Field(..., description="Date when the case was created", example="2024-01-15T09:00:00Z")
    summary: str = Field(..., description="Brief summary of the case", example="Employee alleges wrongful dismissal after reporting safety violations...")
    key_parties: List[str] = Field(..., description="List of key parties involved in the case", example=["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"])
    documents: List[str] = Field(..., description="List of document IDs associated with this case", example=["doc-001", "doc-002", "doc-003"])
    playbook_id: str = Field(..., description="ID of the playbook used for this case type", example="employment-dispute")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "case-001",
                "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
                "case_type": "Employment Dispute",
                "client_name": "Sarah Chen",
                "status": "Active",
                "created_date": "2024-01-15T09:00:00Z",
                "summary": "Employee alleges wrongful dismissal after reporting safety violations. Claims retaliation and seeks reinstatement plus damages.",
                "key_parties": [
                    "Sarah Chen (Claimant)",
                    "TechCorp Solutions Ltd. (Respondent)",
                    "Marcus Rodriguez (HR Director)",
                    "Jennifer Walsh (Direct Supervisor)"
                ],
                "documents": ["doc-001", "doc-002", "doc-003"],
                "playbook_id": "employment-dispute"
            }
        }


class CaseStatistics(BaseModel):
    """Dashboard statistics model providing overview of case metrics"""
    
    total_cases: int = Field(..., description="Total number of cases in the system", example=6)
    active_cases: int = Field(..., description="Number of cases with 'Active' status", example=3)
    resolved_cases: int = Field(..., description="Number of cases with 'Resolved' status", example=1)
    under_review_cases: int = Field(..., description="Number of cases with 'Under Review' status", example=2)
    recent_activity_count: int = Field(..., description="Number of cases with activity in the last 30 days", example=4)

    class Config:
        json_schema_extra = {
            "example": {
                "total_cases": 6,
                "active_cases": 3,
                "resolved_cases": 1,
                "under_review_cases": 2,
                "recent_activity_count": 4
            }
        }