#!/usr/bin/env python3
"""
DataService - Simplified data service for the Legal AI System

This service handles all JSON data loading and searching operations including:
- Loading cases, documents, research corpus, and playbooks from JSON files
- Simple search functionality across all data types
- Direct file access without complex repository patterns
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DataService:
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
            cases_index_path = Path("data/cases/cases_index.json")
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
    
    # === DOCUMENTS MANAGEMENT ===
    
    @staticmethod
    def load_case_documents(case_id: str) -> List[Dict[str, Any]]:
        """Load all documents for a specific case."""
        try:
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
                
                # Filter documents for the specific case
                case_documents = [doc for doc in documents if doc.get('case_id') == case_id]
                return case_documents
        except Exception as e:
            print(f"Error loading case documents: {e}")
            return []
    
    @staticmethod
    def load_document_content(doc_id: str) -> str:
        """Load the full content of a document by ID."""
        try:
            # First get document metadata to find the content path
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return ""
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
                
                # Find the document
                document = None
                for doc in documents:
                    if doc.get('id') == doc_id:
                        document = doc
                        break
                
                if not document:
                    return ""
                
                # Get content from file path
                content_path = document.get('full_content_path', '')
                if content_path:
                    # Convert relative path to absolute from data root
                    full_path = Path("data") / content_path.replace('app/data/', '')
                    if full_path.exists():
                        with open(full_path, 'r', encoding='utf-8') as content_file:
                            return content_file.read()
                
                # Fallback to content preview
                return document.get('content_preview', '')
                
        except Exception as e:
            print(f"Error loading document content: {e}")
            return ""
    
    # === RESEARCH CORPUS MANAGEMENT ===
    
    @staticmethod
    def load_corpus_by_category(category: str) -> List[Dict[str, Any]]:
        """Load research corpus documents by category (contracts, clauses, precedents, statutes)."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            # Get documents for the specified category
            categories = corpus_data.get('categories', {})
            if category not in categories:
                return []
            
            document_ids = categories[category].get('document_ids', [])
            documents = corpus_data.get('documents', {})
            
            # Return list of documents for the category
            result = []
            for doc_id in document_ids:
                if doc_id in documents:
                    doc = documents[doc_id].copy()
                    doc['id'] = doc_id  # Ensure ID is included
                    result.append(doc)
            
            return result
        except Exception as e:
            print(f"Error loading corpus by category: {e}")
            return []
    
    # === PLAYBOOKS MANAGEMENT ===
    
    @staticmethod
    def load_playbooks() -> List[Dict[str, Any]]:
        """Load all playbooks from the playbooks index."""
        try:
            playbooks_index_path = Path("data/playbooks/playbooks_index.json")
            if not playbooks_index_path.exists():
                return []
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                playbooks_data = json.load(f)
                # Handle both array format and object with 'playbooks' key
                if isinstance(playbooks_data, list):
                    return playbooks_data
                return playbooks_data.get('playbooks', [])
        except Exception as e:
            print(f"Error loading playbooks: {e}")
            return []
    
    # === SEARCH METHODS ===
    
    @staticmethod
    def search_cases(query: str) -> List[Dict[str, Any]]:
        """Search cases by title, summary, or client name."""
        try:
            cases = DataService.load_cases()
            if not query:
                return cases
            
            query_lower = query.lower()
            filtered_cases = []
            
            for case in cases:
                # Search in title, summary, client_name, and key_parties
                searchable_text = " ".join([
                    case.get('title', ''),
                    case.get('summary', ''),
                    case.get('client_name', ''),
                    " ".join(case.get('key_parties', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_cases.append(case)
            
            return filtered_cases
        except Exception as e:
            print(f"Error searching cases: {e}")
            return []
    
    @staticmethod
    def search_documents(query: str) -> List[Dict[str, Any]]:
        """Search documents by name, type, or content preview."""
        try:
            # Load all documents from all cases
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
            
            if not query:
                return documents
            
            query_lower = query.lower()
            filtered_documents = []
            
            for doc in documents:
                # Search in name, type, and content_preview
                searchable_text = " ".join([
                    doc.get('name', ''),
                    doc.get('type', ''),
                    doc.get('content_preview', '')
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_documents.append(doc)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    @staticmethod
    def search_corpus(query: str) -> List[Dict[str, Any]]:
        """Search research corpus by name, description, or research areas."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            
            if not query:
                # Return all documents as list
                result = []
                for doc_id, doc_data in documents.items():
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    result.append(doc)
                return result
            
            query_lower = query.lower()
            filtered_documents = []
            
            for doc_id, doc_data in documents.items():
                # Search in name, description, and research_areas
                searchable_text = " ".join([
                    doc_data.get('name', ''),
                    doc_data.get('description', ''),
                    " ".join(doc_data.get('research_areas', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    filtered_documents.append(doc)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching corpus: {e}")
            return []
    
    # === CORPUS SPECIFIC METHODS ===
    
    @staticmethod
    def load_corpus_categories() -> Dict[str, Dict[str, Any]]:
        """Load all corpus categories."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('categories', {})
        except Exception as e:
            print(f"Error loading corpus categories: {e}")
            return {}
    
    @staticmethod
    def load_corpus_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific corpus item by ID with full content."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return None
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            if item_id not in documents:
                return None
            
            item = documents[item_id].copy()
            item['id'] = item_id
            
            # Load full content from file
            filename = item.get('filename', '')
            category = item.get('category', '')
            
            if filename and category:
                content_path = Path(f"data/research_corpus/{category}/{filename}")
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()
                else:
                    item['content'] = ""
            
            return item
        except Exception as e:
            print(f"Error loading corpus item: {e}")
            return None
    
    @staticmethod
    def load_corpus_metadata() -> Dict[str, Any]:
        """Load corpus metadata."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('corpus_metadata', {})
        except Exception as e:
            print(f"Error loading corpus metadata: {e}")
            return {}
    
    @staticmethod
    def get_corpus_research_areas() -> List[str]:
        """Get all research areas from corpus."""
        try:
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('research_areas', [])
        except Exception as e:
            print(f"Error loading research areas: {e}")
            return []
    
    @staticmethod
    def get_related_corpus_items(item_id: str) -> List[Dict[str, Any]]:
        """Get related corpus items based on research areas and category."""
        try:
            # First get the item to find its research areas and category
            item = DataService.load_corpus_item_by_id(item_id)
            if not item:
                return []
            
            item_research_areas = set(item.get('research_areas', []))
            item_category = item.get('category', '')
            
            # Load all corpus items
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            related_items = []
            
            for doc_id, doc_data in documents.items():
                if doc_id == item_id:  # Skip the item itself
                    continue
                
                doc_research_areas = set(doc_data.get('research_areas', []))
                doc_category = doc_data.get('category', '')
                
                # Calculate relevance based on shared research areas and category
                shared_areas = item_research_areas.intersection(doc_research_areas)
                same_category = item_category == doc_category
                
                if shared_areas or same_category:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    # Add relevance score
                    relevance_score = len(shared_areas) * 2 + (1 if same_category else 0)
                    doc['relevance_score'] = relevance_score
                    related_items.append(doc)
            
            # Sort by relevance score (highest first)
            related_items.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Return top 5 related items
            return related_items[:5]
        except Exception as e:
            print(f"Error getting related corpus items: {e}")
            return []
    
    # === DOCUMENTATION MANAGEMENT ===
    
    @staticmethod
    def load_documentation_categories() -> Dict[str, Dict[str, Any]]:
        """Load all documentation categories."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return {}
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            return docs_data.get('categories', {})
        except Exception as e:
            print(f"Error loading documentation categories: {e}")
            return {}
    
    @staticmethod
    def load_documentation_by_category(category: str) -> List[Dict[str, Any]]:
        """Load documentation items by category."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            # Get documents for the specified category
            categories = docs_data.get('categories', {})
            if category not in categories:
                return []
            
            document_ids = categories[category].get('document_ids', [])
            documents = docs_data.get('documents', {})
            
            # Return list of documents for the category
            result = []
            for doc_id in document_ids:
                if doc_id in documents:
                    doc = documents[doc_id].copy()
                    doc['id'] = doc_id  # Ensure ID is included
                    result.append(doc)
            
            return result
        except Exception as e:
            print(f"Error loading documentation by category: {e}")
            return []
    
    @staticmethod
    def load_documentation_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific documentation item by ID with full content."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return None
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            if item_id not in documents:
                return None
            
            item = documents[item_id].copy()
            item['id'] = item_id
            
            # Load full content from file
            filename = item.get('filename', '')
            
            if filename:
                # Look for the file in the docs directory
                content_path = Path(f"docs/{filename}")
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()
                else:
                    # Try backend/docs directory
                    content_path = Path(f"backend/docs/{filename}")
                    if content_path.exists():
                        with open(content_path, 'r', encoding='utf-8') as f:
                            item['content'] = f.read()
                    else:
                        item['content'] = ""
            
            return item
        except Exception as e:
            print(f"Error loading documentation item: {e}")
            return None
    
    @staticmethod
    def search_documentation(query: str) -> List[Dict[str, Any]]:
        """Search documentation by name, description, or tags."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            
            if not query:
                # Return all documents as list
                result = []
                for doc_id, doc_data in documents.items():
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    result.append(doc)
                return result
            
            query_lower = query.lower()
            filtered_documents = []
            
            for doc_id, doc_data in documents.items():
                # Search in name, description, and tags
                searchable_text = " ".join([
                    doc_data.get('name', ''),
                    doc_data.get('description', ''),
                    " ".join(doc_data.get('tags', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    filtered_documents.append(doc)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching documentation: {e}")
            return []
    
    @staticmethod
    def load_json_schemas() -> Dict[str, Dict[str, Any]]:
        """Load all JSON schemas."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return {}
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            return docs_data.get('schemas', {})
        except Exception as e:
            print(f"Error loading JSON schemas: {e}")
            return {}
    
    @staticmethod
    def get_all_documentation_tags() -> List[str]:
        """Get all available documentation tags."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            all_tags = set()
            
            for doc_data in documents.values():
                tags = doc_data.get('tags', [])
                all_tags.update(tags)
            
            return sorted(list(all_tags))
        except Exception as e:
            print(f"Error getting documentation tags: {e}")
            return []