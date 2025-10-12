#!/usr/bin/env python3
"""
ClauseIndexService - Service for managing consolidated clause index

This service creates and maintains a consolidated index of all extracted clauses
in a single file for efficient access and searching.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from ..models.clause import ExtractedClause, Clause, extracted_clause_to_clause


class ClauseIndexService:
    """Service for managing consolidated clause index."""
    
    def __init__(self):
        """Initialize the clause index service."""
        self.backend_dir = Path(__file__).parent.parent.parent
        self.clauses_dir = self.backend_dir / "data" / "ai" / "research_corpus" / "clauses"
        self.index_file = self.backend_dir / "data" / "ai" / "research_corpus" / "clauses_index.json"
    
    def generate_consolidated_index(self) -> List[Dict[str, Any]]:
        """
        Generate consolidated clause index from all individual clause files.
        
        Returns:
            List of clause dictionaries in the frontend-compatible format
        """
        clauses = []
        
        if not self.clauses_dir.exists():
            return clauses
        
        # Read all clause JSON files
        for clause_file in self.clauses_dir.glob("*.json"):
            try:
                with open(clause_file, 'r', encoding='utf-8') as f:
                    clause_data = json.load(f)
                
                # Convert to ExtractedClause model for validation
                extracted_clause = ExtractedClause(**clause_data)
                
                # Convert to frontend-compatible Clause model
                frontend_clause = extracted_clause_to_clause(extracted_clause)
                
                # Convert to dictionary for JSON serialization
                clause_dict = frontend_clause.dict()
                
                clauses.append(clause_dict)
                
            except Exception as e:
                print(f"Error processing clause file {clause_file}: {e}")
                continue
        
        # Sort clauses by document source and clause number
        clauses.sort(key=lambda x: (x['document_source'], int(x['clause_number']) if x['clause_number'].isdigit() else 999))
        
        return clauses
    
    def save_consolidated_index(self, clauses: List[Dict[str, Any]] = None) -> bool:
        """
        Save consolidated clause index to file.
        
        Args:
            clauses: Optional list of clauses. If None, will generate from files.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if clauses is None:
                clauses = self.generate_consolidated_index()
            
            # Create index structure
            index_data = {
                "clauses": clauses,
                "metadata": {
                    "total_clauses": len(clauses),
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            
            # Ensure directory exists
            self.index_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to file
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving consolidated index: {e}")
            return False
    
    def load_consolidated_index(self) -> List[Dict[str, Any]]:
        """
        Load consolidated clause index from file.
        
        Returns:
            List of clause dictionaries
        """
        try:
            if not self.index_file.exists():
                # Generate and save if doesn't exist
                clauses = self.generate_consolidated_index()
                self.save_consolidated_index(clauses)
                return clauses
            
            with open(self.index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            return index_data.get('clauses', [])
            
        except Exception as e:
            print(f"Error loading consolidated index: {e}")
            return []
    
    def refresh_index(self) -> bool:
        """
        Refresh the consolidated index by regenerating from individual files.
        
        Returns:
            True if successful, False otherwise
        """
        clauses = self.generate_consolidated_index()
        return self.save_consolidated_index(clauses)
    
    def get_clauses_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get clauses filtered by category.
        
        Args:
            category: Category to filter by (policy, regulation, precedent, guideline)
            
        Returns:
            List of clauses in the specified category
        """
        all_clauses = self.load_consolidated_index()
        return [clause for clause in all_clauses if clause.get('category') == category]
    
    def search_clauses(self, query: str) -> List[Dict[str, Any]]:
        """
        Search clauses by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching clauses
        """
        all_clauses = self.load_consolidated_index()
        query_lower = query.lower()
        
        matching_clauses = []
        
        for clause in all_clauses:
            # Search in title, content, tags, and keywords
            searchable_text = " ".join([
                clause.get('title', ''),
                clause.get('content', ''),
                " ".join(clause.get('tags', [])),
                " ".join(clause.get('relevance_keywords', []))
            ]).lower()
            
            if query_lower in searchable_text:
                matching_clauses.append(clause)
        
        return matching_clauses
    
    def get_index_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the clause index.
        
        Returns:
            Dictionary containing index metadata
        """
        try:
            if not self.index_file.exists():
                return {"total_clauses": 0, "last_updated": None, "version": "1.0"}
            
            with open(self.index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            return index_data.get('metadata', {})
            
        except Exception as e:
            print(f"Error getting index metadata: {e}")
            return {"total_clauses": 0, "last_updated": None, "version": "1.0"}