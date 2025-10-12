#!/usr/bin/env python3
"""
CasesService - Cases management service for the Legal AI System

This service handles case-related operations including:
- Loading cases from JSON files
- Case search and filtering
- Case statistics
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class CasesService:
    """Service for case management operations."""
    
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
    def find_case_by_id(case_id: str) -> Optional[Dict[str, Any]]:
        """Find a specific case by ID."""
        try:
            cases = CasesService.load_cases()
            return next((c for c in cases if c.get('id') == case_id), None)
        except Exception as e:
            print(f"Error finding case: {e}")
            return None