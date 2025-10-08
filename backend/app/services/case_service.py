import json
import os
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.case import Case, CaseStatistics


class CaseService:
    """Service for managing legal cases"""
    
    def __init__(self):
        self._cases_cache = None
        self._data_file = os.path.join(os.path.dirname(__file__), "..", "data", "demo_cases.json")
    
    def _load_cases(self) -> List[Case]:
        """Load cases from JSON file with caching"""
        if self._cases_cache is None:
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    cases_data = json.load(f)
                    self._cases_cache = [Case(**case_data) for case_data in cases_data]
            except FileNotFoundError:
                raise FileNotFoundError(f"Demo cases file not found: {self._data_file}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in demo cases file: {e}")
        return self._cases_cache
    
    def get_all_cases(self) -> List[Case]:
        """Retrieve all cases"""
        return self._load_cases()
    
    def get_case_by_id(self, case_id: str) -> Optional[Case]:
        """Retrieve a specific case by ID"""
        cases = self._load_cases()
        for case in cases:
            if case.id == case_id:
                return case
        return None
    
    def get_cases_by_type(self, case_type: str) -> List[Case]:
        """Retrieve cases filtered by type"""
        cases = self._load_cases()
        return [case for case in cases if case.case_type == case_type]
    
    def get_case_statistics(self) -> CaseStatistics:
        """Get dashboard statistics"""
        cases = self._load_cases()
        
        total_cases = len(cases)
        active_cases = len([c for c in cases if c.status == "Active"])
        resolved_cases = len([c for c in cases if c.status == "Resolved"])
        under_review_cases = len([c for c in cases if c.status == "Under Review"])
        
        # Count recent activity (cases created in last 30 days)
        thirty_days_ago = datetime.now().replace(tzinfo=None) - timedelta(days=30)
        recent_activity_count = len([
            c for c in cases 
            if c.created_date.replace(tzinfo=None) > thirty_days_ago
        ])
        
        return CaseStatistics(
            total_cases=total_cases,
            active_cases=active_cases,
            resolved_cases=resolved_cases,
            under_review_cases=under_review_cases,
            recent_activity_count=recent_activity_count
        )