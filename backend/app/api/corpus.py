from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Dict, Any, Optional
from app.models.corpus import (
    CorpusItem, 
    CorpusCategory, 
    CorpusMetadata, 
    CorpusSearchResult,
    ConceptAnalysisResult,
    ResearchConcept
)
from app.services.corpus_service import CorpusService

router = APIRouter(
    prefix="/corpus", 
    tags=["Research Corpus"],
    responses={
        404: {"description": "Corpus item not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get(
    "/",
    response_model=List[CorpusItem],
    summary="Browse research corpus by categories",
    description="""
    Retrieve research corpus items organized by categories.
    
    This endpoint returns corpus items filtered by category:
    - **contracts**: Contract templates and agreements
    - **clauses**: Standard legal clauses and provisions
    - **precedents**: Case law and legal precedents
    - **statutes**: Legislation and regulations
    
    **Use cases:**
    - Browse research materials by type
    - Category-specific research
    - Research template discovery
    """,
    responses={
        200: {
            "description": "Corpus items retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "rc-001",
                            "name": "Employment Contract Template",
                            "filename": "rc-001_employment_template.txt",
                            "category": "contracts",
                            "document_type": "Contract Template",
                            "research_areas": ["Employment Law"],
                            "description": "Standard UK employment contract template with key clauses"
                        }
                    ]
                }
            }
        }
    }
)
async def browse_corpus(
    category: Optional[str] = Query(
        None, 
        description="Filter by category (contracts, clauses, precedents, statutes)",
        example="contracts"
    )
):
    """Browse research corpus items by category"""
    try:
        if category:
            # Load items for specific category
            items = CorpusService.load_corpus_by_category(category)
            return [CorpusItem(**item) for item in items]
        else:
            # Load all corpus items
            items = CorpusService.search_corpus("")  # Empty query returns all
            return [CorpusItem(**item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to browse corpus: {str(e)}")


@router.get(
    "/categories",
    response_model=Dict[str, CorpusCategory],
    summary="Get corpus categories",
    description="""
    Retrieve all available corpus categories with their descriptions and document counts.
    
    Returns information about:
    - Category names and descriptions
    - Document IDs in each category
    - Category organization structure
    
    **Use cases:**
    - Navigation menu generation
    - Category overview displays
    - Content organization understanding
    """,
    responses={
        200: {
            "description": "Categories retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "contracts": {
                            "name": "Contract Templates",
                            "description": "Standard UK contract templates",
                            "document_ids": ["rc-001", "rc-002", "rc-003"]
                        },
                        "clauses": {
                            "name": "Research Clauses",
                            "description": "Library of standard research clauses",
                            "document_ids": ["rc-004", "rc-005", "rc-006"]
                        }
                    }
                }
            }
        }
    }
)
async def get_categories():
    """Get all corpus categories with metadata"""
    try:
        categories = CorpusService.load_corpus_categories()
        return {
            category_id: CorpusCategory(**category_data) 
            for category_id, category_data in categories.items()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")


@router.get(
    "/search",
    response_model=CorpusSearchResult,
    summary="Search corpus using concept-based search",
    description="""
    Search the research corpus using concept-based search functionality.
    
    This endpoint provides enhanced search capabilities:
    - Text-based search across names, descriptions, and research areas
    - Category filtering for targeted results
    - Research area analysis for better context
    - Relevance-based result ordering
    
    **Use cases:**
    - Research and discovery
    - Template and clause finding
    - Concept-based research exploration
    """,
    responses={
        200: {
            "description": "Search completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "rc-001",
                                "name": "Employment Contract Template",
                                "category": "contracts",
                                "research_areas": ["Employment Law"],
                                "description": "Standard UK employment contract template"
                            }
                        ],
                        "total_count": 1,
                        "query": "employment",
                        "categories_found": ["contracts"],
                        "research_areas_found": ["Employment Law"]
                    }
                }
            }
        }
    }
)
async def search_corpus(
    q: str = Query(..., description="Search query for corpus items", example="employment"),
    category: Optional[str] = Query(
        None, 
        description="Filter by category (contracts, clauses, precedents, statutes)",
        example="contracts"
    ),
    research_area: Optional[str] = Query(
        None,
        description="Filter by research area",
        example="Employment Law"
    )
):
    """Search corpus items using concept-based search"""
    try:
        # Get search results
        items = CorpusService.search_corpus(q)
        
        # Apply category filter if specified
        if category:
            items = [item for item in items if item.get('category') == category]
        
        # Apply research area filter if specified
        if research_area:
            items = [
                item for item in items 
                if research_area in item.get('research_areas', [])
            ]
        
        # Analyze results for metadata
        categories_found = list(set(item.get('category', '') for item in items))
        research_areas_found = list(set(
            area for item in items 
            for area in item.get('research_areas', [])
        ))
        
        return CorpusSearchResult(
            items=[CorpusItem(**item) for item in items],
            total_count=len(items),
            query=q,
            categories_found=categories_found,
            research_areas_found=research_areas_found
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search corpus: {str(e)}")


@router.get(
    "/concepts",
    response_model=ConceptAnalysisResult,
    summary="Get research concept analysis",
    description="""
    Retrieve research concept analysis and relationships from the corpus.
    
    This endpoint provides:
    - Research concepts extracted from corpus materials
    - Concept relationships and connections
    - Research area categorization
    - Corpus reference mapping
    
    **Use cases:**
    - Research concept exploration
    - Research area understanding
    - Knowledge graph construction
    """,
    responses={
        200: {
            "description": "Concept analysis retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "concepts": [
                            {
                                "id": "employment-law",
                                "name": "Employment Law",
                                "definition": "Legal framework governing employer-employee relationships",
                                "related_concepts": ["Contract Law", "Labour Rights"],
                                "corpus_references": ["rc-001", "rc-007", "rc-009"]
                            }
                        ],
                        "total_concepts": 6,
                        "categories_analyzed": ["contracts", "clauses", "precedents", "statutes"],
                        "research_areas": ["Employment Law", "Contract Law", "Intellectual Property"]
                    }
                }
            }
        }
    }
)
async def get_research_concepts():
    """Get research concept analysis from corpus"""
    try:
        # Get research areas from corpus
        research_areas = CorpusService.get_corpus_research_areas()
        
        # Create research concepts based on research areas
        # In a real implementation, this would use NLP to extract concepts
        concepts = []
        concept_definitions = {
            "Employment Law": "Legal framework governing employer-employee relationships and workplace rights",
            "Contract Law": "Legal principles governing the formation, performance, and enforcement of contracts",
            "Intellectual Property": "Legal rights protecting creations of the mind, including patents, copyrights, and trademarks",
            "Data Protection": "Legal framework for protecting personal data and privacy rights",
            "Commercial Law": "Legal principles governing business transactions and commercial relationships",
            "Liability and Risk": "Research concepts related to responsibility, fault, and risk allocation"
        }
        
        for i, area in enumerate(research_areas):
            concept_id = area.lower().replace(' ', '-')
            related_concepts = [other for other in research_areas if other != area][:2]
            
            # Find corpus references for this research area
            all_items = CorpusService.search_corpus("")
            corpus_refs = [
                item['id'] for item in all_items 
                if area in item.get('research_areas', [])
            ]
            
            concept = ResearchConcept(
                id=concept_id,
                name=area,
                definition=concept_definitions.get(area, f"Research concept related to {area}"),
                related_concepts=related_concepts,
                corpus_references=corpus_refs
            )
            concepts.append(concept)
        
        # Get categories for analysis metadata
        categories = CorpusService.load_corpus_categories()
        
        return ConceptAnalysisResult(
            concepts=concepts,
            total_concepts=len(concepts),
            categories_analyzed=list(categories.keys()),
            research_areas=research_areas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get research concepts: {str(e)}")


@router.get(
    "/{item_id}",
    response_model=CorpusItem,
    summary="Get specific corpus item content",
    description="""
    Retrieve detailed information and full content for a specific corpus item.
    
    This endpoint returns:
    - Complete item metadata
    - Full document content
    - Research areas and categorization
    - Document type and description
    
    **Use cases:**
    - Document content viewing
    - Research template access
    - Research material study
    """,
    responses={
        200: {
            "description": "Corpus item retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "rc-001",
                        "name": "Employment Contract Template",
                        "filename": "rc-001_employment_template.txt",
                        "category": "contracts",
                        "document_type": "Contract Template",
                        "research_areas": ["Employment Law"],
                        "description": "Standard UK employment contract template with key clauses",
                        "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
                    }
                }
            }
        },
        404: {
            "description": "Corpus item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Corpus item with ID rc-999 not found"}
                }
            }
        }
    }
)
async def get_corpus_item(
    item_id: str = Path(..., description="Unique identifier of the corpus item", example="rc-001")
):
    """Get detailed information and content for a specific corpus item"""
    try:
        item = CorpusService.load_corpus_item_by_id(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Corpus item with ID {item_id} not found")
        
        return CorpusItem(**item)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get corpus item: {str(e)}")


@router.get(
    "/{item_id}/related",
    response_model=List[CorpusItem],
    summary="Get related materials for corpus item",
    description="""
    Retrieve related research materials for a specific corpus item.
    
    This endpoint finds related items based on:
    - Shared research areas
    - Same category classification
    - Research concept relationships
    - Content similarity
    
    **Use cases:**
    - Research expansion
    - Related document discovery
    - Comprehensive research analysis
    """,
    responses={
        200: {
            "description": "Related materials retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "rc-004",
                            "name": "Termination Clauses",
                            "category": "clauses",
                            "research_areas": ["Employment Law"],
                            "description": "Various termination clause templates and examples",
                            "relevance_score": 3
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Corpus item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Corpus item with ID rc-999 not found"}
                }
            }
        }
    }
)
async def get_related_materials(
    item_id: str = Path(..., description="Unique identifier of the corpus item", example="rc-001")
):
    """Get related research materials for a specific corpus item"""
    try:
        # First verify the item exists
        item = CorpusService.load_corpus_item_by_id(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Corpus item with ID {item_id} not found")
        
        # Get related items
        related_items = CorpusService.get_related_corpus_items(item_id)
        
        return [CorpusItem(**item) for item in related_items]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get related materials: {str(e)}")


@router.post(
    "/regenerate-index",
    summary="Regenerate corpus index",
    description="""
    Regenerate the corpus index by scanning the corpus directory structure.
    
    This endpoint will:
    - Scan all corpus directories (contracts, clauses, precedents, statutes)
    - Extract metadata from document files
    - Generate legal concept mappings
    - Update the research_corpus_index.json file
    
    **Use cases:**
    - After adding new documents to the corpus
    - Updating metadata and relationships
    - Maintenance and data refresh
    
    **Note:** This operation may take some time for large corpora.
    """,
    responses={
        200: {
            "description": "Index regenerated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Corpus index regenerated successfully",
                        "total_documents": 10,
                        "research_areas": ["Employment Law", "Contract Law"],
                        "legal_concepts_count": 15
                    }
                }
            }
        },
        500: {
            "description": "Index regeneration failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to regenerate corpus index"}
                }
            }
        }
    }
)
async def regenerate_corpus_index():
    """Regenerate the corpus index by scanning the directory structure"""
    try:
        success = CorpusService.regenerate_corpus_index()
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to regenerate corpus index")
        
        # Load the new index to get statistics
        corpus_metadata = CorpusService.load_corpus_metadata()
        research_areas = CorpusService.get_corpus_research_areas()
        
        return {
            "success": True,
            "message": "Corpus index regenerated successfully",
            "total_documents": corpus_metadata.get("total_documents", 0),
            "research_areas": research_areas,
            "legal_concepts_count": corpus_metadata.get("legal_concepts_count", 0),
            "last_updated": corpus_metadata.get("last_updated", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate corpus index: {str(e)}")