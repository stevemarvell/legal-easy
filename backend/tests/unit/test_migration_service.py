"""
Unit tests for MigrationService

Tests the data migration service functionality including backup, rollback,
and migration operations.
"""

import pytest
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from app.services.migration_service import MigrationService


class TestMigrationService:
    """Test cases for MigrationService."""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def migration_service(self, temp_data_dir):
        """Create MigrationService instance with temporary directory."""
        return MigrationService(data_root=temp_data_dir)
    
    @pytest.fixture
    def sample_data_structure(self, temp_data_dir):
        """Create sample data structure for testing."""
        data_root = Path(temp_data_dir)
        
        # Create directories
        (data_root / "case_documents").mkdir(parents=True)
        (data_root / "ai" / "case_documents").mkdir(parents=True)
        (data_root / "al" / "case_documents").mkdir(parents=True)
        (data_root / "legal_corpus").mkdir(parents=True)
        (data_root / "embeddings").mkdir(parents=True)
        
        # Create sample files
        case_data = {"case-001": {"name": "Test Case", "documents": ["doc1.pdf"]}}
        with open(data_root / "case_documents" / "case_documents_index.json", 'w') as f:
            json.dump(case_data, f)
        
        ai_analysis = {"doc1": {"analysis": "AI analysis", "confidence": 0.9}}
        with open(data_root / "ai" / "case_documents" / "case_documents_analysis.json", 'w') as f:
            json.dump(ai_analysis, f)
        
        al_analysis = {"doc2": {"analysis": "AL analysis", "confidence": 0.8}}
        with open(data_root / "al" / "case_documents" / "documents_analysis.json", 'w') as f:
            json.dump(al_analysis, f)
        
        # Create demo files
        demo_data = {"demo": "data"}
        for demo_file in ["demo_cases.json", "demo_playbooks.json"]:
            with open(data_root / demo_file, 'w') as f:
                json.dump(demo_data, f)
        
        return data_root
    
    def test_init(self, temp_data_dir):
        """Test MigrationService initialization."""
        service = MigrationService(data_root=temp_data_dir)
        
        assert service.data_root == Path(temp_data_dir)
        assert service.backup_root == Path(temp_data_dir) / "migration_backup"
        assert service.migration_log_file == Path(temp_data_dir) / "migration_log.json"
        assert service.path_resolver is not None
        assert service.validator is not None
        assert "migration_status" in service.migration_state
        assert "path_mappings" in service.migration_state
    
    def test_create_backup_success(self, migration_service, sample_data_structure):
        """Test successful backup creation."""
        with patch.object(migration_service.validator, 'validate_backup_integrity', return_value=True):
            result = migration_service.create_backup()
            
            assert result is True
            assert migration_service.backup_root.exists()
            assert migration_service.migration_state["migration_status"]["rollback_available"] is True
            
            # Check that directories were backed up
            assert (migration_service.backup_root / "case_documents").exists()
            assert (migration_service.backup_root / "ai").exists()
            assert (migration_service.backup_root / "al").exists()
            
            # Check that files were backed up
            assert (migration_service.backup_root / "demo_cases.json").exists()
            assert (migration_service.backup_root / "demo_playbooks.json").exists()
    
    def test_create_backup_validation_failure(self, migration_service, sample_data_structure):
        """Test backup creation with validation failure."""
        with patch.object(migration_service.validator, 'validate_backup_integrity', return_value=False):
            result = migration_service.create_backup()
            
            assert result is False
            assert migration_service.migration_state["migration_status"]["rollback_available"] is False
    
    def test_create_backup_exception(self, migration_service):
        """Test backup creation with exception."""
        # Create a scenario that will cause an exception
        with patch('shutil.copytree', side_effect=Exception("Test exception")):
            result = migration_service.create_backup()
            
            assert result is False
    
    def test_start_migration_success(self, migration_service, sample_data_structure):
        """Test successful migration start."""
        with patch.object(migration_service, 'create_backup', return_value=True):
            result = migration_service.start_migration()
            
            assert result is True
            assert migration_service.migration_state["migration_status"]["started"] is not None
            assert migration_service.migration_state["migration_status"]["phase"] == "executing"
    
    def test_start_migration_backup_failure(self, migration_service, sample_data_structure):
        """Test migration start with backup failure."""
        with patch.object(migration_service, 'create_backup', return_value=False):
            result = migration_service.start_migration()
            
            assert result is False
            assert migration_service.migration_state["migration_status"]["phase"] == "planning"
    
    def test_migrate_case_documents_success(self, migration_service, sample_data_structure):
        """Test successful case documents migration."""
        result = migration_service.migrate_case_documents()
        
        assert result is True
        assert (migration_service.data_root / "cases").exists()
        assert (migration_service.data_root / "cases" / "case_documents_index.json").exists()
        assert "migrate_case_documents" in migration_service.migration_state["migration_status"]["steps_completed"]
        
        # Check path mappings were created
        assert len(migration_service.migration_state["path_mappings"]) > 0
    
    def test_migrate_case_documents_no_source(self, migration_service, temp_data_dir):
        """Test case documents migration when source doesn't exist."""
        result = migration_service.migrate_case_documents()
        
        assert result is True  # Should succeed even if source doesn't exist
    
    def test_merge_analysis_data_success(self, migration_service, sample_data_structure):
        """Test successful analysis data merge."""
        result = migration_service.merge_analysis_data()
        
        assert result is True
        assert (migration_service.data_root / "analysis").exists()
        assert (migration_service.data_root / "analysis" / "case_analysis.json").exists()
        
        # Check merged data
        with open(migration_service.data_root / "analysis" / "case_analysis.json", 'r') as f:
            merged_data = json.load(f)
            assert "doc1" in merged_data
            assert "doc2" in merged_data
            assert merged_data["doc1"]["source"] == "ai"
            assert merged_data["doc2"]["source"] == "al"
        
        assert "merge_analysis_data" in migration_service.migration_state["migration_status"]["steps_completed"]
    
    def test_merge_analysis_data_conflicts(self, migration_service, sample_data_structure):
        """Test analysis data merge with conflicts."""
        # Create conflicting data
        ai_analysis = {"doc1": {"analysis": "AI analysis", "confidence": 0.9}}
        al_analysis = {"doc1": {"analysis": "AL analysis", "confidence": 0.8}}
        
        with open(migration_service.data_root / "ai" / "case_documents" / "case_documents_analysis.json", 'w') as f:
            json.dump(ai_analysis, f)
        with open(migration_service.data_root / "al" / "case_documents" / "documents_analysis.json", 'w') as f:
            json.dump(al_analysis, f)
        
        result = migration_service.merge_analysis_data()
        
        assert result is True
        
        # Check that conflict was resolved
        with open(migration_service.data_root / "analysis" / "case_analysis.json", 'r') as f:
            merged_data = json.load(f)
            assert merged_data["doc1"]["source"] == "merged"
    
    def test_merge_analysis_data_no_sources(self, migration_service, temp_data_dir):
        """Test analysis data merge when no source directories exist."""
        result = migration_service.merge_analysis_data()
        
        assert result is True
        assert (migration_service.data_root / "analysis").exists()
        assert (migration_service.data_root / "analysis" / "case_analysis.json").exists()
        
        # Check empty merged data
        with open(migration_service.data_root / "analysis" / "case_analysis.json", 'r') as f:
            merged_data = json.load(f)
            assert merged_data == {}
    
    def test_rollback_migration_success(self, migration_service, sample_data_structure):
        """Test successful migration rollback."""
        # First create backup and migrate
        migration_service.create_backup()
        migration_service.migrate_case_documents()
        
        result = migration_service.rollback_migration()
        
        assert result is True
        assert migration_service.migration_state["migration_status"]["phase"] == "rolled_back"
        assert migration_service.migration_state["migration_status"]["completed"] is not None
        
        # Check that new directories were removed
        assert not (migration_service.data_root / "cases").exists()
        assert not (migration_service.data_root / "analysis").exists()
        
        # Check that original structure was restored
        assert (migration_service.data_root / "case_documents").exists()
    
    def test_rollback_migration_no_backup(self, migration_service):
        """Test rollback when no backup is available."""
        result = migration_service.rollback_migration()
        
        assert result is False
    
    def test_complete_migration_success(self, migration_service, sample_data_structure):
        """Test successful migration completion."""
        with patch.object(migration_service.validator, 'validate_migration_integrity', return_value=True):
            result = migration_service.complete_migration()
            
            assert result is True
            assert migration_service.migration_state["migration_status"]["phase"] == "complete"
            assert migration_service.migration_state["migration_status"]["completed"] is not None
    
    def test_complete_migration_validation_failure(self, migration_service, sample_data_structure):
        """Test migration completion with validation failure."""
        with patch.object(migration_service.validator, 'validate_migration_integrity', return_value=False):
            result = migration_service.complete_migration()
            
            assert result is False
    
    def test_get_migration_status(self, migration_service):
        """Test getting migration status."""
        status = migration_service.get_migration_status()
        
        assert isinstance(status, dict)
        assert "migration_status" in status
        assert "path_mappings" in status
        assert "backup_location" in status
        
        # Ensure it's a copy, not the original
        status["test"] = "value"
        assert "test" not in migration_service.migration_state
    
    def test_save_migration_state(self, migration_service):
        """Test saving migration state to file."""
        migration_service.migration_state["test"] = "value"
        migration_service._save_migration_state()
        
        assert migration_service.migration_log_file.exists()
        
        with open(migration_service.migration_log_file, 'r') as f:
            saved_state = json.load(f)
            assert saved_state["test"] == "value"
    
    def test_load_migration_state(self, migration_service):
        """Test loading migration state from file."""
        # Create a migration log file
        test_state = {"migration_status": {"phase": "test"}, "path_mappings": {"test": "path"}}
        with open(migration_service.migration_log_file, 'w') as f:
            json.dump(test_state, f)
        
        migration_service._load_migration_state()
        
        assert migration_service.migration_state["migration_status"]["phase"] == "test"
        assert migration_service.migration_state["path_mappings"]["test"] == "path"
    
    def test_save_migration_state_exception(self, migration_service):
        """Test saving migration state with exception."""
        with patch('builtins.open', side_effect=Exception("Test exception")):
            # Should not raise exception
            migration_service._save_migration_state()
    
    def test_load_migration_state_exception(self, migration_service):
        """Test loading migration state with exception."""
        with patch('builtins.open', side_effect=Exception("Test exception")):
            # Should not raise exception
            migration_service._load_migration_state()
    
    def test_load_migration_state_no_file(self, migration_service):
        """Test loading migration state when file doesn't exist."""
        # Should not raise exception
        migration_service._load_migration_state()
        
        # State should remain unchanged
        assert "migration_status" in migration_service.migration_state