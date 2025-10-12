#!/usr/bin/env python3
"""
ResearchService - Simplified data service for the Legal AI System

This service handles all JSON data loading operations including:
- Loading cases, documents, research corpus, and playbooks from JSON files
- Simple search functionality across all data types
- Direct file access without complex repository patterns
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class ResearchService:
    """Single service for all JSON data loading and searching."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.cases_path = self.data_root / "cases"
        self.research_corpus_path = self.data_root / "research_corpus"
        self.playbooks_path = self.data_root / "playbooks"
    
    # === CASES MANAGEMENT ===
    
    @staticmethod
    def load_cases() -> List[Dict[str, Any]]:
        """Load all cases from the cases index."""
        try:
            # Use absolute path from the backend directory
            backend_dir = Path(__file__).parent.parent.parent
            cases_index_path = backend_dir / "data" / "cases" / "cases_index.json"
            
            if not cases_index_path.exists():
                return []
            
            with open(cases_index_path, 'r', encoding='utf-8') as f:
                cases_data = json.load(f)
                
                # Handle both array format and object with 'cases' key
                if isinstance(cases_data, list):
                    return cases_data
                return cases_data.get('cases', [])
        except Exception as e:
            print(f"Error loading cases: {e}")
            return []
    
    @staticmethod
    def load_case_documents(case_id: str) -> List[Dict[str, Any]]:
        """Load all documents for a specific case."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            case_docs_path = backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
            
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                all_docs = json.load(f)
                
                # Filter documents for the specific case
                case_docs = [doc for doc in all_docs if doc.get('case_id') == case_id]
                return case_docs
        except Exception as e:
            print(f"Error loading case documents: {e}")
            return []
    
    @staticmethod
    def load_document_content(document_id: str) -> Optional[str]:
        """Load the full text content of a document."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            
            # First, find the document in the index to get its path
            case_docs_path = backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
            
            if not case_docs_path.exists():
                return None
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                all_docs = json.load(f)
            
            # Find the document
            document = next((doc for doc in all_docs if doc.get('id') == document_id), None)
            if not document:
                return None
            
            # Load content from the document's file path
            if 'full_content_path' in document:
                content_path = backend_dir / "data" / document['full_content_path']
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        return f.read()
            
            # Fallback to content preview if full content not available
            return document.get('content_preview', '')
            
        except Exception as e:
            print(f"Error loading document content: {e}")
            return None
    
    # === RESEARCH CORPUS MANAGEMENT ===
    
    @staticmethod
    def load_research_corpus() -> List[Dict[str, Any]]:
        """Load all research corpus items."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            corpus_index_path = backend_dir / "data" / "ai" / "research_corpus" / "research_corpus_index.json"
            
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                return corpus_data.get('corpus_items', [])
        except Exception as e:
            print(f"Error loading research corpus: {e}")
            return []
    
    @staticmethod
    def search_research_corpus(query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search research corpus items."""
        try:
            corpus_items = ResearchService.load_research_corpus()
            
            if not query:
                return corpus_items
            
            # Simple text search in name and description
            query_lower = query.lower()
            results = []
            
            for item in corpus_items:
                name = item.get('name', '').lower()
                description = item.get('description', '').lower()
                research_areas = ' '.join(item.get('research_areas', [])).lower()
                
                if (query_lower in name or 
                    query_lower in description or 
                    query_lower in research_areas):
                    results.append(item)
            
            return results
        except Exception as e:
            print(f"Error searching research corpus: {e}")
            return []
    
    # === PLAYBOOKS MANAGEMENT ===
    
    @staticmethod
    def load_playbooks() -> List[Dict[str, Any]]:
        """Load all playbooks from the playbooks index."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            playbooks_index_path = backend_dir / "data" / "playbooks" / "playbooks_index.json"
            
            if not playbooks_index_path.exists():
                return []
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                playbooks_data = json.load(f)
                return playbooks_data.get('playbooks', [])
        except Exception as e:
            print(f"Error loading playbooks: {e}")
            return []
    
    @staticmethod
    def get_playbook_by_id(playbook_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific playbook by ID."""
        try:
            playbooks = ResearchService.load_playbooks()
            return next((p for p in playbooks if p.get('id') == playbook_id), None)
        except Exception as e:
            print(f"Error getting playbook: {e}")
            return None
    
    # === CORPUS INDEX REGENERATION ===
    
    @staticmethod
    def regenerate_corpus_index() -> Dict[str, Any]:
        """Regenerate the research corpus index."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            
            # Scan research corpus directories
            corpus_base = backend_dir / "data" / "research_corpus"
            corpus_items = []
            research_areas = set()
            
            if corpus_base.exists():
                # Scan different corpus categories
                categories = ['contracts', 'clauses', 'precedents', 'statutes']
                
                for category in categories:
                    category_path = corpus_base / category
                    if category_path.exists():
                        for file_path in category_path.glob('*.txt'):
                            # Create corpus item from file
                            item_id = file_path.stem
                            name = file_path.stem.replace('_', ' ').replace('-', ' ').title()
                            
                            corpus_items.append({
                                "id": item_id,
                                "name": name,
                                "category": category,
                                "file_path": str(file_path.relative_to(backend_dir / "data")),
                                "research_areas": [category],
                                "description": f"{category.title()} document: {name}",
                                "last_updated": datetime.now().isoformat()
                            })
                            
                            research_areas.add(category)
            
            # Save the regenerated index
            index_data = {
                "corpus_items": corpus_items,
                "metadata": {
                    "total_items": len(corpus_items),
                    "research_areas": list(research_areas),
                    "last_regenerated": datetime.now().isoformat()
                }
            }
            
            # Ensure AI directory exists
            ai_dir = backend_dir / "data" / "ai" / "research_corpus"
            ai_dir.mkdir(parents=True, exist_ok=True)
            
            # Save index
            index_path = ai_dir / "research_corpus_index.json"
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": "Research corpus index regenerated successfully",
                "total_documents": len(corpus_items),
                "research_areas": list(research_areas),
                "legal_concepts_count": len(corpus_items),  # Simplified count
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error regenerating corpus index: {e}")
            return {
                "success": False,
                "message": f"Failed to regenerate corpus index: {str(e)}",
                "total_documents": 0,
                "research_areas": [],
                "legal_concepts_count": 0,
                "last_updated": datetime.now().isoformat()
            }