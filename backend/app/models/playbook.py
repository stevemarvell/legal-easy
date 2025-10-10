from typing import List, Dict, Tuple, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class PlaybookRule(BaseModel):
    """Individual playbook rule"""
    id: str
    condition: str
    action: str
    weight: float
    description: str


class MonetaryRange(BaseModel):
    """Monetary assessment range with description and factors"""
    range: List[int]
    description: str
    factors: List[str]


class Playbook(BaseModel):
    """Case type-specific playbook"""
    id: str
    case_type: str
    name: str
    rules: List[PlaybookRule]
    decision_tree: Dict[str, Any]
    monetary_ranges: Dict[str, MonetaryRange]
    escalation_paths: List[str]


class PlaybookResult(BaseModel):
    """Result of applying playbook to a case"""
    case_id: str
    playbook_id: str
    applied_rules: List[str]
    recommendations: List[str]
    case_strength: str
    reasoning: str


class CaseAssessment(BaseModel):
    """Complete case assessment using playbook"""
    case_id: str
    playbook_used: str
    case_strength: str  # "Strong", "Moderate", "Weak"
    key_issues: List[str]
    recommended_actions: List[str]
    monetary_assessment: Optional[Tuple[int, int]]
    applied_rules: List[str]
    reasoning: str


class CaseStrengthAssessment(BaseModel):
    """Case strength assessment with confidence levels"""
    overall_strength: str  # Strong, Moderate, Weak
    confidence_level: float
    key_strengths: List[str]
    potential_weaknesses: List[str]
    supporting_evidence: List[str]


class StrategicRecommendation(BaseModel):
    """Strategic recommendation with precedent references"""
    id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    rationale: str
    supporting_precedents: List[str]


class CorpusItem(BaseModel):
    """Legal corpus item reference"""
    id: str
    title: str
    category: str  # contracts, clauses, precedents, statutes
    content: Optional[str] = None
    legal_concepts: Optional[List[str]] = None
    related_items: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ComprehensiveCaseAnalysis(BaseModel):
    """Comprehensive case analysis using playbooks"""
    case_id: str
    case_strength_assessment: CaseStrengthAssessment
    strategic_recommendations: List[StrategicRecommendation]
    relevant_precedents: List[CorpusItem]
    applied_playbook: Optional[Playbook]
    analysis_timestamp: datetime