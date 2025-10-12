from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional, Dict, Any
from app.models.case import Case, CaseStatistics
from app.models.ai_analysis import (
    AIAnalysisResponse, 
    AIAnalysisGetResponse, 
    AIConversationsResponse, 
    ErrorResponse
)
from app.services.cases_service import CasesService
from app.services.documents_service import DocumentsService
from app.services.ai_analysis_service import AIAnalysisService

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
        # Load all cases using CasesService
        cases = CasesService.load_cases()
        
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
        return CasesService.load_cases()
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
        cases = CasesService.load_cases()
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
        200: {"description": "Cases list retrieved successfully"},
        404: {"description": "Cases list not found"}
    }
)
async def get_case_research_list(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get research list for a case"""
    try:
        # TODO: Implement research list retrieval
        raise HTTPException(status_code=404, detail=f"Cases list for case {case_id} not found")
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
        200: {"description": "Cases list generated successfully"},
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
        cases = CasesService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        if not case:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        
        # Load case documents
        documents = DocumentsService.load_case_documents(case_id)
        
        # TODO: Implement AI research list generation
        research_list = {"message": "AI research list generation not implemented"}
        
        return research_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate research list: {str(e)}")


@router.post(
    "/{case_id}/ai-analysis",
    response_model=AIAnalysisResponse,
    summary="Trigger AI analysis for case",
    description="""
    Trigger AI-powered analysis of case documents using Claude API.
    Extracts structured information including claim details, timeline, and key facts.
    
    This endpoint will:
    - Analyze all documents associated with the case
    - Extract key facts, dates, and legal issues
    - Generate structured analysis results
    - Log the conversation for audit purposes
    """,
    responses={
        200: {"model": AIAnalysisResponse, "description": "AI analysis completed successfully"},
        404: {"model": ErrorResponse, "description": "Case not found"},
        422: {"model": ErrorResponse, "description": "Analysis failed due to validation errors"},
        500: {"model": ErrorResponse, "description": "Internal server error during analysis"}
    }
)
async def trigger_ai_analysis(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Trigger AI analysis for a specific case"""
    try:
        # Verify case exists
        cases = CasesService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        if not case:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        
        # Trigger AI analysis
        ai_service = AIAnalysisService()
        analysis_result = ai_service.analyze_case(case_id)
        
        return AIAnalysisResponse(
            success=True,
            message="AI analysis completed successfully",
            case_id=case_id,
            analysis=analysis_result
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Analysis validation error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform AI analysis: {str(e)}")


@router.get(
    "/{case_id}/ai-analysis",
    response_model=AIAnalysisGetResponse,
    summary="Get AI analysis results for case",
    description="""
    Retrieve existing AI analysis results for a case.
    Returns structured analysis data including claim details, timeline, and key facts.
    
    This endpoint returns:
    - Previously generated analysis results
    - Confidence scores and metadata
    - Extracted key facts and legal issues
    - Analysis timestamp and type information
    """,
    responses={
        200: {"model": AIAnalysisGetResponse, "description": "AI analysis data retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Case or analysis not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_ai_analysis(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get existing AI analysis results for a case"""
    try:
        # Verify case exists
        cases = CasesService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        if not case:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        
        # Get analysis results
        ai_service = AIAnalysisService()
        analysis_result = ai_service.get_case_analysis(case_id)
        
        if analysis_result is None:
            raise HTTPException(status_code=404, detail=f"No AI analysis found for case {case_id}")
        
        return AIAnalysisGetResponse(
            success=True,
            case_id=case_id,
            analysis=analysis_result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve AI analysis: {str(e)}")


@router.get(
    "/{case_id}/ai-conversations",
    response_model=AIConversationsResponse,
    summary="Get AI conversation log for case",
    description="""
    Retrieve the conversation log of all AI interactions for a case.
    Includes timestamps, prompts, responses, and metadata for audit trail.
    
    This endpoint provides:
    - Complete audit trail of AI interactions
    - Timestamps and conversation IDs
    - Full prompts and responses
    - Processing metadata and performance metrics
    - Token usage and API version information
    """,
    responses={
        200: {"model": AIConversationsResponse, "description": "Conversation log retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Case not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_ai_conversations(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get AI conversation log for a case"""
    try:
        # Verify case exists
        cases = CasesService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        if not case:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        
        # Get conversation log
        ai_service = AIAnalysisService()
        conversations = ai_service.get_conversation_log(case_id)
        
        return AIConversationsResponse(
            success=True,
            case_id=case_id,
            conversations=conversations,
            total_conversations=len(conversations)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve conversation log: {str(e)}")