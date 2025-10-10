#!/usr/bin/env python3
"""
Backup System for Legal Data Reorganization

This script creates comprehensive backups of the current data structure
and implements backup validation to ensure data integrity before migration.

Requirements addressed: 8.3
"""

import os
import json
import shutil
import hashlib
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse
import logging


class DataBackupSystem:
    """Comprehensive backup system for legal data reorganization."""
    
    def __init__(self, data_root: str = "backend/app/data", backup_root: str = "backend/backups"):
        self.data_root = Path(data_root)
        self.backup_root = Path(backup_root)
        self.backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.backup_root / f"backup_{self.backup_timestamp}"
        
        # Setup logging
        self._setup_logging()
        
        # Backup metadata
        self.backup_metadata = {
            "backup_id": f"backup_{self.backup_timestamp}",
            "created_date": datetime.now().isoformat(),
            "source_path": str(self.data_root),
            "backup_path": str(self.backup_dir),
            "backup_type": "full",
            "files_backed_up": 0,
            "total_size_bytes": 0,
            "validation_status": "pending",
            "file_checksums": {},
            "directory_structure": {},
            "backup_integrity": "unknown"
        }
    
    def _setup_logging(self):
        """Setup logging for backup operations."""
        log_dir = self.backup_root / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"backup_{self.backup_timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self, compress: bool = True) -> Dict[str, Any]:
        """Create a comprehensive backup of the data structure."""
        self.logger.info(f"Starting backup creation: {self.backup_metadata['backup_id']}")
        
        try:
            # Create backup directory
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create data backup
            self._backup_data_files()
            
            # Create metadata backup
            self._create_backup_metadata()
            
            # Validate backup integrity
            validation_result = self.validate_backup()
            
            if validation_result["is_valid"]:
                self.backup_metadata["validation_status"] = "passed"
                self.backup_metadata["backup_integrity"] = "verified"
                
                # Optionally compress backup
                if compress:
                    self._compress_backup()
                
                self.logger.info(f"Backup completed successfully: {self.backup_dir}")
            else:
                self.backup_metadata["validation_status"] = "failed"
                self.backup_metadata["backup_integrity"] = "corrupted"
                self.logger.error("Backup validation failed!")
                
        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            self.backup_metadata["validation_status"] = "error"
            self.backup_metadata["backup_integrity"] = "error"
            raise
        
        return self.backup_metadata
    
    def _backup_data_files(self):
        """Backup all data files while preserving directory structure."""
        self.logger.info("Backing up data files...")
        
        data_backup_dir = self.backup_dir / "data"
        data_backup_dir.mkdir(parents=True, exist_ok=True)
        
        files_backed_up = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.data_root):
            # Calculate relative path from data root
            rel_path = os.path.relpath(root, self.data_root)
            if rel_path == ".":
                backup_root_dir = data_backup_dir
            else:
                backup_root_dir = data_backup_dir / rel_path
                backup_root_dir.mkdir(parents=True, exist_ok=True)
            
            # Record directory structure
            self.backup_metadata["directory_structure"][rel_path] = {
                "subdirectories": dirs.copy(),
                "files": files.copy()
            }
            
            # Backup files
            for file in files:
                source_file = Path(root) / file
                backup_file = backup_root_dir / file
                
                try:
                    # Copy file
                    shutil.copy2(source_file, backup_file)
                    
                    # Calculate checksum
                    checksum = self._calculate_file_checksum(source_file)
                    rel_file_path = os.path.relpath(source_file, self.data_root)
                    
                    self.backup_metadata["file_checksums"][rel_file_path] = {
                        "checksum": checksum,
                        "size_bytes": source_file.stat().st_size,
                        "modified_time": datetime.fromtimestamp(source_file.stat().st_mtime).isoformat()
                    }
                    
                    files_backed_up += 1
                    total_size += source_file.stat().st_size
                    
                    if files_backed_up % 10 == 0:
                        self.logger.info(f"Backed up {files_backed_up} files...")
                        
                except Exception as e:
                    self.logger.error(f"Failed to backup file {source_file}: {str(e)}")
                    raise
        
        self.backup_metadata["files_backed_up"] = files_backed_up
        self.backup_metadata["total_size_bytes"] = total_size
        
        self.logger.info(f"Backed up {files_backed_up} files ({total_size:,} bytes)")
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate checksum for {file_path}: {str(e)}")
            return "checksum_failed"
    
    def _create_backup_metadata(self):
        """Create backup metadata file."""
        metadata_file = self.backup_dir / "backup_metadata.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.backup_metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Backup metadata saved: {metadata_file}")
    
    def validate_backup(self) -> Dict[str, Any]:
        """Validate backup integrity by comparing checksums."""
        self.logger.info("Validating backup integrity...")
        
        validation_result = {
            "is_valid": True,
            "validation_date": datetime.now().isoformat(),
            "files_validated": 0,
            "checksum_mismatches": [],
            "missing_files": [],
            "extra_files": [],
            "validation_errors": []
        }
        
        data_backup_dir = self.backup_dir / "data"
        
        try:
            # Check if all original files are backed up with correct checksums
            for rel_file_path, file_info in self.backup_metadata["file_checksums"].items():
                original_file = self.data_root / rel_file_path
                backup_file = data_backup_dir / rel_file_path
                
                if not backup_file.exists():
                    validation_result["missing_files"].append(rel_file_path)
                    validation_result["is_valid"] = False
                    continue
                
                # Verify checksum
                backup_checksum = self._calculate_file_checksum(backup_file)
                if backup_checksum != file_info["checksum"]:
                    validation_result["checksum_mismatches"].append({
                        "file": rel_file_path,
                        "original_checksum": file_info["checksum"],
                        "backup_checksum": backup_checksum
                    })
                    validation_result["is_valid"] = False
                
                validation_result["files_validated"] += 1
            
            # Check for extra files in backup
            for root, dirs, files in os.walk(data_backup_dir):
                for file in files:
                    backup_file = Path(root) / file
                    rel_path = os.path.relpath(backup_file, data_backup_dir)
                    
                    if rel_path not in self.backup_metadata["file_checksums"]:
                        validation_result["extra_files"].append(rel_path)
            
            if validation_result["is_valid"]:
                self.logger.info(f"Backup validation passed: {validation_result['files_validated']} files validated")
            else:
                self.logger.error(f"Backup validation failed: {len(validation_result['checksum_mismatches'])} checksum mismatches, "
                                f"{len(validation_result['missing_files'])} missing files")
                
        except Exception as e:
            validation_result["is_valid"] = False
            validation_result["validation_errors"].append(str(e))
            self.logger.error(f"Backup validation error: {str(e)}")
        
        # Save validation results
        validation_file = self.backup_dir / "validation_results.json"
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, indent=2, ensure_ascii=False)
        
        return validation_result
    
    def _compress_backup(self):
        """Compress the backup into a ZIP file."""
        self.logger.info("Compressing backup...")
        
        zip_file_path = self.backup_root / f"{self.backup_metadata['backup_id']}.zip"
        
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.backup_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = os.path.relpath(file_path, self.backup_dir)
                    zipf.write(file_path, arc_name)
        
        # Update metadata with compressed file info
        self.backup_metadata["compressed_backup"] = {
            "zip_file": str(zip_file_path),
            "compressed_size_bytes": zip_file_path.stat().st_size,
            "compression_ratio": zip_file_path.stat().st_size / self.backup_metadata["total_size_bytes"]
        }
        
        self.logger.info(f"Backup compressed: {zip_file_path} ({zip_file_path.stat().st_size:,} bytes)")
    
    def restore_backup(self, backup_path: str, target_path: Optional[str] = None) -> bool:
        """Restore data from a backup."""
        backup_dir = Path(backup_path)
        target_dir = Path(target_path) if target_path else self.data_root
        
        self.logger.info(f"Restoring backup from {backup_dir} to {target_dir}")
        
        try:
            # Load backup metadata
            metadata_file = backup_dir / "backup_metadata.json"
            if not metadata_file.exists():
                self.logger.error("Backup metadata not found")
                return False
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                backup_metadata = json.load(f)
            
            # Restore files
            data_backup_dir = backup_dir / "data"
            if not data_backup_dir.exists():
                self.logger.error("Backup data directory not found")
                return False
            
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            shutil.copytree(data_backup_dir, target_dir, dirs_exist_ok=True)
            
            # Validate restored files
            validation_passed = self._validate_restored_files(backup_metadata, target_dir)
            
            if validation_passed:
                self.logger.info("Backup restored successfully")
                return True
            else:
                self.logger.error("Backup restoration validation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Backup restoration failed: {str(e)}")
            return False
    
    def _validate_restored_files(self, backup_metadata: Dict[str, Any], target_dir: Path) -> bool:
        """Validate restored files against backup metadata."""
        self.logger.info("Validating restored files...")
        
        try:
            for rel_file_path, file_info in backup_metadata["file_checksums"].items():
                restored_file = target_dir / rel_file_path
                
                if not restored_file.exists():
                    self.logger.error(f"Restored file missing: {rel_file_path}")
                    return False
                
                # Verify checksum
                restored_checksum = self._calculate_file_checksum(restored_file)
                if restored_checksum != file_info["checksum"]:
                    self.logger.error(f"Checksum mismatch for restored file: {rel_file_path}")
                    return False
            
            self.logger.info("All restored files validated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Restored file validation error: {str(e)}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups."""
        backups = []
        
        if not self.backup_root.exists():
            return backups
        
        for item in self.backup_root.iterdir():
            if item.is_dir() and item.name.startswith("backup_"):
                metadata_file = item / "backup_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        backups.append(metadata)
                    except Exception as e:
                        self.logger.warning(f"Failed to read backup metadata: {metadata_file}: {str(e)}")
        
        return sorted(backups, key=lambda x: x["created_date"], reverse=True)


def main():
    """Main function to run backup operations."""
    parser = argparse.ArgumentParser(description="Legal data backup system")
    parser.add_argument("--action", choices=["create", "validate", "restore", "list"], 
                       default="create", help="Action to perform")
    parser.add_argument("--data-root", default="backend/app/data",
                       help="Root directory of data to backup")
    parser.add_argument("--backup-root", default="backend/backups",
                       help="Root directory for backups")
    parser.add_argument("--backup-path", help="Path to backup for restore/validate operations")
    parser.add_argument("--target-path", help="Target path for restore operation")
    parser.add_argument("--compress", action="store_true", help="Compress backup")
    
    args = parser.parse_args()
    
    backup_system = DataBackupSystem(args.data_root, args.backup_root)
    
    if args.action == "create":
        print("Creating backup...")
        result = backup_system.create_backup(compress=args.compress)
        print(f"Backup created: {result['backup_id']}")
        print(f"Files backed up: {result['files_backed_up']}")
        print(f"Total size: {result['total_size_bytes']:,} bytes")
        print(f"Validation status: {result['validation_status']}")
        
    elif args.action == "validate":
        if not args.backup_path:
            print("Error: --backup-path required for validate action")
            return
        
        backup_system.backup_dir = Path(args.backup_path)
        result = backup_system.validate_backup()
        print(f"Validation result: {'PASSED' if result['is_valid'] else 'FAILED'}")
        print(f"Files validated: {result['files_validated']}")
        
    elif args.action == "restore":
        if not args.backup_path:
            print("Error: --backup-path required for restore action")
            return
        
        success = backup_system.restore_backup(args.backup_path, args.target_path)
        print(f"Restore result: {'SUCCESS' if success else 'FAILED'}")
        
    elif args.action == "list":
        backups = backup_system.list_backups()
        print(f"Found {len(backups)} backups:")
        for backup in backups:
            print(f"  {backup['backup_id']} - {backup['created_date']} - {backup['files_backed_up']} files - {backup['validation_status']}")


if __name__ == "__main__":
    main()