#!/usr/bin/env python3
"""
CorpusService - Research corpus service for the Legal AI System

This service handles research corpus operations including:
- Loading corpus items from JSON files
- Corpus search and filtering
- Category management
- Corpus index regeneration
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class CorpusService:
    """Service for research corpus operations."""
    
    @staticmethod
    def load_corpus_items() -> List[Dict[str, Any]]:
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
    def search_corpus(query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search research corpus items."""
        try:
            corpus_items = CorpusService.load_corpus_items()
            
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
    
    @staticmethod
    def load_corpus_by_category(category: str) -> List[Dict[str, Any]]:
        """Load corpus items for a specific category."""
        try:
            corpus_items = CorpusService.load_corpus_items()
            return [item for item in corpus_items if item.get('category') == category]
        except Exception as e:
            print(f"Error loading corpus by category: {e}")
            return []
    
    @staticmethod
    def load_corpus_categories() -> Dict[str, Dict[str, Any]]:
        """Load corpus categories with metadata."""
        try:
            corpus_items = CorpusService.load_corpus_items()
            categories = {}
            
            # Group items by category
            for item in corpus_items:
                category = item.get('category', 'uncategorized')
                if category not in categories:
                    categories[category] = {
                        'name': category.replace('_', ' ').title(),
                        'description': f"Research materials in {category}",
                        'document_ids': []
                    }
                categories[category]['document_ids'].append(item.get('id'))
            
            return categories
        except Exception as e:
            print(f"Error loading corpus categories: {e}")
            return {}
    
    @staticmethod
    def load_corpus_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific corpus item by ID."""
        try:
            corpus_items = CorpusService.load_corpus_items()
            item = next((item for item in corpus_items if item.get('id') == item_id), None)
            
            if item and 'file_path' in item:
                # Load content from file
                backend_dir = Path(__file__).parent.parent.parent
                content_path = backend_dir / "data" / item['file_path']
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()
            
            return item
        except Exception as e:
            print(f"Error loading corpus item: {e}")
            return None
    
    @staticmethod
    def get_related_corpus_items(item_id: str) -> List[Dict[str, Any]]:
        """Get related corpus items based on research areas and category."""
        try:
            # Get the source item
            source_item = CorpusService.load_corpus_item_by_id(item_id)
            if not source_item:
                return []
            
            source_category = source_item.get('category')
            source_research_areas = set(source_item.get('research_areas', []))
            
            # Get all corpus items
            all_items = CorpusService.load_corpus_items()
            related_items = []
            
            for item in all_items:
                if item.get('id') == item_id:
                    continue  # Skip the source item
                
                # Calculate relevance score
                relevance_score = 0
                item_research_areas = set(item.get('research_areas', []))
                
                # Same category gets points
                if item.get('category') == source_category:
                    relevance_score += 1
                
                # Shared research areas get points
                shared_areas = source_research_areas.intersection(item_research_areas)
                relevance_score += len(shared_areas)
                
                if relevance_score > 0:
                    item_copy = item.copy()
                    item_copy['relevance_score'] = relevance_score
                    related_items.append(item_copy)
            
            # Sort by relevance score (descending) and return top 5
            related_items.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            return related_items[:5]
            
        except Exception as e:
            print(f"Error getting related corpus items: {e}")
            return []
    
    @staticmethod
    def get_corpus_research_areas() -> List[str]:
        """Get all unique research areas from the corpus."""
        try:
            corpus_items = CorpusService.load_corpus_items()
            research_areas = set()
            
            for item in corpus_items:
                areas = item.get('research_areas', [])
                research_areas.update(areas)
            
            return sorted(list(research_areas))
        except Exception as e:
            print(f"Error getting research areas: {e}")
            return []
    
    @staticmethod
    def load_corpus_metadata() -> Dict[str, Any]:
        """Load corpus metadata."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            corpus_index_path = backend_dir / "data" / "ai" / "research_corpus" / "research_corpus_index.json"
            
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                return corpus_data.get('metadata', {})
        except Exception as e:
            print(f"Error loading corpus metadata: {e}")
            return {}
    
    @staticmethod
    def regenerate_corpus_index() -> bool:
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
                                "research_areas": [category.title()],
                                "description": f"{category.title()} document: {name}",
                                "last_updated": datetime.now().isoformat()
                            })
                            
                            research_areas.add(category.title())
            
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
            
            return True
            
        except Exception as e:
            print(f"Error regenerating corpus index: {e}")
            return False