"""
Validation Service for Legal Data Reorganization

This service provides utilities for data integrity checking during migration.
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import filecmp


class ValidationService:
    """Service for validating data integrity during migration."""
    
    def __init__(self, data_root: str = "backend/app/data"):
        self.data_root = Path(data_root)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validation results
        self.validation_results = {
            "file_integrity": {},
            "index_consistency": {},
            "reference_validation": {},
            "structure_validation": {}
        }
    
    def validate_backup_integrity(self, source_dir: str, backup_dir: str) -> bool:
        """Validate that backup is complete and accurate."""
        try:
            self.logger.info("Validating backup integrity...")
            
            source_path = Path(source_dir)
            backup_path = Path(backup_dir)
            
            if not backup_path.exists():
                self.logger.error("Backup directory does not exist")
                return False
            
            # Get all files in source and backup
            source_files = self._get_all_files(source_path)
            backup_files = self._get_all_files(backup_path)
            
            # Check if all source files are backed up
            missing_files = []
            for source_file in source_files:
                relative_path = source_file.relative_to(source_path)
                backup_file = backup_path / relative_path
                
                if not backup_file.exists():
                    missing_files.append(str(relative_path))
                elif not self._compare_files(source_file, backup_file):
                    missing_files.append(f"{relative_path} (content mismatch)")
            
            if missing_files:
                self.logger.error(f"Backup validation failed. Missing/mismatched files: {missing_files}")
                return False
            
            self.logger.info("Backup integrity validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup integrity validation failed: {str(e)}")
            return False
    
    def validate_migration_integrity(self) -> bool:
        """Validate complete migration integrity."""
        try:
            self.logger.info("Validating migration integrity...")
            
            # Validate file integrity
            if not self._validate_file_integrity():
                return False
            
            # Validate index consistency
            if not self._validate_index_consistency():
                return False
            
            # Validate structure
            if not self._validate_structure():
                return False
            
            self.logger.info("Migration integrity validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Migration integrity validation failed: {str(e)}")
            return False
    
    def validate_json_file(self, file_path: Path) -> bool:
        """Validate that a JSON file is properly formatted."""
        try:
            if not file_path.exists():
                self.logger.error(f"JSON file does not exist: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error validating JSON file {file_path}: {str(e)}")
            return False
    
    def validate_index_file(self, index_path: Path, expected_structure: Dict) -> bool:
        """Validate that an index file has the expected structure."""
        try:
            if not self.validate_json_file(index_path):
                return False
            
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Check required top-level keys
            for key in expected_structure.get("required_keys", []):
                if key not in index_data:
                    self.logger.error(f"Missing required key '{key}' in index file: {index_path}")
                    return False
            
            # Check metadata structure if present
            if "metadata" in index_data and "metadata_keys" in expected_structure:
                metadata = index_data["metadata"]
                for meta_key in expected_structure["metadata_keys"]:
                    if meta_key not in metadata:
                        self.logger.error(f"Missing metadata key '{meta_key}' in index file: {index_path}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating index file {index_path}: {str(e)}")
            return False
    
    def validate_case_structure(self, cases_dir: Path) -> bool:
        """Validate the structure of the cases directory."""
        try:
            if not cases_dir.exists():
                self.logger.error(f"Cases directory does not exist: {cases_dir}")
                return False
            
            # Check for cases index
            cases_index = cases_dir / "cases_index.json"
            if not cases_index.exists():
                self.logger.warning(f"Cases index file not found: {cases_index}")
            else:
                expected_structure = {
                    "required_keys": ["metadata", "cases"],
                    "metadata_keys": ["created", "last_updated", "total_cases"]
                }
                if not self.validate_index_file(cases_index, expected_structure):
                    return False
            
            # Validate individual case directories
            case_dirs = [d for d in cases_dir.iterdir() if d.is_dir()]
            for case_dir in case_dirs:
                if not self._validate_case_directory(case_dir):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating case structure: {str(e)}")
            return False
    
    def validate_analysis_structure(self, analysis_dir: Path) -> bool:
        """Validate the structure of the analysis directory."""
        try:
            if not analysis_dir.exists():
                self.logger.error(f"Analysis directory does not exist: {analysis_dir}")
                return False
            
            # Check for analysis files
            expected_files = ["case_analysis.json"]
            for file_name in expected_files:
                file_path = analysis_dir / file_name
                if file_path.exists():
                    if not self.validate_json_file(file_path):
                        return False
            
            # Check for analysis index if it exists
            analysis_index = analysis_dir / "analysis_index.json"
            if analysis_index.exists():
                expected_structure = {
                    "required_keys": ["metadata", "analyses"],
                    "metadata_keys": ["created", "last_updated", "total_analyses"]
                }
                if not self.validate_index_file(analysis_index, expected_structure):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating analysis structure: {str(e)}")
            return False
    
    def check_missing_files(self, expected_files: List[str]) -> List[str]:
        """Check for missing files in the data structure."""
        missing_files = []
        
        for file_path in expected_files:
            full_path = self.data_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        return missing_files
    
    def check_orphaned_files(self, valid_references: Set[str]) -> List[str]:
        """Check for files that are not referenced anywhere."""
        try:
            all_files = self._get_all_files(self.data_root)
            orphaned_files = []
            
            for file_path in all_files:
                relative_path = str(file_path.relative_to(self.data_root))
                if relative_path not in valid_references:
                    # Skip certain system files
                    if not self._is_system_file(file_path):
                        orphaned_files.append(relative_path)
            
            return orphaned_files
            
        except Exception as e:
            self.logger.error(f"Error checking orphaned files: {str(e)}")
            return []
    
    def generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report."""
        report = {
            "timestamp": self._get_timestamp(),
            "validation_results": self.validation_results.copy(),
            "summary": {
                "total_checks": 0,
                "passed_checks": 0,
                "failed_checks": 0,
                "warnings": 0
            }
        }
        
        # Count results
        for category, results in self.validation_results.items():
            for check, result in results.items():
                report["summary"]["total_checks"] += 1
                if result.get("status") == "passed":
                    report["summary"]["passed_checks"] += 1
                elif result.get("status") == "failed":
                    report["summary"]["failed_checks"] += 1
                elif result.get("status") == "warning":
                    report["summary"]["warnings"] += 1
        
        return report
    
    def _validate_file_integrity(self) -> bool:
        """Validate integrity of migrated files."""
        try:
            # Check that critical directories exist
            critical_dirs = ["cases", "analysis", "legal_corpus", "embeddings"]
            for dir_name in critical_dirs:
                dir_path = self.data_root / dir_name
                if dir_name in ["cases", "analysis"]:
                    # These are created during migration
                    if not dir_path.exists():
                        self.validation_results["file_integrity"][f"{dir_name}_exists"] = {
                            "status": "warning",
                            "message": f"Directory {dir_name} does not exist (may not be migrated yet)"
                        }
                else:
                    # These should always exist
                    if not dir_path.exists():
                        self.validation_results["file_integrity"][f"{dir_name}_exists"] = {
                            "status": "failed",
                            "message": f"Critical directory {dir_name} does not exist"
                        }
                        return False
                    else:
                        self.validation_results["file_integrity"][f"{dir_name}_exists"] = {
                            "status": "passed",
                            "message": f"Directory {dir_name} exists"
                        }
            
            return True
            
        except Exception as e:
            self.logger.error(f"File integrity validation failed: {str(e)}")
            return False
    
    def _validate_index_consistency(self) -> bool:
        """Validate consistency of index files."""
        try:
            # Validate cases index if it exists
            cases_index = self.data_root / "cases" / "cases_index.json"
            if cases_index.exists():
                if self.validate_json_file(cases_index):
                    self.validation_results["index_consistency"]["cases_index"] = {
                        "status": "passed",
                        "message": "Cases index is valid JSON"
                    }
                else:
                    self.validation_results["index_consistency"]["cases_index"] = {
                        "status": "failed",
                        "message": "Cases index is invalid JSON"
                    }
                    return False
            
            # Validate analysis files if they exist
            analysis_file = self.data_root / "analysis" / "case_analysis.json"
            if analysis_file.exists():
                if self.validate_json_file(analysis_file):
                    self.validation_results["index_consistency"]["analysis_file"] = {
                        "status": "passed",
                        "message": "Analysis file is valid JSON"
                    }
                else:
                    self.validation_results["index_consistency"]["analysis_file"] = {
                        "status": "failed",
                        "message": "Analysis file is invalid JSON"
                    }
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Index consistency validation failed: {str(e)}")
            return False
    
    def _validate_structure(self) -> bool:
        """Validate overall data structure."""
        try:
            # Check that we don't have both old and new structures
            old_dirs = ["case_documents", "ai", "al"]
            new_dirs = ["cases", "analysis"]
            
            old_exists = any((self.data_root / d).exists() for d in old_dirs)
            new_exists = any((self.data_root / d).exists() for d in new_dirs)
            
            if old_exists and new_exists:
                self.validation_results["structure_validation"]["migration_state"] = {
                    "status": "warning",
                    "message": "Both old and new structures exist - migration may be in progress"
                }
            elif new_exists:
                self.validation_results["structure_validation"]["migration_state"] = {
                    "status": "passed",
                    "message": "New structure exists"
                }
            elif old_exists:
                self.validation_results["structure_validation"]["migration_state"] = {
                    "status": "passed",
                    "message": "Old structure exists (pre-migration)"
                }
            else:
                self.validation_results["structure_validation"]["migration_state"] = {
                    "status": "failed",
                    "message": "No valid data structure found"
                }
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Structure validation failed: {str(e)}")
            return False
    
    def _validate_case_directory(self, case_dir: Path) -> bool:
        """Validate individual case directory structure."""
        try:
            # Check that directory contains files
            files = list(case_dir.iterdir())
            if not files:
                self.logger.warning(f"Empty case directory: {case_dir}")
                return True  # Empty is not necessarily invalid
            
            # Check for common file types
            has_documents = any(f.suffix.lower() in ['.pdf', '.txt', '.docx', '.doc'] for f in files)
            if not has_documents:
                self.logger.warning(f"Case directory has no document files: {case_dir}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating case directory {case_dir}: {str(e)}")
            return False
    
    def _get_all_files(self, directory: Path) -> List[Path]:
        """Get all files recursively from a directory."""
        files = []
        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    files.append(item)
        except Exception as e:
            self.logger.error(f"Error getting files from {directory}: {str(e)}")
        return files
    
    def _compare_files(self, file1: Path, file2: Path) -> bool:
        """Compare two files for equality."""
        try:
            return filecmp.cmp(file1, file2, shallow=False)
        except Exception as e:
            self.logger.error(f"Error comparing files {file1} and {file2}: {str(e)}")
            return False
    
    def _is_system_file(self, file_path: Path) -> bool:
        """Check if a file is a system file that should be ignored."""
        system_files = [
            "__pycache__",
            ".pyc",
            ".git",
            ".gitignore",
            "migration_log.json",
            ".DS_Store",
            "Thumbs.db"
        ]
        
        file_str = str(file_path)
        return any(sys_file in file_str for sys_file in system_files)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()