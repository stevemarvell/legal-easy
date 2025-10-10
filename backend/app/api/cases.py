from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.case import Case, CaseStatistics
from app.models.playbook import ComprehensiveCaseAnalysis
from app.services.data_service import DataService
from app.services.playbook_service import PlaybookService

router = APIRouter(
    prefix="/cases", 
    tags=["Cases"],
    responses={
        404: {"description": "Case not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get(
    "/statistics", 
    response_model=CaseStatistics,
    summary="Get case statistics",
    description="""
    Retrieve comprehensive statistics about all cases in the system.
    
    This endpoint provides dashboard-ready metrics including:
    - Total number of cases
    - Cases by status (Active, Under Review, Resolved)
    - Recent activity count (last 30 days)
    
    **Use cases:**
    - Dashboard widgets
    - Management reporting
    - System health monitoring
    """,
    responses={
        200: {
            "description": "Case statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_cases": 6,
                        "active_cases": 3,
                        "resolved_cases": 1,
                        "under_review_cases": 2,
                        "recent_activity_count": 4
                    }
                }
            }
        }
    }
)
async def get_case_statistics():
    """Get case statistics for dashboard and reporting"""
    try:
        # Load all cases using DataService
        cases = DataService.load_cases()
        
        # Calculate statistics
        total_cases = len(cases)
        active_cases = len([c for c in cases if c.status == "Active"])
        resolved_cases = len([c for c in cases if c.status == "Resolved"])
        under_review_cases = len([c for c in cases if c.status == "Under Review"])
        
        # For recent activity, count cases created in last 30 days
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activity_count = len([
            c for c in cases 
            if c.created_date and c.created_date >= thirty_days_ago
        ])
        
        return CaseStatistics(
            total_cases=total_cases,
            active_cases=active_cases,
            resolved_cases=resolved_cases,
            under_review_cases=under_review_cases,
            recent_activity_count=recent_activity_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case statistics: {str(e)}")


@router.get(
    "/", 
    response_model=List[Case],
    summary="Get all cases",
    description="""
    Retrieve a list of all legal cases in the system.
    
    This endpoint returns all cases with their complete information including:
    - Case details (title, type, status, client)
    - Key parties involved
    - Associated document IDs
    - Case timeline information
    
    **Use cases:**
    - Case listing pages
    - Search and filter operations
    - Bulk operations
    """,
    responses={
        200: {
            "description": "List of cases retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "case-001",
                            "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
                            "case_type": "Employment Dispute",
                            "client_name": "Sarah Chen",
                            "status": "Active",
                            "created_date": "2024-01-15T09:00:00Z",
                            "summary": "Employee alleges wrongful dismissal after reporting safety violations...",
                            "key_parties": ["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"],
                            "documents": ["doc-001", "doc-002", "doc-003"],
                            "playbook_id": "employment-dispute"
                        }
                    ]
                }
            }
        }
    }
)
async def get_cases():
    """Get all legal cases in the system"""
    try:
        return DataService.load_cases()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cases: {str(e)}")


@router.get(
    "/{case_id}", 
    response_model=Case,
    summary="Get case by ID",
    description="""
    Retrieve detailed information about a specific legal case.
    
    This endpoint returns complete case information including:
    - All case metadata and details
    - List of key parties involved
    - Associated document references
    - Case status and timeline
    
    **Use cases:**
    - Case detail pages
    - Case management operations
    - Document association lookups
    """,
    responses={
        200: {
            "description": "Case retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "case-001",
                        "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
                        "case_type": "Employment Dispute",
                        "client_name": "Sarah Chen",
                        "status": "Active",
                        "created_date": "2024-01-15T09:00:00Z",
                        "summary": "Employee alleges wrongful dismissal after reporting safety violations...",
                        "key_parties": ["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"],
                        "documents": ["doc-001", "doc-002", "doc-003"],
                        "playbook_id": "employment-dispute"
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
async def get_case(
    case_id: str = Path(..., description="Unique identifier of the case to retrieve", example="case-001")
):
    """Get detailed information about a specific legal case"""
    try:
        # Load all cases and find the specific one
        cases = DataService.load_cases()
        case = next((c for c in cases if c.id == case_id), None)
        
        if case is None:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case: {str(e)}")


@router.get(
    "/{case_id}/comprehensive-analysis",
    response_model=ComprehensiveCaseAnalysis,
    summary="Get comprehensive case analysis using playbook",
    description="""
    Generate comprehensive case analysis using the appropriate playbook.
    
    This endpoint applies case type-specific playbook rules to analyze the case and provides:
    - Case strength assessment with confidence levels
    - Strategic recommendations with legal precedent references
    - Relevant legal precedents from corpus
    - Applied playbook information
    - Detailed reasoning for the assessment
    
    The analysis is generated by:
    1. Identifying the appropriate playbook for the case type
    2. Applying relevant playbook rules to case facts
    3. Calculating case strength based on rule weights
    4. Generating strategic recommendations with precedent references
    
    **Use cases:**
    - Complete case evaluation
    - Strategic planning
    - Client consultation preparation
    - Legal reasoning transparency
    """,
    responses={
        200: {
            "description": "Comprehensive analysis generated successfully",
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
                        "relevant_precedents": [],
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
async def get_comprehensive_analysis(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Generate comprehensive case analysis using appropriate playbook"""
    try:
        # Perform comprehensive analysis using PlaybookService
        analysis = PlaybookService.analyze_case_with_playbook(case_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate comprehensive analysis: {str(e)}")