#!/usr/bin/env python3
"""
Clause Storage Service - Handles storage and retrieval of extracted clauses

This service provides comprehensive storage operations for extracted clauses,
including JSON file management, ID generation, and directory organization.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.clause import ExtractedClause, ProcessingStatus


class ClauseStorageService:
    """Service for storing and retrieving extracted clauses."""
    
    def __init__(self):
        """Initialize the clause storage service."""
        self.backend_dir = Path(__file__).parent.parent.parent
        self.clauses_dir = self.backend_dir / "data" / "ai" / "research_corpus" / "clauses"
        self.clauses_dir.mkdir(parents=True, exist_ok=True)
    
    def save_clause(self, clause: ExtractedClause) -> bool:
        """
        Save a single extracted clause to JSON file.
        
        Args:
            clause: ExtractedClause object to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            file_path = self.clauses_dir / f"{clause.id}.json"
            
            # Convert clause to dictionary
            clause_data = clause.dict()
            
            # Ensure metadata has required fields
            if 'extraction_timestamp' not in clause_data['metadata']:
                clause_data['metadata']['extraction_timestamp'] = datetime.now().isoformat()
            
            # Save to JSON file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(clause_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving clause {clause.id}: {e}")
            return False
    
    def save_clauses_batch(self, clauses: List[ExtractedClause]) -> Dict[str, bool]:
        """
        Save multiple clauses in batch.
        
        Args:
            clauses: List of ExtractedClause objects to save
            
        Returns:
            Dictionary mapping clause IDs to save success status
        """
        results = {}
        
        for clause in clauses:
            results[clause.id] = self.save_clause(clause)
        
        return results
    
    def load_clause_by_id(self, clause_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a clause by its ID.
        
        Args:
            clause_id: ID of the clause to load
            
        Returns:
            Clause data as dictionary, or None if not found
        """
        try:
            file_path = self.clauses_dir / f"{clause_id}.json"
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading clause {clause_id}: {e}")
            return None
    
    def load_clauses_by_source_document(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Load all clauses from a specific source document.
        
        Args:
            document_id: ID of the source document
            
        Returns:
            List of clause data dictionaries
        """
        clauses = []
        
        try:
            # Find all clause files for this document
            pattern = f"{document_id}_clause_*.json"
            clause_files = list(self.clauses_dir.glob(pattern))
            
            # Sort by clause number
            clause_files.sort(key=lambda x: self._extract_clause_number(x.name))
            
            # Load each clause
            for file_path in clause_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    clause_data = json.load(f)
                    clauses.append(clause_data)
                    
        except Exception as e:
            print(f"Error loading clauses for document {document_id}: {e}")
        
        return clauses
    
    def delete_clause(self, clause_id: str) -> bool:
        """
        Delete a clause file.
        
        Args:
            clause_id: ID of the clause to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            file_path = self.clauses_dir / f"{clause_id}.json"
            
            if file_path.exists():
                file_path.unlink()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting clause {clause_id}: {e}")
            return False
    
    def delete_clauses_by_source_document(self, document_id: str) -> int:
        """
        Delete all clauses from a specific source document.
        
        Args:
            document_id: ID of the source document
            
        Returns:
            Number of clauses deleted
        """
        deleted_count = 0
        
        try:
            # Find all clause files for this document
            pattern = f"{document_id}_clause_*.json"
            clause_files = list(self.clauses_dir.glob(pattern))
            
            # Delete each clause file
            for file_path in clause_files:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting clause file {file_path}: {e}")
                    
        except Exception as e:
            print(f"Error deleting clauses for document {document_id}: {e}")
        
        return deleted_count
    
    def list_all_clause_ids(self) -> List[str]:
        """
        List all clause IDs in storage.
        
        Returns:
            List of clause IDs
        """
        clause_ids = []
        
        try:
            for file_path in self.clauses_dir.glob("*.json"):
                # Extract clause ID from filename (remove .json extension)
                clause_id = file_path.stem
                clause_ids.append(clause_id)
                
        except Exception as e:
            print(f"Error listing clause IDs: {e}")
        
        return sorted(clause_ids)
    
    def get_clause_count_by_document(self, document_id: str) -> int:
        """
        Get the number of clauses for a specific document.
        
        Args:
            document_id: ID of the source document
            
        Returns:
            Number of clauses for the document
        """
        try:
            pattern = f"{document_id}_clause_*.json"
            clause_files = list(self.clauses_dir.glob(pattern))
            return len(clause_files)
            
        except Exception as e:
            print(f"Error counting clauses for document {document_id}: {e}")
            return 0
    
    def get_total_clause_count(self) -> int:
        """
        Get the total number of clauses in storage.
        
        Returns:
            Total number of clauses
        """
        try:
            clause_files = list(self.clauses_dir.glob("*.json"))
            return len(clause_files)
            
        except Exception as e:
            print(f"Error counting total clauses: {e}")
            return 0
    
    def clause_exists(self, clause_id: str) -> bool:
        """
        Check if a clause exists in storage.
        
        Args:
            clause_id: ID of the clause to check
            
        Returns:
            True if clause exists, False otherwise
        """
        file_path = self.clauses_dir / f"{clause_id}.json"
        return file_path.exists()
    
    def generate_clause_id(self, source_document_id: str, clause_number: int) -> str:
        """
        Generate a clause ID using the standard format.
        
        Args:
            source_document_id: ID of the source document
            clause_number: Sequential number of the clause
            
        Returns:
            Generated clause ID in format {source_document_id}_clause_{sequential_number}
        """
        return f"{source_document_id}_clause_{clause_number:03d}"
    
    def get_next_clause_number(self, source_document_id: str) -> int:
        """
        Get the next available clause number for a document.
        
        Args:
            source_document_id: ID of the source document
            
        Returns:
            Next available clause number
        """
        try:
            pattern = f"{source_document_id}_clause_*.json"
            clause_files = list(self.clauses_dir.glob(pattern))
            
            if not clause_files:
                return 1
            
            # Extract clause numbers and find the maximum
            clause_numbers = []
            for file_path in clause_files:
                clause_number = self._extract_clause_number(file_path.name)
                if clause_number is not None:
                    clause_numbers.append(clause_number)
            
            return max(clause_numbers) + 1 if clause_numbers else 1
            
        except Exception as e:
            print(f"Error getting next clause number for document {source_document_id}: {e}")
            return 1
    
    def validate_clause_data(self, clause_data: Dict[str, Any]) -> bool:
        """
        Validate clause data structure.
        
        Args:
            clause_data: Clause data dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            'id', 'title', 'content', 'source_document_id', 
            'source_document_title', 'category', 'clause_number'
        ]
        
        try:
            # Check required fields
            for field in required_fields:
                if field not in clause_data:
                    return False
            
            # Validate ID format
            clause_id = clause_data['id']
            if not clause_id or '_clause_' not in clause_id:
                return False
            
            # Validate clause number is positive integer
            clause_number = clause_data.get('clause_number')
            if not isinstance(clause_number, int) or clause_number < 1:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating clause data: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            total_clauses = self.get_total_clause_count()
            
            # Count clauses by source document
            document_counts = {}
            for file_path in self.clauses_dir.glob("*.json"):
                clause_id = file_path.stem
                if '_clause_' in clause_id:
                    document_id = clause_id.split('_clause_')[0]
                    document_counts[document_id] = document_counts.get(document_id, 0) + 1
            
            # Calculate storage size
            total_size = sum(f.stat().st_size for f in self.clauses_dir.glob("*.json"))
            
            return {
                'total_clauses': total_clauses,
                'documents_with_clauses': len(document_counts),
                'document_clause_counts': document_counts,
                'storage_size_bytes': total_size,
                'storage_directory': str(self.clauses_dir)
            }
            
        except Exception as e:
            print(f"Error getting storage stats: {e}")
            return {}
    
    # Private helper methods
    
    def _extract_clause_number(self, filename: str) -> Optional[int]:
        """
        Extract clause number from filename.
        
        Args:
            filename: Name of the clause file
            
        Returns:
            Clause number or None if not found
        """
        try:
            # Remove .json extension
            name = filename.replace('.json', '')
            
            # Extract number after '_clause_'
            if '_clause_' in name:
                parts = name.split('_clause_')
                if len(parts) == 2:
                    return int(parts[1])
            
            return None
            
        except (ValueError, IndexError):
            return None