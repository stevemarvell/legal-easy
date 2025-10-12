from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.case import Case, CaseStatistics, CaseDetailsAnalysis
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
        case = next((c for c in cases if c.get('id') == case_id), None)
        
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


@router.get(
    "/{case_id}/integrated-analysis",
    summary="Get integrated case analysis linking documents, research, and playbooks",
    description="""
    Get comprehensive integrated analysis of a case that combines:
    - Document analysis from all case documents
    - Relevant research corpus items and precedents
    - Applicable playbook strategies and recommendations
    - Strategic recommendations and risk assessment
    - Overall case strength assessment
    
    This endpoint provides a holistic view by linking together all information sources.
    """,
    responses={
        200: {
            "description": "Integrated case analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "case_id": "case-001",
                        "case_info": {
                            "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
                            "case_type": "Employment Dispute",
                            "status": "Active"
                        },
                        "document_analysis": {
                            "summary": {
                                "total_documents": 3,
                                "key_dates": ["2022-03-15", "2023-12-10"],
                                "parties_involved": ["Sarah Chen", "TechCorp Solutions"],
                                "themes": ["employment", "termination", "safety"]
                            }
                        },
                        "research_analysis": {
                            "total_found": 15,
                            "top_relevant": [
                                {
                                    "name": "Employment Termination Precedents",
                                    "relevance_score": 0.9
                                }
                            ]
                        },
                        "playbook_analysis": {
                            "playbook_name": "Employment Law Playbook",
                            "decision_path": {
                                "result": "Strong case with high likelihood of success"
                            },
                            "monetary_assessment": {
                                "range": [50000, 200000],
                                "description": "Moderate to high damages expected"
                            }
                        },
                        "strategic_recommendations": {
                            "recommendations": [
                                {
                                    "category": "Strategic Action",
                                    "priority": "High",
                                    "recommendation": "File formal complaint"
                                }
                            ],
                            "strength_assessment": {
                                "overall": "Strong"
                            }
                        },
                        "case_assessment": {
                            "overall_score": 0.85,
                            "assessment_level": "Strong",
                            "confidence": "High"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case not found"}
                }
            }
        },
        500: {
            "description": "Analysis failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to perform integrated case analysis"}
                }
            }
        }
    }
)
async def get_integrated_case_analysis(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Get integrated analysis linking case documents, research, and playbooks"""
    try:
        from app.services.case_analysis_service import CaseAnalysisService
        
        analysis = CaseAnalysisService.analyze_case_comprehensive(case_id)
        
        if "error" in analysis:
            if "not found" in analysis["error"].lower():
                raise HTTPException(status_code=404, detail=analysis["error"])
            else:
                raise HTTPException(status_code=500, detail=analysis["error"])
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform integrated case analysis: {str(e)}")


@router.get(
    "/{case_id}/strategic-recommendations",
    summary="Get strategic recommendations for a case",
    description="""
    Get strategic recommendations for a case based on integrated analysis of:
    - Case documents and their analysis
    - Relevant legal research and precedents
    - Applicable playbook strategies
    
    Returns prioritized recommendations with next steps and risk factors.
    """,
    responses={
        200: {
            "description": "Strategic recommendations generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "case_id": "case-001",
                        "recommendations": [
                            {
                                "category": "Strategic Action",
                                "priority": "High",
                                "recommendation": "File formal complaint with Employment Tribunal",
                                "basis": "Strong evidence of victimisation following safety report"
                            },
                            {
                                "category": "Evidence Gathering",
                                "priority": "High",
                                "recommendation": "Collect witness statements from colleagues",
                                "basis": "Corroboration needed for hostile work environment claim"
                            }
                        ],
                        "next_steps": [
                            "File ACAS early conciliation",
                            "Gather additional witness evidence",
                            "Document timeline of events"
                        ],
                        "risk_factors": [
                            "Employer may claim performance-based dismissal",
                            "Limited documentation of safety concerns"
                        ],
                        "strength_assessment": {
                            "overall": "Strong",
                            "strengths": [
                                "Clear timeline established",
                                "Supporting legal precedents available"
                            ],
                            "weaknesses": [
                                "Some gaps in documentation"
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def get_strategic_recommendations(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get strategic recommendations for a case"""
    try:
        from app.services.case_analysis_service import CaseAnalysisService
        
        analysis = CaseAnalysisService.analyze_case_comprehensive(case_id)
        
        if "error" in analysis:
            if "not found" in analysis["error"].lower():
                raise HTTPException(status_code=404, detail=analysis["error"])
            else:
                raise HTTPException(status_code=500, detail=analysis["error"])
        
        # Extract just the strategic recommendations
        strategic_recs = analysis.get("strategic_recommendations", {})
        
        return {
            "case_id": case_id,
            "recommendations": strategic_recs.get("recommendations", []),
            "next_steps": strategic_recs.get("next_steps", []),
            "risk_factors": strategic_recs.get("risk_factors", []),
            "strength_assessment": strategic_recs.get("strength_assessment", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate strategic recommendations: {str(e)}")


@router.get(
    "/{case_id}/research-links",
    summary="Get relevant research links for a case",
    description="""
    Get relevant research corpus items linked to a case based on:
    - Case type and subject matter
    - Key themes extracted from case documents
    - Legal concepts and precedents
    
    Returns categorized research items with relevance scores.
    """,
    responses={
        200: {
            "description": "Research links found successfully",
            "content": {
                "application/json": {
                    "example": {
                        "case_id": "case-001",
                        "total_found": 25,
                        "top_relevant": [
                            {
                                "id": "rc-001",
                                "name": "Employment Termination Precedents",
                                "category": "precedents",
                                "relevance_score": 0.95,
                                "description": "Key cases on wrongful dismissal and victimisation"
                            }
                        ],
                        "categorized": {
                            "precedents": [
                                {
                                    "name": "Employment Termination Cases",
                                    "relevance_score": 0.9
                                }
                            ],
                            "statutes": [
                                {
                                    "name": "Employment Rights Act 1996",
                                    "relevance_score": 0.85
                                }
                            ]
                        },
                        "search_terms": ["employment dispute", "termination", "safety"]
                    }
                }
            }
        }
    }
)
async def get_case_research_links(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get relevant research corpus items for a case"""
    try:
        from app.services.case_analysis_service import CaseAnalysisService
        
        analysis = CaseAnalysisService.analyze_case_comprehensive(case_id)
        
        if "error" in analysis:
            if "not found" in analysis["error"].lower():
                raise HTTPException(status_code=404, detail=analysis["error"])
            else:
                raise HTTPException(status_code=500, detail=analysis["error"])
        
        # Extract just the research analysis
        research_analysis = analysis.get("research_analysis", {})
        
        return {
            "case_id": case_id,
            "total_found": research_analysis.get("total_found", 0),
            "top_relevant": research_analysis.get("top_relevant", []),
            "categorized": research_analysis.get("categorized", {}),
            "search_terms": research_analysis.get("search_terms", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get research links: {str(e)}")


@router.get(
    "/{case_id}/details-analysis",
    summary="Get detailed case analysis from case description",
    description="""
    Analyze case details from the comprehensive case description to extract:
    - Legal elements (contracts, statutes, monetary amounts)
    - Timeline analysis with key events
    - Parties analysis and relationships
    - Legal issues identification
    - Evidence analysis
    - Risk assessment
    - Strategic insights and recommendations
    - Case strength assessment
    
    This analysis is based on the detailed case description and provides
    structured insights for legal strategy and case management.
    """,
    responses={
        200: {
            "description": "Case details analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "case_id": "case-001",
                        "case_title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
                        "case_type": "Employment Dispute",
                        "analysis_timestamp": "2024-01-15T10:30:00Z",
                        "legal_elements": {
                            "contracts": ["Employment Agreement"],
                            "statutes": ["Public Interest Disclosure Act 1998"],
                            "monetary_amounts": ["£20,000", "£35,000"]
                        },
                        "timeline_analysis": {
                            "events": [
                                {
                                    "date": "15 March 2022",
                                    "event": "Employment commenced",
                                    "type": "key_event"
                                }
                            ],
                            "timeline_span": "365 days (12 months)"
                        },
                        "case_strength": {
                            "overall_score": 75.5,
                            "strength_level": "Strong",
                            "confidence_level": 0.85
                        }
                    }
                }
            }
        },
        404: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case not found"}
                }
            }
        }
    }
)
async def get_case_details_analysis(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Get detailed analysis of case based on case description"""
    try:
        from app.services.case_analysis_service import CaseAnalysisService
        
        analysis = CaseAnalysisService.analyze_case_details(case_id)
        
        if "error" in analysis:
            if "not found" in analysis["error"].lower():
                raise HTTPException(status_code=404, detail=analysis["error"])
            else:
                raise HTTPException(status_code=500, detail=analysis["error"])
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze case details: {str(e)}")


@router.post(
    "/{case_id}/analyze-details",
    response_model=CaseDetailsAnalysis,
    summary="Analyze comprehensive case details",
    description="""
    Perform comprehensive case details analysis based on the case description.
    
    This endpoint analyzes all aspects of a case including:
    - Legal issues identification and applicable legislation
    - Parties analysis with roles and relationships
    - Timeline extraction with key dates and events
    - Risk assessment with identified risk factors
    - Evidence analysis and strength assessment
    - Legal precedents identification
    - Strategic recommendations and priority actions
    - Case strength assessment with confidence scoring
    
    The analysis is performed using AI to extract structured insights from the
    comprehensive case description, providing legal professionals with detailed
    analysis for case strategy and management.
    
    **Use cases:**
    - Comprehensive case evaluation
    - Strategic planning and case preparation
    - Risk assessment and mitigation planning
    - Evidence gathering prioritization
    - Legal research direction
    """,
    responses={
        200: {
            "description": "Case details analysis completed successfully",
            "content": {
                "application/json": {
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
            }
        },
        404: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case with ID case-999 not found"}
                }
            }
        },
        400: {
            "description": "Case has no description for analysis",
            "content": {
                "application/json": {
                    "example": {"detail": "Case case-001 has no description available for analysis"}
                }
            }
        },
        500: {
            "description": "Analysis failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to analyze case details: Internal error"}
                }
            }
        }
    }
)
async def analyze_case_details(
    case_id: str = Path(..., description="Unique identifier of the case to analyze", example="case-001")
):
    """Perform comprehensive case details analysis based on case description"""
    try:
        # Load case data to verify it exists and has description
        cases = DataService.load_cases()
        case = next((c for c in cases if c.get('id') == case_id), None)
        
        if case is None:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")
        
        # Check if case has description for analysis
        description = case.get('description', '')
        if not description:
            raise HTTPException(
                status_code=400, 
                detail=f"Case {case_id} has no description available for analysis"
            )
        
        # Perform comprehensive case details analysis using AIService
        from app.services.ai_service import AIService
        analysis = AIService.analyze_case_details(case_id, case.get('case_type', ''), description)
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze case details: {str(e)}")


