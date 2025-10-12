from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.case import Case, CaseStatistics
from app.services.data_service import DataService

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
    description="Retrieve comprehensive statistics about all cases in the system."
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
    description="Retrieve a list of all legal cases in the system."
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
    description="Retrieve detailed information about a specific legal case."
)
async def get_case(
    case_id: str = Path(..., description="Unique identifier of the case to retrieve", example="case-001")
):
    """Get detailed information about a specific legal case"""
    try:
        # Load all cases and find the specific one
        cases = DataService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        
        if case is None:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case: {str(e)}")


@router.post(
    "/comprehensive-analysis",
    summary="Perform comprehensive case analysis",
    description="""
    Perform comprehensive analysis integrating case overview, documents, and research.
    
    TODO: Implement AI-powered comprehensive analysis
    """,
    responses={
        200: {"description": "Comprehensive analysis completed successfully"},
        500: {"description": "Analysis failed"}
    }
)
async def comprehensive_case_analysis():
    """Perform comprehensive analysis of all cases"""
    try:
        # TODO: Implement comprehensive case analysis with AI
        return {
            "success": True,
            "message": "Comprehensive case analysis not yet implemented",
            "total_cases": 0,
            "analyzed_cases": 0,
            "failed_cases": 0,
            "average_confidence": 0.0,
            "processing_time_seconds": 0.0,
            "analysis_types": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform comprehensive analysis: {str(e)}")


@router.get(
    "/{case_id}/research-list",
    summary="Get research list for case",
    description="""
    Get generated research list for a case.
    
    TODO: Implement AI-powered research list generation
    """,
    responses={
        200: {"description": "Research list retrieved successfully"},
        404: {"description": "Research list not found"}
    }
)
async def get_case_research_list(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get research list for a case"""
    try:
        # TODO: Implement research list retrieval
        raise HTTPException(status_code=404, detail=f"Research list for case {case_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get research list: {str(e)}")


@router.post(
    "/{case_id}/generate-research-list",
    summary="Generate research list for case",
    description="""
    Generate research list based on case analysis.
    
    TODO: Implement AI-powered research list generation
    """,
    responses={
        200: {"description": "Research list generated successfully"},
        404: {"description": "Case not found"}
    }
)
async def generate_case_research_list(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Generate research list for a case"""
    try:
        # TODO: Implement research list generation with AI
        from app.services.ai_service import AIService
        
        # Load case data
        cases = DataService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        if not case:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        
        # Load case documents
        documents = DataService.load_case_documents(case_id)
        
        # Generate research list
        research_list = AIService.generate_research_list(case_id, case, documents)
        
        return research_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate research list: {str(e)}")