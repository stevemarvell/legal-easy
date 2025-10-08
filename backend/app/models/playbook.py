from typing import List, Dict, Tuple, Optional, Any
from pydantic import BaseModel


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