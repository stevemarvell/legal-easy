#!/usr/bin/env python3
"""
Migration CLI Utility

Command-line interface for managing legal data reorganization migration.
"""

import sys
import argparse
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from services.migration_service import MigrationService
from services.path_resolution_service import PathResolutionService
from services.validation_service import ValidationService


def main():
    parser = argparse.ArgumentParser(description="Legal Data Migration Utility")
    parser.add_argument("--data-root", default="backend/app/data", 
                       help="Root directory for data (default: backend/app/data)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show migration status")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create backup of current data")
    
    # Start migration command
    start_parser = subparsers.add_parser("start", help="Start migration process")
    
    # Rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback migration")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate data integrity")
    validate_parser.add_argument("--type", choices=["backup", "migration", "structure"], 
                                default="structure", help="Type of validation to perform")
    
    # Path resolution command
    path_parser = subparsers.add_parser("resolve", help="Resolve data paths")
    path_parser.add_argument("--case-id", help="Resolve path for specific case ID")
    path_parser.add_argument("--analysis", action="store_true", help="Resolve analysis path")
    path_parser.add_argument("--index", choices=["cases", "analysis", "legal_corpus"], 
                            help="Resolve index path")
    path_parser.add_argument("--demo", help="Resolve demo path for specific type")
    
    # Structure info command
    info_parser = subparsers.add_parser("info", help="Show current data structure info")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize services
    migration_service = MigrationService(args.data_root)
    path_service = PathResolutionService(args.data_root)
    validation_service = ValidationService(args.data_root)
    
    try:
        if args.command == "status":
            status = migration_service.get_migration_status()
            print(json.dumps(status, indent=2))
        
        elif args.command == "backup":
            print("Creating backup...")
            if migration_service.create_backup():
                print("Backup created successfully")
            else:
                print("Backup creation failed")
                sys.exit(1)
        
        elif args.command == "start":
            print("Starting migration...")
            if migration_service.start_migration():
                print("Migration started successfully")
            else:
                print("Migration start failed")
                sys.exit(1)
        
        elif args.command == "rollback":
            print("Rolling back migration...")
            if migration_service.rollback_migration():
                print("Migration rolled back successfully")
            else:
                print("Migration rollback failed")
                sys.exit(1)
        
        elif args.command == "validate":
            print(f"Running {args.type} validation...")
            
            if args.type == "backup":
                # This would need source and backup paths
                print("Backup validation requires source and backup directories")
                sys.exit(1)
            elif args.type == "migration":
                if validation_service.validate_migration_integrity():
                    print("Migration validation passed")
                else:
                    print("Migration validation failed")
                    sys.exit(1)
            elif args.type == "structure":
                # Validate current structure
                cases_dir = Path(args.data_root) / "cases"
                analysis_dir = Path(args.data_root) / "analysis"
                
                results = []
                if cases_dir.exists():
                    results.append(("Cases structure", validation_service.validate_case_structure(cases_dir)))
                if analysis_dir.exists():
                    results.append(("Analysis structure", validation_service.validate_analysis_structure(analysis_dir)))
                
                if not results:
                    print("No migrated structure found to validate")
                else:
                    for name, result in results:
                        print(f"{name}: {'PASSED' if result else 'FAILED'}")
        
        elif args.command == "resolve":
            if args.case_id:
                path = path_service.resolve_case_path(args.case_id)
                print(f"Case path for '{args.case_id}': {path}")
            
            if args.analysis:
                path = path_service.resolve_analysis_path()
                print(f"Analysis path: {path}")
            
            if args.index:
                path = path_service.resolve_index_path(args.index)
                print(f"Index path for '{args.index}': {path}")
            
            if args.demo:
                path = path_service.resolve_demo_path(args.demo)
                print(f"Demo path for '{args.demo}': {path}")
            
            if not any([args.case_id, args.analysis, args.index, args.demo]):
                print("Please specify what to resolve (--case-id, --analysis, --index, or --demo)")
        
        elif args.command == "info":
            info = path_service.get_current_structure_info()
            print(json.dumps(info, indent=2))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()