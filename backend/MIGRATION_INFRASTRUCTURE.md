# Migration Infrastructure Documentation

This document describes the migration infrastructure created for the legal data reorganization project.

## Overview

The migration infrastructure consists of three main services that work together to safely migrate data from the old structure to the new structure:

1. **MigrationService** - Handles the actual data migration with backup and rollback capabilities
2. **PathResolutionService** - Provides abstraction for data access during and after migration
3. **ValidationService** - Ensures data integrity throughout the migration process

## Services

### MigrationService

Located: `backend/app/services/migration_service.py`

**Purpose**: Manages the systematic migration of data with backup and rollback capabilities.

**Key Methods**:
- `create_backup()` - Creates comprehensive backup of current data structure
- `start_migration()` - Initializes migration process with backup creation
- `migrate_case_documents()` - Moves case documents from case_documents/ to cases/
- `merge_analysis_data()` - Combines analysis from ai/ and al/ directories
- `rollback_migration()` - Restores original state from backup
- `complete_migration()` - Finalizes migration with validation
- `get_migration_status()` - Returns current migration state

**Features**:
- Automatic backup creation before migration
- Path mapping tracking for reference updates
- Step-by-step migration with rollback points
- Comprehensive logging and error handling

### PathResolutionService

Located: `backend/app/services/path_resolution_service.py`

**Purpose**: Provides abstraction layer for data access during and after migration.

**Key Methods**:
- `resolve_case_path(case_id)` - Gets current path for case data
- `resolve_analysis_path()` - Gets current path for analysis data
- `resolve_index_path(index_type)` - Gets current path for index files
- `resolve_demo_path(demo_type)` - Gets current path for demo data
- `get_current_structure_info()` - Returns information about data structure
- `validate_path_resolution()` - Validates path resolution functionality

**Features**:
- Automatic fallback to legacy paths
- Migration-aware path resolution
- Comprehensive structure analysis
- Legacy path mapping support

### ValidationService

Located: `backend/app/services/validation_service.py`

**Purpose**: Provides utilities for data integrity checking during migration.

**Key Methods**:
- `validate_backup_integrity()` - Validates backup completeness and accuracy
- `validate_migration_integrity()` - Validates complete migration integrity
- `validate_json_file()` - Validates JSON file formatting
- `validate_index_file()` - Validates index file structure
- `validate_case_structure()` - Validates cases directory structure
- `validate_analysis_structure()` - Validates analysis directory structure
- `generate_validation_report()` - Creates comprehensive validation report

**Features**:
- File integrity checking with checksums
- JSON structure validation
- Index consistency verification
- Comprehensive reporting

## Command Line Interface

Located: `backend/app/utils/migration_cli.py`

A command-line utility for managing the migration process.

### Usage

```bash
# Show current data structure info
python backend/app/utils/migration_cli.py info

# Show migration status
python backend/app/utils/migration_cli.py status

# Create backup
python backend/app/utils/migration_cli.py backup

# Start migration
python backend/app/utils/migration_cli.py start

# Rollback migration
python backend/app/utils/migration_cli.py rollback

# Validate data integrity
python backend/app/utils/migration_cli.py validate --type structure

# Resolve paths
python backend/app/utils/migration_cli.py resolve --case-id case-001
python backend/app/utils/migration_cli.py resolve --analysis
python backend/app/utils/migration_cli.py resolve --index cases
```

## Testing

### Test Script

Located: `backend/test_migration_infrastructure.py`

Run comprehensive tests of the migration infrastructure:

```bash
python backend/test_migration_infrastructure.py
```

### Test Results

The test script validates:
- Path resolution for cases, analysis, and indexes
- JSON file validation
- Service integration
- Current structure analysis

## Migration State Tracking

The migration process tracks its state in `backend/app/data/migration_log.json`:

```json
{
  "migration_status": {
    "started": "2024-01-01T10:00:00",
    "completed": null,
    "phase": "executing",
    "steps_completed": ["migrate_case_documents"],
    "rollback_available": true
  },
  "path_mappings": {
    "case_documents/case-001": "cases/case-001",
    "ai/case_documents/case_documents_analysis.json": "analysis/case_analysis.json"
  },
  "backup_location": "backend/app/data/migration_backup"
}
```

## Safety Features

1. **Automatic Backup**: Full backup created before any migration steps
2. **Rollback Capability**: Complete restoration to original state
3. **Step Tracking**: Individual migration steps can be monitored
4. **Path Mapping**: Legacy paths automatically mapped to new locations
5. **Validation**: Comprehensive integrity checking at each step
6. **Logging**: Detailed logging of all operations

## Integration with Existing Code

The path resolution service provides backward compatibility during migration:

```python
from services.path_resolution_service import PathResolutionService

path_service = PathResolutionService()

# This will work both before and after migration
case_path = path_service.resolve_case_path("case-001")
analysis_path = path_service.resolve_analysis_path()
```

## Error Handling

All services include comprehensive error handling:
- File system errors (permissions, missing files)
- JSON parsing errors
- Migration conflicts and duplicates
- Backup validation failures
- Network/storage issues

## Requirements Satisfied

This implementation satisfies the following requirements:

- **8.1**: Backend import paths can be updated using path resolution service
- **8.2**: Frontend data path references can be updated using path mappings
- **8.3**: System maintains full functionality with validation and rollback capabilities

## Next Steps

After implementing this infrastructure, the next tasks in the migration plan can safely:
1. Use the migration service to move data
2. Rely on path resolution for backward compatibility
3. Validate each step with the validation service
4. Rollback if any issues occur

The infrastructure is now ready to support the complete migration process outlined in the tasks.md file.