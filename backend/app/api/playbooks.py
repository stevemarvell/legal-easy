from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.playbook import Playbook, PlaybookResult
from app.services.playbook_engine import PlaybookEngine
from app.services.case_service import CaseService

router = APIRouter(
    prefix="/playbooks", 
    tags=["Playbooks"],
    responses={
        404: {"description": "Playbook not found"},
        500: {"description": "Internal server error"}
    }
)
playbook_engine = PlaybookEngine()
case_service = CaseService()


@router.get(
    "/",
    response_model=List[Playbook],
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
        return playbook_engine.get_all_playbooks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get playbooks: {str(e)}")


@router.get(
    "/{case_type}",
    response_model=Playbook,
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
        playbook = playbook_engine.get_playbook_by_case_type(case_type)
        if playbook is None:
            raise HTTPException(status_code=404, detail=f"No playbook found for case type: {case_type}")
        return playbook
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get playbook: {str(e)}")


@router.get(
    "/cases/{case_id}/applied-rules",
    response_model=PlaybookResult,
    summary="Get applied playbook rules for a case",
    description="""
    Show which playbook rules were applied to a specific case and the reasoning.
    
    This endpoint analyzes a case against its appropriate playbook and returns:
    - List of rules that were applied to the case
    - Recommendations generated from applied rules
    - Case strength assessment
    - Detailed reasoning for the assessment
    
    This is useful for understanding how the AI reached its conclusions and
    which specific legal factors influenced the case evaluation.
    
    **Use cases:**
    - Case analysis explanation
    - Legal reasoning transparency
    - Rule application debugging
    - Client consultation preparation
    """,
    responses={
        200: {
            "description": "Applied rules retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "case_id": "case-001",
                        "playbook_id": "employment-dispute",
                        "applied_rules": ["rule-001", "rule-004"],
                        "recommendations": [
                            "investigate_victimisation_claim",
                            "document_harassment_incidents"
                        ],
                        "case_strength": "Strong",
                        "reasoning": "Case shows strong prospects based on 2 applicable rules. Key factors support the client's position in this employment dispute matter."
                    }
                }
            }
        },
        404: {
            "description": "Case not found or no playbook available",
            "content": {
                "application/json": {
                    "example": {"detail": "Case with ID case-999 not found"}
                }
            }
        }
    }
)
async def get_applied_rules(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Show which playbook rules were applied to a specific case"""
    try:
        # Get the case first
        case = case_service.get_case_by_id(case_id)
        if case is None:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")
        
        # Get the appropriate playbook
        playbook = playbook_engine.get_playbook_by_case_type(case.case_type)
        if playbook is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No playbook available for case type: {case.case_type}"
            )
        
        # Apply playbook rules and return the result
        result = playbook_engine.apply_playbook_rules(case, playbook)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get applied rules: {str(e)}")