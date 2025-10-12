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
    description: Optional[str] = Field(None, description="Detailed description of the case with comprehensive background information", example="Sarah Chen commenced employment with TechCorp Solutions Ltd. on 15 March 2022...")
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
                "description": "Sarah Chen commenced employment with TechCorp Solutions Ltd. on 15 March 2022 as a Senior Safety Engineer under a comprehensive employment agreement...",
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

# Case Details Analysis Models

class PartyDetail(BaseModel):
    """Details about a party involved in the case"""
    name: str = Field(..., description="Name of the party")
    role: str = Field(..., description="Role of the party in the case")
    mentioned_in_description: bool = Field(..., description="Whether the party is mentioned in the case description")


class LegalAnalysis(BaseModel):
    """Legal analysis of the case"""
    primary_legal_issues: List[str] = Field(..., description="Primary legal issues identified in the case")
    applicable_legislation: List[str] = Field(..., description="Applicable legislation and legal frameworks")
    complexity_score: int = Field(..., description="Legal complexity score from 1-10", ge=1, le=10)


class PartiesAnalysis(BaseModel):
    """Analysis of parties involved in the case"""
    total_parties: int = Field(..., description="Total number of parties involved")
    parties_detail: List[PartyDetail] = Field(..., description="Detailed information about each party")
    complexity_indicator: str = Field(..., description="Complexity indicator based on number of parties", enum=["Low", "Medium", "High"])


class TimelineAnalysis(BaseModel):
    """Timeline analysis of the case"""
    dates_identified: List[str] = Field(..., description="Key dates identified in the case")
    key_events: List[str] = Field(..., description="Key events in chronological order")
    timeline_complexity: int = Field(..., description="Timeline complexity score from 1-10", ge=1, le=10)


class RiskAssessment(BaseModel):
    """Risk assessment for the case"""
    risk_factors: List[str] = Field(..., description="Identified risk factors")
    overall_risk_level: str = Field(..., description="Overall risk level", enum=["Low", "Medium", "High"])
    risk_score: int = Field(..., description="Risk score from 1-10", ge=1, le=10)


class EvidenceAnalysis(BaseModel):
    """Evidence analysis for the case"""
    evidence_types: List[str] = Field(..., description="Types of evidence available")
    evidence_strength: str = Field(..., description="Overall evidence strength", enum=["Limited", "Moderate", "Strong"])
    evidence_score: int = Field(..., description="Evidence strength score from 1-10", ge=1, le=10)


class LegalPrecedents(BaseModel):
    """Legal precedents relevant to the case"""
    relevant_precedents: List[str] = Field(..., description="Relevant legal precedents")
    precedent_strength: str = Field(..., description="Strength of precedent support", enum=["Low", "Medium", "High"])


class StrategicRecommendations(BaseModel):
    """Strategic recommendations for the case"""
    strategic_recommendations: List[str] = Field(..., description="Strategic recommendations for case handling")
    priority_actions: List[str] = Field(..., description="Priority actions to take")


class CaseStrengthAnalysis(BaseModel):
    """Case strength analysis"""
    strength_factors: List[str] = Field(..., description="Factors that strengthen the case")
    weakness_factors: List[str] = Field(..., description="Factors that weaken the case")
    overall_strength: str = Field(..., description="Overall case strength", enum=["Weak", "Moderate", "Strong"])
    strength_score: int = Field(..., description="Case strength score from 1-10", ge=1, le=10)


class CaseDetailsAnalysis(BaseModel):
    """Comprehensive case details analysis model"""
    case_id: str = Field(..., description="ID of the analyzed case")
    case_type: str = Field(..., description="Type of the case")
    analysis_timestamp: datetime = Field(..., description="When the analysis was performed")
    legal_analysis: LegalAnalysis = Field(..., description="Legal analysis of the case")
    parties_analysis: PartiesAnalysis = Field(..., description="Analysis of parties involved")
    timeline_analysis: TimelineAnalysis = Field(..., description="Timeline analysis")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment")
    evidence_analysis: EvidenceAnalysis = Field(..., description="Evidence analysis")
    legal_precedents: LegalPrecedents = Field(..., description="Legal precedents analysis")
    strategic_recommendations: StrategicRecommendations = Field(..., description="Strategic recommendations")
    case_strength: CaseStrengthAnalysis = Field(..., description="Case strength analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "case_id": "case-001",
                "case_type": "Employment Dispute",
                "analysis_timestamp": "2024-01-15T10:30:00Z",
                "legal_analysis": {
                    "primary_legal_issues": ["Wrongful dismissal", "Retaliation", "Safety violations"],
                    "applicable_legislation": ["Employment Standards Act", "Occupational Health and Safety Act"],
                    "complexity_score": 7
                },
                "parties_analysis": {
                    "total_parties": 4,
                    "parties_detail": [
                        {"name": "Sarah Chen", "role": "Claimant", "mentioned_in_description": True},
                        {"name": "TechCorp Solutions Ltd.", "role": "Respondent", "mentioned_in_description": True}
                    ],
                    "complexity_indicator": "Medium"
                },
                "timeline_analysis": {
                    "dates_identified": ["2022-03-15", "2024-01-10"],
                    "key_events": ["Employment commenced", "Dismissal occurred"],
                    "timeline_complexity": 5
                },
                "risk_assessment": {
                    "risk_factors": ["Retaliation claim", "Safety violation reporting"],
                    "overall_risk_level": "Medium",
                    "risk_score": 6
                },
                "evidence_analysis": {
                    "evidence_types": ["Employment contract", "Email correspondence", "Safety reports"],
                    "evidence_strength": "Moderate",
                    "evidence_score": 6
                },
                "legal_precedents": {
                    "relevant_precedents": ["Similar wrongful dismissal cases", "Retaliation precedents"],
                    "precedent_strength": "Medium"
                },
                "strategic_recommendations": {
                    "strategic_recommendations": ["Gather additional evidence", "Review safety documentation"],
                    "priority_actions": ["Document timeline", "Collect witness statements"]
                },
                "case_strength": {
                    "strength_factors": ["Clear timeline", "Safety violation documentation"],
                    "weakness_factors": ["Limited witness testimony"],
                    "overall_strength": "Moderate",
                    "strength_score": 6
                }
            }
        }