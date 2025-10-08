from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.case import Case, CaseStatistics
from app.services.case_service import CaseService

router = APIRouter(
    prefix="/cases", 
    tags=["Cases"],
    responses={
        404: {"description": "Case not found"},
        500: {"description": "Internal server error"}
    }
)
case_service = CaseService()


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
        return case_service.get_case_statistics()
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
        return case_service.get_all_cases()
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
        case = case_service.get_case_by_id(case_id)
        if case is None:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case: {str(e)}")