#!/usr/bin/env python3
"""
Documentation API endpoints for the Legal AI System

This module provides API endpoints for system documentation including:
- Documentation categories and browsing
- Searchable documentation content
- JSON schemas and API specifications
- Category-specific documentation access
"""

from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Dict, Any, Optional
from app.models.documentation import (
    DocumentationItem,
    DocumentationCategory,
    DocumentationSearchResult,
    JSONSchema,
    SchemasResponse,
    DocumentationOverview
)
from app.services.data_service import DataService

router = APIRouter(
    prefix="/docs", 
    tags=["Documentation"],
    responses={
        404: {"description": "Documentation not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get(
    "/",
    response_model=DocumentationOverview,
    summary="Get documentation categories",
    description="""
    Retrieve all documentation categories with their descriptions and document counts.
    
    This endpoint returns:
    - All available documentation categories
    - Category descriptions and metadata
    - Total document counts
    - Available tags for filtering
    
    **Use cases:**
    - Navigation menu generation
    - Documentation overview displays
    - Category browsing interfaces
    """,
    responses={
        200: {
            "description": "Documentation categories retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "categories": {
                            "api": {
                                "name": "API Documentation",
                                "description": "Complete API reference and examples",
                                "document_ids": ["api-overview", "api-examples"]
                            }
                        },
                        "total_documents": 6,
                        "available_tags": ["api", "reference", "examples"],
                        "last_updated": "2024-01-15T10:00:00Z"
                    }
                }
            }
        }
    }
)
async def get_documentation_categories():
    """Get all documentation categories with metadata"""
    try:
        categories = DataService.load_documentation_categories()
        
        # Count total documents
        total_documents = sum(
            len(category.get('document_ids', [])) 
            for category in categories.values()
        )
        
        # Get all available tags
        available_tags = DataService.get_all_documentation_tags()
        
        return DocumentationOverview(
            categories={
                category_id: DocumentationCategory(**category_data) 
                for category_id, category_data in categories.items()
            },
            total_documents=total_documents,
            available_tags=available_tags
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get documentation categories: {str(e)}")


@router.get(
    "/search",
    response_model=DocumentationSearchResult,
    summary="Search documentation content",
    description="""
    Search through all documentation content using text-based search.
    
    This endpoint provides:
    - Full-text search across documentation names, descriptions, and tags
    - Category filtering for targeted results
    - Tag-based filtering and discovery
    - Relevance-based result ordering
    
    **Use cases:**
    - Documentation search functionality
    - Content discovery and exploration
    - Filtered documentation browsing
    """,
    responses={
        200: {
            "description": "Search completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "api-overview",
                                "name": "API Overview",
                                "category": "api",
                                "description": "Complete API overview and getting started guide",
                                "tags": ["api", "reference", "getting-started"]
                            }
                        ],
                        "total_count": 1,
                        "query": "api",
                        "categories_found": ["api"],
                        "tags_found": ["api", "reference"]
                    }
                }
            }
        }
    }
)
async def search_documentation(
    q: str = Query(..., description="Search query for documentation", example="api"),
    category: Optional[str] = Query(
        None, 
        description="Filter by category (api, architecture, deployment)",
        example="api"
    ),
    tag: Optional[str] = Query(
        None,
        description="Filter by tag",
        example="reference"
    )
):
    """Search documentation content"""
    try:
        # Get search results
        items = DataService.search_documentation(q)
        
        # Apply category filter if specified
        if category:
            items = [item for item in items if item.get('category') == category]
        
        # Apply tag filter if specified
        if tag:
            items = [
                item for item in items 
                if tag in item.get('tags', [])
            ]
        
        # Analyze results for metadata
        categories_found = list(set(item.get('category', '') for item in items))
        tags_found = list(set(
            tag for item in items 
            for tag in item.get('tags', [])
        ))
        
        return DocumentationSearchResult(
            items=[DocumentationItem(**item) for item in items],
            total_count=len(items),
            query=q,
            categories_found=categories_found,
            tags_found=tags_found
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search documentation: {str(e)}")


@router.get(
    "/schemas",
    response_model=SchemasResponse,
    summary="Get JSON schemas and examples",
    description="""
    Retrieve all JSON schemas used in the API with examples and descriptions.
    
    This endpoint provides:
    - Complete JSON schema definitions for all data models
    - Example data for each schema
    - Schema descriptions and usage information
    - API specification details
    
    **Use cases:**
    - API client development
    - Data validation and testing
    - Integration documentation
    - Schema reference and validation
    """,
    responses={
        200: {
            "description": "Schemas retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "schemas": [
                            {
                                "name": "Case",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"}
                                    }
                                },
                                "description": "Legal case data model"
                            }
                        ],
                        "total_count": 4,
                        "categories": ["api", "data-models"]
                    }
                }
            }
        }
    }
)
async def get_json_schemas():
    """Get all JSON schemas and examples"""
    try:
        schemas_data = DataService.load_json_schemas()
        
        schemas = []
        for schema_name, schema_def in schemas_data.items():
            schema = JSONSchema(
                name=schema_name,
                schema_definition=schema_def,
                description=f"JSON schema for {schema_name} data model"
            )
            schemas.append(schema)
        
        return SchemasResponse(
            schemas=schemas,
            total_count=len(schemas),
            categories=["api", "data-models", "schemas"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get JSON schemas: {str(e)}")


@router.get(
    "/{category}",
    response_model=List[DocumentationItem],
    summary="Get documentation by category",
    description="""
    Retrieve all documentation items for a specific category.
    
    Available categories:
    - **api**: API reference and examples
    - **architecture**: System architecture and design documentation
    - **deployment**: Deployment and configuration guides
    
    **Use cases:**
    - Category-specific documentation browsing
    - Organized content access
    - Documentation navigation
    """,
    responses={
        200: {
            "description": "Category documentation retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "api-overview",
                            "name": "API Overview",
                            "filename": "README.md",
                            "category": "api",
                            "document_type": "API Reference",
                            "description": "Complete API overview and getting started guide",
                            "tags": ["api", "reference", "getting-started"],
                            "content": "# API Overview\n\nWelcome to the API..."
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Category not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Documentation category 'invalid' not found"}
                }
            }
        }
    }
)
async def get_documentation_by_category(
    category: str = Path(..., description="Documentation category", example="api")
):
    """Get all documentation items for a specific category"""
    try:
        # Verify category exists
        categories = DataService.load_documentation_categories()
        if category not in categories:
            raise HTTPException(status_code=404, detail=f"Documentation category '{category}' not found")
        
        # Get documentation items for the category
        items = DataService.load_documentation_by_category(category)
        
        # Load full content for each item
        result = []
        for item in items:
            # Load full content
            full_item = DataService.load_documentation_item_by_id(item['id'])
            if full_item:
                result.append(DocumentationItem(**full_item))
            else:
                result.append(DocumentationItem(**item))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get documentation by category: {str(e)}")