#!/usr/bin/env python3
"""
Documentation models for the Legal AI System API

This module defines the data models for system documentation including:
- Documentation categories and organization
- Document metadata and content
- JSON schemas and API specifications
- Search results and categorization
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentationItem(BaseModel):
    """Represents a single documentation item"""
    id: str = Field(..., description="Unique documentation item identifier")
    name: str = Field(..., description="Documentation item name")
    filename: str = Field(..., description="Source filename")
    category: str = Field(..., description="Documentation category")
    document_type: str = Field(..., description="Type of documentation")
    description: str = Field(..., description="Item description")
    tags: List[str] = Field(default_factory=list, description="Documentation tags")
    content: Optional[str] = Field(None, description="Full documentation content")


class DocumentationCategory(BaseModel):
    """Represents a documentation category"""
    name: str = Field(..., description="Category display name")
    description: str = Field(..., description="Category description")
    document_ids: List[str] = Field(..., description="Document IDs in this category")


class DocumentationSearchResult(BaseModel):
    """Search results for documentation"""
    items: List[DocumentationItem] = Field(..., description="Found documentation items")
    total_count: int = Field(..., description="Total number of results")
    query: str = Field(..., description="Search query used")
    categories_found: List[str] = Field(..., description="Categories containing results")
    tags_found: List[str] = Field(..., description="Tags found in results")


class JSONSchema(BaseModel):
    """Represents a JSON schema definition"""
    name: str = Field(..., description="Schema name")
    schema_definition: Dict[str, Any] = Field(..., description="JSON schema definition")
    description: Optional[str] = Field(None, description="Schema description")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="Example data")
    
    class Config:
        populate_by_name = True


class SchemasResponse(BaseModel):
    """Response containing all JSON schemas"""
    schemas: List[JSONSchema] = Field(..., description="Available JSON schemas")
    total_count: int = Field(..., description="Total number of schemas")
    categories: List[str] = Field(..., description="Schema categories")


class DocumentationOverview(BaseModel):
    """Overview of all documentation"""
    categories: Dict[str, DocumentationCategory] = Field(..., description="Documentation categories")
    total_documents: int = Field(..., description="Total number of documents")
    available_tags: List[str] = Field(..., description="All available tags")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")