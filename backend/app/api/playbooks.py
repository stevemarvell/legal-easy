from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict, Any
from app.services.playbook_service import PlaybookService
from app.services.data_service import DataService

router = APIRouter(
    prefix="/playbooks", 
    tags=["Playbooks"],
    responses={
        404: {"description": "Playbook not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    summary="Get all available playbooks",
    description="""
    Retrieve a list of all available playbooks in the system.
    
    This endpoint returns all playbooks with their complete information including:
    - Playbook metadata (ID, name, case type)
    - All playbook rules with conditions and actions
    - Decision tree structure
    - Monetary assessment ranges
    - Escalation paths
    
    **Use cases:**
    - Playbook management interfaces
    - Case type selection
    - Rule exploration and analysis
    """,
    responses={
        200: {
            "description": "List of playbooks retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "employment-dispute",
                            "case_type": "Employment Dispute",
                            "name": "Employment Law Playbook",
                            "rules": [],
                            "decision_tree": {},
                            "monetary_ranges": {},
                            "escalation_paths": []
                        }
                    ]
                }
            }
        }
    }
)
async def get_all_playbooks():
    """Get all available playbooks in the system"""
    try:
        return DataService.load_playbooks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get playbooks: {str(e)}")


@router.get(
    "/{case_type}",
    response_model=Dict[str, Any],
    summary="Get playbook by case type",
    description="""
    Retrieve the playbook for a specific case type.
    
    This endpoint returns the complete playbook information including:
    - All applicable rules with conditions, actions, and weights
    - Decision tree for case evaluation
    - Monetary assessment ranges by case strength
    - Escalation paths and procedures
    - Legal basis and evidence requirements for each rule
    
    **Use cases:**
    - Case-specific playbook display
    - Rule analysis and application
    - Legal strategy planning
    - Training and reference
    """,
    responses={
        200: {
            "description": "Playbook retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "employment-dispute",
                        "case_type": "Employment Dispute",
                        "name": "Employment Law Playbook",
                        "rules": [
                            {
                                "id": "rule-001",
                                "condition": "termination_within_protected_period",
                                "action": "investigate_victimisation_claim",
                                "weight": 0.9,
                                "description": "If dismissal occurred within 90 days of protected activity, investigate potential victimisation"
                            }
                        ],
                        "decision_tree": {},
                        "monetary_ranges": {
                            "high": {"range": [200000, 1000000]}
                        },
                        "escalation_paths": ["Internal HR complaint", "ACAS early conciliation"]
                    }
                }
            }
        },
        404: {
            "description": "Playbook not found",
            "content": {
                "application/json": {
                    "example": {"detail": "No playbook found for case type: Unknown Type"}
                }
            }
        }
    }
)
async def get_playbook(
    case_type: str = Path(..., description="Case type to get playbook for", example="Employment Dispute")
):
    """Get playbook for a specific case type"""
    try:
        playbook = PlaybookService.match_playbook(case_type)
        if playbook is None:
            raise HTTPException(status_code=404, detail=f"No playbook found for case type: {case_type}")
        return playbook
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get playbook: {str(e)}")


@router.get(
    "/match/{case_type}",
    response_model=Dict[str, Any],
    summary="Match playbook for case type",
    description="""
    Find the matching playbook for a specific case type.
    
    This endpoint returns the playbook that matches the given case type,
    or None if no matching playbook is found. This is useful for:
    - Determining if a playbook exists for a case type
    - Getting playbook metadata before full analysis
    - Case type validation
    
    **Use cases:**
    - Case type validation
    - Playbook availability checking
    - UI playbook selection
    """,
    responses={
        200: {
            "description": "Playbook match result",
            "content": {
                "application/json": {
                    "example": {
                        "id": "employment-dispute",
                        "case_type": "Employment Dispute",
                        "name": "Employment Law Playbook",
                        "description": "Comprehensive playbook for employment-related legal disputes"
                    }
                }
            }
        },
        404: {
            "description": "No matching playbook found",
            "content": {
                "application/json": {
                    "example": {"detail": "No playbook found for case type: Unknown Type"}
                }
            }
        }
    }
)
async def match_playbook(
    case_type: str = Path(..., description="Case type to match playbook for", example="Employment Dispute")
):
    """Match playbook for a specific case type"""
    try:
        playbook = PlaybookService.match_playbook(case_type)
        if playbook is None:
            raise HTTPException(status_code=404, detail=f"No playbook found for case type: {case_type}")
        return playbook
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to match playbook: {str(e)}")


@router.post(
    "/cases/{case_id}/comprehensive-analysis",
    response_model=Dict[str, Any],
    summary="Generate comprehensive case analysis using playbook",
    description="""
    Perform comprehensive case analysis using the appropriate playbook.
    
    This endpoint analyzes a case against its appropriate playbook and returns:
    - Case strength assessment with confidence levels
    - Strategic recommendations with legal precedent references
    - List of rules that were applied to the case
    - Relevant legal precedents from corpus
    - Applied playbook information
    - Detailed reasoning for the assessment
    
    This is the main endpoint for getting complete case analysis with playbook-driven insights.
    
    **Use cases:**
    - Complete case evaluation
    - Strategic planning
    - Client consultation preparation
    - Legal reasoning transparency
    """,
    responses={
        200: {
            "description": "Comprehensive analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
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
                                "priority": "High",
                                "rationale": "Moderate case strength suggests settlement may be optimal",
                                "supporting_precedents": ["Risk mitigation"]
                            }
                        ],
                        "relevant_precedents": [
                            {
                                "id": "employment_precedent_1",
                                "title": "Employment Rights Act 1996 - Unfair Dismissal",
                                "category": "statutes",
                                "relevance": "Primary legislation governing employment termination"
                            }
                        ],
                        "applied_playbook": {
                            "id": "employment-dispute",
                            "name": "Employment Law Playbook",
                            "case_type": "Employment Dispute"
                        },
                        "analysis_timestamp": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case with ID case-999 not found"}
                }
            }
        }
    }
)
async def generate_comprehensive_analysis(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Generate comprehensive case analysis using playbook"""
    try:
        # Perform comprehensive analysis using PlaybookService
        analysis = PlaybookService.analyze_case_with_playbook(case_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform comprehensive analysis: {str(e)}")