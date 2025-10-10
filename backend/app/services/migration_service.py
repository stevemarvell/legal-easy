"""
Data Migration Service for Legal Data Reorganization

This service handles the systematic migration of data from the old structure to the new structure,
including backup and rollback capabilities.
"""

import os
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .path_resolution_service import PathResolutionService
from .validation_service import ValidationService


class MigrationService:
    """Service for managing data migration with backup and rollback capabilities."""
    
    def __init__(self, data_root: str = "backend/app/data"):
        self.data_root = Path(data_root)
        self.backup_root = self.data_root / "migration_backup"
        self.migration_log_file = self.data_root / "migration_log.json"
        self.path_resolver = PathResolutionService(data_root)
        self.validator = ValidationService(data_root)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Migration state tracking
        self.migration_state = {
            "migration_status": {
                "started": None,
                "completed": None,
                "phase": "planning",
                "steps_completed": [],
                "rollback_available": False
            },
            "path_mappings": {},
            "backup_location": str(self.backup_root)
        }
    
    def create_backup(self) -> bool:
        """Create comprehensive backup of current data structure."""
        try:
            self.logger.info("Creating backup of current data structure...")
            
            # Create backup directory
            if self.backup_root.exists():
                shutil.rmtree(self.backup_root)
            self.backup_root.mkdir(parents=True, exist_ok=True)
            
            # Backup all data directories
            directories_to_backup = ["ai", "al", "case_documents", "legal_corpus", "embeddings"]
            files_to_backup = [
                "demo_case_analysis_summaries.json",
                "demo_cases.json", 
                "demo_legal_corpus.json",
                "demo_playbooks.json"
            ]
            
            # Backup directories
            for dir_name in directories_to_backup:
                source_dir = self.data_root / dir_name
                if source_dir.exists():
                    backup_dir = self.backup_root / dir_name
                    shutil.copytree(source_dir, backup_dir)
                    self.logger.info(f"Backed up directory: {dir_name}")
            
            # Backup individual files
            for file_name in files_to_backup:
                source_file = self.data_root / file_name
                if source_file.exists():
                    backup_file = self.backup_root / file_name
                    shutil.copy2(source_file, backup_file)
                    self.logger.info(f"Backed up file: {file_name}")
            
            # Validate backup integrity
            if self.validator.validate_backup_integrity(str(self.data_root), str(self.backup_root)):
                self.migration_state["migration_status"]["rollback_available"] = True
                self.logger.info("Backup created and validated successfully")
                return True
            else:
                self.logger.error("Backup validation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            return False
    
    def start_migration(self) -> bool:
        """Initialize migration process."""
        try:
            self.logger.info("Starting migration process...")
            
            # Create backup first
            if not self.create_backup():
                self.logger.error("Migration aborted: backup creation failed")
                return False
            
            # Update migration state
            self.migration_state["migration_status"]["started"] = datetime.now().isoformat()
            self.migration_state["migration_status"]["phase"] = "executing"
            
            # Save migration state
            self._save_migration_state()
            
            self.logger.info("Migration initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Migration initialization failed: {str(e)}")
            return False
    
    def migrate_case_documents(self) -> bool:
        """Move all case documents from case_documents/ to cases/."""
        try:
            self.logger.info("Migrating case documents...")
            
            source_dir = self.data_root / "case_documents"
            target_dir = self.data_root / "cases"
            
            if not source_dir.exists():
                self.logger.warning("Source case_documents directory does not exist")
                return True
            
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all contents from case_documents to cases
            for item in source_dir.iterdir():
                target_path = target_dir / item.name
                if item.is_dir():
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.copytree(item, target_path)
                else:
                    shutil.copy2(item, target_path)
                
                # Update path mapping
                old_path = str(item.relative_to(self.data_root))
                new_path = str(target_path.relative_to(self.data_root))
                self.migration_state["path_mappings"][old_path] = new_path
            
            # Update migration state
            self.migration_state["migration_status"]["steps_completed"].append("migrate_case_documents")
            self._save_migration_state()
            
            self.logger.info("Case documents migration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Case documents migration failed: {str(e)}")
            return False
    
    def merge_analysis_data(self) -> bool:
        """Combine analysis from ai/ and al/ directories into analysis/."""
        try:
            self.logger.info("Merging analysis data...")
            
            ai_dir = self.data_root / "ai"
            al_dir = self.data_root / "al"
            target_dir = self.data_root / "analysis"
            
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            merged_analysis = {}
            
            # Process ai directory
            if ai_dir.exists():
                ai_analysis_file = ai_dir / "case_documents" / "case_documents_analysis.json"
                if ai_analysis_file.exists():
                    with open(ai_analysis_file, 'r', encoding='utf-8') as f:
                        ai_data = json.load(f)
                        for key, value in ai_data.items():
                            if isinstance(value, dict):
                                value["source"] = "ai"
                            merged_analysis[key] = value
            
            # Process al directory
            if al_dir.exists():
                al_analysis_file = al_dir / "case_documents" / "documents_analysis.json"
                if al_analysis_file.exists():
                    with open(al_analysis_file, 'r', encoding='utf-8') as f:
                        al_data = json.load(f)
                        for key, value in al_data.items():
                            if key in merged_analysis:
                                # Handle conflicts - merge or prioritize
                                self.logger.warning(f"Conflict found for key: {key}, merging data")
                                if isinstance(value, dict) and isinstance(merged_analysis[key], dict):
                                    merged_analysis[key].update(value)
                                    merged_analysis[key]["source"] = "merged"
                            else:
                                if isinstance(value, dict):
                                    value["source"] = "al"
                                merged_analysis[key] = value
            
            # Save merged analysis
            merged_file = target_dir / "case_analysis.json"
            with open(merged_file, 'w', encoding='utf-8') as f:
                json.dump(merged_analysis, f, indent=2, ensure_ascii=False)
            
            # Update path mappings
            if ai_dir.exists():
                self.migration_state["path_mappings"]["ai/case_documents/case_documents_analysis.json"] = "analysis/case_analysis.json"
            if al_dir.exists():
                self.migration_state["path_mappings"]["al/case_documents/documents_analysis.json"] = "analysis/case_analysis.json"
            
            # Update migration state
            self.migration_state["migration_status"]["steps_completed"].append("merge_analysis_data")
            self._save_migration_state()
            
            self.logger.info("Analysis data merge completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Analysis data merge failed: {str(e)}")
            return False
    
    def rollback_migration(self) -> bool:
        """Rollback migration to original state."""
        try:
            if not self.migration_state["migration_status"]["rollback_available"]:
                self.logger.error("No backup available for rollback")
                return False
            
            self.logger.info("Starting migration rollback...")
            
            # Remove new directories created during migration
            new_dirs = ["cases", "analysis", "demo"]
            for dir_name in new_dirs:
                dir_path = self.data_root / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path)
            
            # Restore from backup
            for item in self.backup_root.iterdir():
                target_path = self.data_root / item.name
                if target_path.exists():
                    if item.is_dir():
                        shutil.rmtree(target_path)
                    else:
                        target_path.unlink()
                
                if item.is_dir():
                    shutil.copytree(item, target_path)
                else:
                    shutil.copy2(item, target_path)
            
            # Reset migration state
            self.migration_state["migration_status"]["phase"] = "rolled_back"
            self.migration_state["migration_status"]["completed"] = datetime.now().isoformat()
            self._save_migration_state()
            
            self.logger.info("Migration rollback completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Migration rollback failed: {str(e)}")
            return False
    
    def complete_migration(self) -> bool:
        """Mark migration as complete and clean up."""
        try:
            self.logger.info("Completing migration...")
            
            # Final validation
            if not self.validator.validate_migration_integrity():
                self.logger.error("Migration validation failed")
                return False
            
            # Update migration state
            self.migration_state["migration_status"]["phase"] = "complete"
            self.migration_state["migration_status"]["completed"] = datetime.now().isoformat()
            self._save_migration_state()
            
            self.logger.info("Migration completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Migration completion failed: {str(e)}")
            return False
    
    def get_migration_status(self) -> Dict:
        """Get current migration status."""
        return self.migration_state.copy()
    
    def _save_migration_state(self):
        """Save migration state to file."""
        try:
            with open(self.migration_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.migration_state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save migration state: {str(e)}")
    
    def _load_migration_state(self):
        """Load migration state from file."""
        try:
            if self.migration_log_file.exists():
                with open(self.migration_log_file, 'r', encoding='utf-8') as f:
                    self.migration_state = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load migration state: {str(e)}")