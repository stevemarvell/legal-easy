"""
Path Resolution Service for Legal Data Reorganization

This service provides abstraction layer for data access during and after migration,
handling old and new path mappings.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Union


class PathResolutionService:
    """Service for resolving data paths during migration and after reorganization."""
    
    def __init__(self, data_root: str = "backend/app/data"):
        self.data_root = Path(data_root)
        self.migration_log_file = self.data_root / "migration_log.json"
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Path mappings for legacy support
        self.legacy_mappings = {}
        self._load_path_mappings()
        
        # Define new structure paths
        self.new_structure = {
            "cases": "cases",
            "analysis": "analysis", 
            "legal_corpus": "legal_corpus",
            "embeddings": "embeddings",
            "demo": "demo"
        }
    
    def resolve_case_path(self, case_id: str) -> Optional[Path]:
        """Get current path for case data."""
        try:
            # Try new structure first
            new_case_path = self.data_root / "cases" / case_id
            if new_case_path.exists():
                return new_case_path
            
            # Fall back to legacy structure
            legacy_case_path = self.data_root / "case_documents" / case_id
            if legacy_case_path.exists():
                self.logger.warning(f"Using legacy path for case {case_id}")
                return legacy_case_path
            
            self.logger.error(f"Case path not found for case_id: {case_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error resolving case path for {case_id}: {str(e)}")
            return None
    
    def resolve_analysis_path(self, analysis_type: str = "case_analysis") -> Optional[Path]:
        """Get current path for analysis data."""
        try:
            # Try new structure first
            new_analysis_path = self.data_root / "analysis" / f"{analysis_type}.json"
            if new_analysis_path.exists():
                return new_analysis_path
            
            # Fall back to legacy structures
            legacy_paths = [
                self.data_root / "ai" / "case_documents" / "case_documents_analysis.json",
                self.data_root / "al" / "case_documents" / "documents_analysis.json"
            ]
            
            for legacy_path in legacy_paths:
                if legacy_path.exists():
                    self.logger.warning(f"Using legacy analysis path: {legacy_path}")
                    return legacy_path
            
            self.logger.error(f"Analysis path not found for type: {analysis_type}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error resolving analysis path for {analysis_type}: {str(e)}")
            return None
    
    def resolve_index_path(self, index_type: str) -> Optional[Path]:
        """Get current path for index files."""
        try:
            index_mappings = {
                "cases": ("cases/cases_index.json", "case_documents/case_documents_index.json"),
                "analysis": ("analysis/analysis_index.json", None),
                "legal_corpus": ("legal_corpus/corpus_index.json", "legal_corpus/corpus_index.json")
            }
            
            if index_type not in index_mappings:
                self.logger.error(f"Unknown index type: {index_type}")
                return None
            
            new_path_str, legacy_path_str = index_mappings[index_type]
            
            # Try new structure first
            new_path = self.data_root / new_path_str
            if new_path.exists():
                return new_path
            
            # Fall back to legacy structure
            if legacy_path_str:
                legacy_path = self.data_root / legacy_path_str
                if legacy_path.exists():
                    self.logger.warning(f"Using legacy index path: {legacy_path}")
                    return legacy_path
            
            self.logger.error(f"Index path not found for type: {index_type}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error resolving index path for {index_type}: {str(e)}")
            return None
    
    def resolve_demo_path(self, demo_type: str) -> Optional[Path]:
        """Get current path for demo data."""
        try:
            # Try new structure first
            new_demo_path = self.data_root / "demo" / f"demo_{demo_type}.json"
            if new_demo_path.exists():
                return new_demo_path
            
            # Fall back to legacy structure (root level)
            legacy_demo_path = self.data_root / f"demo_{demo_type}.json"
            if legacy_demo_path.exists():
                self.logger.warning(f"Using legacy demo path: {legacy_demo_path}")
                return legacy_demo_path
            
            self.logger.error(f"Demo path not found for type: {demo_type}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error resolving demo path for {demo_type}: {str(e)}")
            return None
    
    def get_legacy_path_mapping(self) -> Dict[str, str]:
        """Map old paths to new paths."""
        return self.legacy_mappings.copy()
    
    def resolve_any_path(self, relative_path: str) -> Optional[Path]:
        """Resolve any relative path, checking both new and legacy locations."""
        try:
            # Check if it's already mapped
            if relative_path in self.legacy_mappings:
                new_path = self.data_root / self.legacy_mappings[relative_path]
                if new_path.exists():
                    return new_path
            
            # Try the path as-is
            direct_path = self.data_root / relative_path
            if direct_path.exists():
                return direct_path
            
            # Try common legacy to new mappings
            common_mappings = {
                "case_documents": "cases",
                "ai/case_documents": "analysis", 
                "al/case_documents": "analysis"
            }
            
            for old_prefix, new_prefix in common_mappings.items():
                if relative_path.startswith(old_prefix):
                    new_relative_path = relative_path.replace(old_prefix, new_prefix, 1)
                    new_path = self.data_root / new_relative_path
                    if new_path.exists():
                        return new_path
            
            self.logger.warning(f"Path not found: {relative_path}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error resolving path {relative_path}: {str(e)}")
            return None
    
    def update_path_mapping(self, old_path: str, new_path: str):
        """Update path mapping for legacy support."""
        self.legacy_mappings[old_path] = new_path
        self._save_path_mappings()
    
    def get_current_structure_info(self) -> Dict:
        """Get information about current data structure."""
        structure_info = {
            "migration_completed": self._is_migration_completed(),
            "available_paths": {},
            "legacy_paths": {}
        }
        
        # Check new structure
        for key, path_str in self.new_structure.items():
            path = self.data_root / path_str
            structure_info["available_paths"][key] = {
                "path": path_str,
                "exists": path.exists(),
                "is_directory": path.is_dir() if path.exists() else None
            }
        
        # Check legacy paths
        legacy_paths = ["case_documents", "ai", "al"]
        for legacy_path in legacy_paths:
            path = self.data_root / legacy_path
            structure_info["legacy_paths"][legacy_path] = {
                "path": legacy_path,
                "exists": path.exists(),
                "is_directory": path.is_dir() if path.exists() else None
            }
        
        return structure_info
    
    def validate_path_resolution(self) -> bool:
        """Validate that path resolution is working correctly."""
        try:
            # Test case path resolution
            case_dirs = []
            cases_dir = self.data_root / "cases"
            case_documents_dir = self.data_root / "case_documents"
            
            if cases_dir.exists():
                case_dirs.extend([d.name for d in cases_dir.iterdir() if d.is_dir()])
            elif case_documents_dir.exists():
                case_dirs.extend([d.name for d in case_documents_dir.iterdir() if d.is_dir()])
            
            for case_id in case_dirs[:3]:  # Test first 3 cases
                resolved_path = self.resolve_case_path(case_id)
                if not resolved_path:
                    self.logger.error(f"Failed to resolve path for case: {case_id}")
                    return False
            
            # Test analysis path resolution
            analysis_path = self.resolve_analysis_path()
            if not analysis_path:
                self.logger.warning("No analysis path found, but this may be expected")
            
            # Test index path resolution
            for index_type in ["cases", "legal_corpus"]:
                index_path = self.resolve_index_path(index_type)
                if not index_path and index_type == "cases":
                    self.logger.warning(f"No {index_type} index found, but this may be expected")
            
            self.logger.info("Path resolution validation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Path resolution validation failed: {str(e)}")
            return False
    
    def _load_path_mappings(self):
        """Load path mappings from migration log."""
        try:
            if self.migration_log_file.exists():
                with open(self.migration_log_file, 'r', encoding='utf-8') as f:
                    migration_data = json.load(f)
                    self.legacy_mappings = migration_data.get("path_mappings", {})
        except Exception as e:
            self.logger.error(f"Failed to load path mappings: {str(e)}")
    
    def _save_path_mappings(self):
        """Save path mappings to migration log."""
        try:
            migration_data = {}
            if self.migration_log_file.exists():
                with open(self.migration_log_file, 'r', encoding='utf-8') as f:
                    migration_data = json.load(f)
            
            migration_data["path_mappings"] = self.legacy_mappings
            
            with open(self.migration_log_file, 'w', encoding='utf-8') as f:
                json.dump(migration_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save path mappings: {str(e)}")
    
    def _is_migration_completed(self) -> bool:
        """Check if migration has been completed."""
        try:
            if self.migration_log_file.exists():
                with open(self.migration_log_file, 'r', encoding='utf-8') as f:
                    migration_data = json.load(f)
                    return migration_data.get("migration_status", {}).get("phase") == "complete"
            return False
        except Exception as e:
            self.logger.error(f"Failed to check migration status: {str(e)}")
            return False