@router.post(
    "/regenerate-analysis",
    summary="Regenerate integrated analysis for all cases",
    description="""
    Regenerate comprehensive integrated analysis for all cases in the system.
    
    This endpoint will:
    - Re-analyze all case documents
    - Update research corpus correlations
    - Refresh playbook-based strategic recommendations
    - Recalculate case strength assessments
    
    This is an administrative function that should be used after:
    - Adding new legal research materials
    - Updating playbook rules
    - Modifying analysis algorithms
    """,
    responses={
        200: {
            "description": "Case analysis regeneration completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Successfully regenerated analysis for all cases",
                        "total_cases": 6,
                        "analyzed_cases": 6,
                        "failed_cases": 0,
                        "average_confidence": 0.82,
                        "processing_time_seconds": 45,
                        "analysis_types": [
                            "Document Analysis",
                            "Research Correlation",
                            "Strategic Recommendations",
                            "Case Strength Assessment"
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Analysis regeneration failed",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Failed to regenerate case analysis",
                        "error": "Database connection error"
                    }
                }
            }
        }
    }
)
async def regenerate_case_analysis():
    """Regenerate integrated analysis for all cases"""
    import time
    from datetime import datetime
    
    start_time = time.time()
    
    try:
        from app.services.case_analysis_service import CaseAnalysisService
        
        # Use the new regeneration method
        result = CaseAnalysisService.regenerate_all_case_analyses()
        
        processing_time = time.time() - start_time
        
        if "error" in result:
            return {
                "success": False,
                "message": "Failed to regenerate case analysis",
                "error": result["error"],
                "processing_time_seconds": round(processing_time, 1)
            }
        
        analysis_types = [
            "Document Analysis",
            "Research Correlation", 
            "Strategic Recommendations",
            "Case Strength Assessment"
        ]
        
        return {
            "success": True,
            "message": f"Successfully regenerated analysis for {result['analyzed_cases']} out of {result['total_cases']} cases",
            "total_cases": result["total_cases"],
            "analyzed_cases": result["analyzed_cases"],
            "failed_cases": result["failed_cases"],
            "average_confidence": result["average_confidence"],
            "processing_time_seconds": round(processing_time, 1),
            "analysis_types": analysis_types
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        return {
            "success": False,
            "message": "Failed to regenerate case analysis",
            "error": str(e),
            "processing_time_seconds": round(processing_time, 1)
        }