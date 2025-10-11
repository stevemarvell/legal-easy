#!/usr/bin/env python3
"""
Unit tests for DataService
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from app.services.data_service import DataService


class TestDataService:
    """Test cases for DataService"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"cases": [{"id": "case1", "title": "Test Case"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_object_format(self, mock_exists, mock_file):
        """Test loading cases from object format"""
        result = DataService.load_cases()
        
        assert len(result) == 1
        assert result[0]["id"] == "case1"
        assert result[0]["title"] == "Test Case"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case1", "title": "Test Case"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_array_format(self, mock_exists, mock_file):
        """Test loading cases from array format"""
        result = DataService.load_cases()
        
        assert len(result) == 1
        assert result[0]["id"] == "case1"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_cases_file_not_exists(self, mock_exists):
        """Test loading cases when file doesn't exist"""
        result = DataService.load_cases()
        
        assert result == []

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_exception(self, mock_exists, mock_file):
        """Test loading cases with exception"""
        result = DataService.load_cases()
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='{"case_documents": [{"id": "doc1", "case_id": "case1"}, {"id": "doc2", "case_id": "case2"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_case_documents_success(self, mock_exists, mock_file):
        """Test loading case documents for specific case"""
        case_id = "case1"
        
        result = DataService.load_case_documents(case_id)
        
        assert len(result) == 1
        assert result[0]["id"] == "doc1"
        assert result[0]["case_id"] == "case1"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_case_documents_file_not_exists(self, mock_exists):
        """Test loading case documents when file doesn't exist"""
        result = DataService.load_case_documents("case1")
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_document_content_success(self, mock_exists, mock_file):
        """Test loading document content successfully"""
        # Mock the index file
        index_data = {
            "case_documents": [
                {
                    "id": "doc1",
                    "full_content_path": "cases/case_documents/doc1.txt",
                    "content_preview": "Preview content"
                }
            ]
        }
        content_data = "Full document content here"
        
        def side_effect(path, *args, **kwargs):
            if "case_documents_index.json" in str(path):
                return mock_open(read_data=json.dumps(index_data)).return_value
            else:
                return mock_open(read_data=content_data).return_value
        
        mock_file.side_effect = side_effect
        mock_exists.return_value = True
        
        result = DataService.load_document_content("doc1")
        
        assert result == content_data

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_document_content_fallback_to_preview(self, mock_exists, mock_file):
        """Test loading document content falls back to preview when full content not available"""
        index_data = {
            "case_documents": [
                {
                    "id": "doc1",
                    "content_preview": "Preview content only"
                }
            ]
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(index_data)).return_value
        # Only the index file exists, not the content file
        mock_exists.return_value = True
        
        result = DataService.load_document_content("doc1")
        
        assert result == "Preview content only"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_document_content_file_not_exists(self, mock_exists):
        """Test loading document content when file doesn't exist"""
        result = DataService.load_document_content("doc1")
        
        assert result == ""

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_by_category_success(self, mock_exists, mock_file):
        """Test loading corpus by category successfully"""
        corpus_data = {
            "categories": {
                "contracts": {
                    "document_ids": ["doc1", "doc2"]
                }
            },
            "documents": {
                "doc1": {"name": "Contract 1", "category": "contracts"},
                "doc2": {"name": "Contract 2", "category": "contracts"}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(corpus_data)).return_value
        
        result = DataService.load_corpus_by_category("contracts")
        
        assert len(result) == 2
        assert result[0]["id"] == "doc1"
        assert result[0]["name"] == "Contract 1"
        assert result[1]["id"] == "doc2"

    @patch("builtins.open", new_callable=mock_open, read_data='{"categories": {}, "documents": {}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_by_category_invalid_category(self, mock_exists, mock_file):
        """Test loading corpus by invalid category"""
        result = DataService.load_corpus_by_category("invalid_category")
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "name": "Test Playbook"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_playbooks_success(self, mock_exists, mock_file):
        """Test loading playbooks successfully"""
        result = DataService.load_playbooks()
        
        assert len(result) == 1
        assert result[0]["id"] == "pb1"
        assert result[0]["name"] == "Test Playbook"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "pb1", "name": "Test Playbook"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_playbooks_array_format(self, mock_exists, mock_file):
        """Test loading playbooks in array format"""
        result = DataService.load_playbooks()
        
        assert len(result) == 1
        assert result[0]["id"] == "pb1"

    def test_search_cases_with_query(self):
        """Test searching cases with query string"""
        with patch.object(DataService, 'load_cases') as mock_load:
            mock_load.return_value = [
                {"id": "case1", "title": "Employment Dispute", "summary": "Wrongful termination", "client_name": "John Smith", "key_parties": ["ABC Corp"]},
                {"id": "case2", "title": "Contract Breach", "summary": "Payment issues", "client_name": "Jane Doe", "key_parties": ["XYZ Ltd"]}
            ]
            
            result = DataService.search_cases("employment")
            
            assert len(result) == 1
            assert result[0]["id"] == "case1"

    def test_search_cases_no_query(self):
        """Test searching cases without query returns all cases"""
        with patch.object(DataService, 'load_cases') as mock_load:
            mock_cases = [{"id": "case1"}, {"id": "case2"}]
            mock_load.return_value = mock_cases
            
            result = DataService.search_cases("")
            
            assert result == mock_cases

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_documents_with_query(self, mock_exists, mock_file):
        """Test searching documents with query string"""
        documents_data = {
            "case_documents": [
                {"id": "doc1", "name": "Employment Contract", "type": "contract", "content_preview": "Employment terms"},
                {"id": "doc2", "name": "Invoice", "type": "financial", "content_preview": "Payment details"}
            ]
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(documents_data)).return_value
        
        result = DataService.search_documents("employment")
        
        assert len(result) == 1
        assert result[0]["id"] == "doc1"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_corpus_with_query(self, mock_exists, mock_file):
        """Test searching corpus with query string"""
        corpus_data = {
            "documents": {
                "doc1": {"title": "Employment Law", "description": "Employment regulations", "research_areas": ["employment"]},
                "doc2": {"title": "Contract Law", "description": "Contract principles", "research_areas": ["contracts"]}
            }
        }
        
        # Mock both corpus index and concepts files
        def side_effect(path, *args, **kwargs):
            if "research_corpus_index.json" in str(path):
                return mock_open(read_data=json.dumps(corpus_data)).return_value
            elif "research_concepts.json" in str(path):
                return mock_open(read_data='{"legal_concepts": {}}').return_value
            return mock_open(read_data="{}").return_value
        
        mock_file.side_effect = side_effect
        
        result = DataService.search_corpus("employment")
        
        assert len(result) == 1
        assert result[0]["id"] == "doc1"
        assert result[0]["title"] == "Employment Law"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_corpus_no_query_returns_all(self, mock_exists, mock_file):
        """Test searching corpus without query returns all documents"""
        corpus_data = {
            "documents": {
                "doc1": {"name": "Doc 1"},
                "doc2": {"name": "Doc 2"}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(corpus_data)).return_value
        
        result = DataService.search_corpus("")
        
        assert len(result) == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_categories_success(self, mock_exists, mock_file):
        """Test loading corpus categories successfully"""
        corpus_data = {
            "categories": {
                "contracts": {"name": "Contracts", "document_ids": ["doc1"]},
                "statutes": {"name": "Statutes", "document_ids": ["doc2"]}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(corpus_data)).return_value
        
        result = DataService.load_corpus_categories()
        
        assert "contracts" in result
        assert "statutes" in result
        assert result["contracts"]["name"] == "Contracts"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_corpus_item_by_id_success(self, mock_exists, mock_file):
        """Test loading corpus item by ID successfully"""
        corpus_data = {
            "documents": {
                "doc1": {
                    "name": "Test Document",
                    "filename": "test.txt",
                    "category": "contracts"
                }
            }
        }
        content_data = "Full document content"
        
        def side_effect(path, *args, **kwargs):
            if "research_corpus_index.json" in str(path):
                return mock_open(read_data=json.dumps(corpus_data)).return_value
            else:
                return mock_open(read_data=content_data).return_value
        
        mock_file.side_effect = side_effect
        mock_exists.return_value = True
        
        result = DataService.load_corpus_item_by_id("doc1")
        
        assert result is not None
        assert result["id"] == "doc1"
        assert result["name"] == "Test Document"
        assert result["content"] == content_data

    @patch("builtins.open", new_callable=mock_open, read_data='{"documents": {}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_item_by_id_not_found(self, mock_exists, mock_file):
        """Test loading corpus item by ID when item not found"""
        result = DataService.load_corpus_item_by_id("nonexistent")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_metadata_success(self, mock_exists, mock_file):
        """Test loading corpus metadata successfully"""
        corpus_data = {
            "corpus_metadata": {
                "version": "1.0",
                "last_updated": "2024-01-01"
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(corpus_data)).return_value
        
        result = DataService.load_corpus_metadata()
        
        assert result["version"] == "1.0"
        assert result["last_updated"] == "2024-01-01"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_corpus_research_areas_success(self, mock_exists, mock_file):
        """Test getting corpus research areas successfully"""
        corpus_data = {
            "research_areas": ["employment", "contracts", "torts"]
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(corpus_data)).return_value
        
        result = DataService.get_corpus_research_areas()
        
        assert result == ["employment", "contracts", "torts"]

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_related_corpus_items_success(self, mock_exists, mock_file):
        """Test getting related corpus items successfully"""
        corpus_data = {
            "documents": {
                "doc1": {
                    "name": "Employment Law",
                    "research_areas": ["employment", "labor"],
                    "category": "statutes"
                },
                "doc2": {
                    "name": "Labor Relations",
                    "research_areas": ["employment", "unions"],
                    "category": "statutes"
                },
                "doc3": {
                    "name": "Contract Law",
                    "research_areas": ["contracts"],
                    "category": "statutes"
                }
            }
        }
        
        def side_effect(path, *args, **kwargs):
            return mock_open(read_data=json.dumps(corpus_data)).return_value
        
        mock_file.side_effect = side_effect
        
        result = DataService.get_related_corpus_items("doc1")
        
        assert len(result) > 0
        # Should find doc2 as related (shared employment research area and same category)
        related_ids = [item["id"] for item in result]
        assert "doc2" in related_ids
        # Should have relevance scores
        assert all("relevance_score" in item for item in result)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_documentation_categories_success(self, mock_exists, mock_file):
        """Test loading documentation categories successfully"""
        docs_data = {
            "categories": {
                "api": {"name": "API Documentation", "document_ids": ["api1"]},
                "guides": {"name": "User Guides", "document_ids": ["guide1"]}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(docs_data)).return_value
        
        result = DataService.load_documentation_categories()
        
        assert "api" in result
        assert "guides" in result

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_documentation_by_category_success(self, mock_exists, mock_file):
        """Test loading documentation by category successfully"""
        docs_data = {
            "categories": {
                "api": {"document_ids": ["doc1", "doc2"]}
            },
            "documents": {
                "doc1": {"name": "API Guide 1"},
                "doc2": {"name": "API Guide 2"}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(docs_data)).return_value
        
        result = DataService.load_documentation_by_category("api")
        
        assert len(result) == 2
        assert result[0]["id"] == "doc1"
        assert result[1]["id"] == "doc2"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_documentation_item_by_id_success(self, mock_exists, mock_file):
        """Test loading documentation item by ID successfully"""
        docs_data = {
            "documents": {
                "doc1": {
                    "name": "Test Doc",
                    "filename": "test.md"
                }
            }
        }
        content_data = "# Test Documentation\nContent here"
        
        def side_effect(path, *args, **kwargs):
            if "documentation_index.json" in str(path):
                return mock_open(read_data=json.dumps(docs_data)).return_value
            else:
                return mock_open(read_data=content_data).return_value
        
        mock_file.side_effect = side_effect
        mock_exists.return_value = True
        
        result = DataService.load_documentation_item_by_id("doc1")
        
        assert result is not None
        assert result["id"] == "doc1"
        assert result["content"] == content_data

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_documentation_with_query(self, mock_exists, mock_file):
        """Test searching documentation with query"""
        docs_data = {
            "documents": {
                "doc1": {
                    "name": "API Documentation",
                    "description": "REST API guide",
                    "tags": ["api", "rest"]
                },
                "doc2": {
                    "name": "User Guide",
                    "description": "How to use the system",
                    "tags": ["guide", "tutorial"]
                }
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(docs_data)).return_value
        
        result = DataService.search_documentation("api")
        
        assert len(result) == 1
        assert result[0]["id"] == "doc1"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_json_schemas_success(self, mock_exists, mock_file):
        """Test loading JSON schemas successfully"""
        docs_data = {
            "schemas": {
                "case": {"type": "object", "properties": {}},
                "document": {"type": "object", "properties": {}}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(docs_data)).return_value
        
        result = DataService.load_json_schemas()
        
        assert "case" in result
        assert "document" in result

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_all_documentation_tags_success(self, mock_exists, mock_file):
        """Test getting all documentation tags successfully"""
        docs_data = {
            "documents": {
                "doc1": {"tags": ["api", "rest"]},
                "doc2": {"tags": ["guide", "api"]},
                "doc3": {"tags": ["tutorial"]}
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(docs_data)).return_value
        
        result = DataService.get_all_documentation_tags()
        
        expected_tags = ["api", "guide", "rest", "tutorial"]
        assert sorted(result) == sorted(expected_tags)

    def test_data_service_initialization(self):
        """Test DataService initialization with custom data root"""
        service = DataService("custom_data")
        
        assert service.data_root == Path("custom_data")
        assert service.cases_path == Path("custom_data/cases")
        assert service.research_corpus_path == Path("custom_data/research_corpus")
        assert service.playbooks_path == Path("custom_data/playbooks")

    def test_data_service_default_initialization(self):
        """Test DataService initialization with default data root"""
        service = DataService()
        
        assert service.data_root == Path("data")

    @patch("builtins.open", side_effect=Exception("JSON decode error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_error_handling_in_search_methods(self, mock_exists, mock_file):
        """Test error handling in search methods"""
        # Test that search methods return empty lists on errors
        assert DataService.search_cases("test") == []
        assert DataService.search_documents("test") == []
        assert DataService.search_corpus("test") == []
        assert DataService.search_documentation("test") == []

    # === CORPUS CONCEPT ANALYSIS TESTS ===

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_legal_concepts_success(self, mock_exists, mock_file):
        """Test loading legal concepts successfully"""
        concepts_data = {
            "legal_concepts": {
                "lc-001": {
                    "name": "Employment Termination",
                    "definition": "The legal process of ending employment",
                    "related_concepts": ["lc-002"],
                    "corpus_references": ["rc-001"]
                }
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(concepts_data)).return_value
        
        result = DataService.load_legal_concepts()
        
        assert "lc-001" in result
        assert result["lc-001"]["name"] == "Employment Termination"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_concept_relationships_success(self, mock_exists, mock_file):
        """Test loading concept relationships successfully"""
        concepts_data = {
            "concept_relationships": {
                "employment_cluster": {
                    "concepts": ["lc-001", "lc-002"],
                    "description": "Employment law concepts"
                }
            }
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(concepts_data)).return_value
        
        result = DataService.load_concept_relationships()
        
        assert "employment_cluster" in result
        assert result["employment_cluster"]["description"] == "Employment law concepts"

    @patch.object(DataService, 'load_corpus_item_by_id')
    @patch.object(DataService, 'load_legal_concepts')
    def test_get_concepts_for_corpus_item_success(self, mock_load_concepts, mock_load_item):
        """Test getting concepts for corpus item successfully"""
        mock_load_item.return_value = {
            "id": "rc-001",
            "legal_concepts": ["lc-001", "lc-002"]
        }
        
        mock_load_concepts.return_value = {
            "lc-001": {"name": "Concept 1", "definition": "Definition 1"},
            "lc-002": {"name": "Concept 2", "definition": "Definition 2"}
        }
        
        result = DataService.get_concepts_for_corpus_item("rc-001")
        
        assert len(result) == 2
        assert result[0]["id"] == "lc-001"
        assert result[1]["id"] == "lc-002"

    @patch.object(DataService, 'load_legal_concepts')
    def test_extract_concepts_from_text_success(self, mock_load_concepts):
        """Test extracting concepts from text successfully"""
        mock_load_concepts.return_value = {
            "lc-001": {
                "name": "Employment Termination",
                "definition": "The legal process of ending employment relationship"
            },
            "lc-002": {
                "name": "Contract Breach",
                "definition": "Failure to perform contractual obligations"
            }
        }
        
        text = "This document discusses employment termination procedures and contract obligations."
        
        result = DataService.extract_concepts_from_text(text)
        
        assert "lc-001" in result  # Should find "employment termination"

    def test_extract_concepts_from_empty_text(self):
        """Test extracting concepts from empty text"""
        result = DataService.extract_concepts_from_text("")
        
        assert result == []

    def test_extract_key_terms_from_definition(self):
        """Test extracting key terms from concept definition"""
        definition = "The legal process of ending an employment relationship with proper notice"
        
        result = DataService._extract_key_terms_from_definition(definition)
        
        assert "legal" in result
        assert "employment" in result
        assert "notice" in result

    @patch.object(DataService, 'load_legal_concepts')
    @patch.object(DataService, 'load_concept_relationships')
    def test_analyze_concept_relationships_success(self, mock_load_relationships, mock_load_concepts):
        """Test analyzing concept relationships successfully"""
        mock_load_concepts.return_value = {
            "lc-001": {
                "name": "Employment Termination",
                "definition": "Legal process of ending employment",
                "related_concepts": ["lc-002"],
                "corpus_references": ["rc-001"]
            },
            "lc-002": {
                "name": "Notice Period",
                "definition": "Required advance notice",
                "related_concepts": ["lc-001"],
                "corpus_references": ["rc-001"]
            }
        }
        
        mock_load_relationships.return_value = {
            "employment_cluster": {
                "concepts": ["lc-001", "lc-002"],
                "description": "Employment law concepts"
            }
        }
        
        result = DataService.analyze_concept_relationships("lc-001")
        
        assert result["concept_id"] == "lc-001"
        assert result["concept_name"] == "Employment Termination"
        assert len(result["related_concepts"]) == 1
        assert len(result["concept_clusters"]) == 1
        assert result["relationship_strength"] == 1

    @patch.object(DataService, 'load_legal_concepts')
    def test_build_concept_relationship_map_success(self, mock_load_concepts):
        """Test building concept relationship map successfully"""
        mock_load_concepts.return_value = {
            "lc-001": {"related_concepts": ["lc-002", "lc-003"]},
            "lc-002": {"related_concepts": ["lc-001"]},
            "lc-003": {"related_concepts": ["lc-001"]}
        }
        
        result = DataService.build_concept_relationship_map()
        
        assert "lc-001" in result
        assert result["lc-001"] == ["lc-002", "lc-003"]
        assert result["lc-002"] == ["lc-001"]

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_update_concept_analysis_success(self, mock_exists, mock_file):
        """Test updating concept analysis successfully"""
        existing_data = {
            "legal_concepts": {
                "lc-001": {
                    "name": "Employment Termination",
                    "definition": "Original definition"
                }
            },
            "concepts_metadata": {
                "last_updated": "2024-01-01"
            }
        }
        
        # Mock reading existing data
        mock_file.return_value = mock_open(read_data=json.dumps(existing_data)).return_value
        
        update_data = {"definition": "Updated definition"}
        
        result = DataService.update_concept_analysis("lc-001", update_data)
        
        assert result is True

    @patch("pathlib.Path.exists", return_value=False)
    def test_update_concept_analysis_file_not_exists(self, mock_exists):
        """Test updating concept analysis when file doesn't exist"""
        result = DataService.update_concept_analysis("lc-001", {})
        
        assert result is False

    @patch.object(DataService, 'load_corpus_item_by_id')
    @patch.object(DataService, 'extract_concepts_from_text')
    @patch.object(DataService, 'load_legal_concepts')
    def test_analyze_corpus_item_concepts_success(self, mock_load_concepts, mock_extract, mock_load_item):
        """Test analyzing corpus item concepts successfully"""
        mock_load_item.return_value = {
            "id": "rc-001",
            "title": "Employment Contract",
            "category": "contracts",
            "content": "Employment termination procedures",
            "legal_concepts": ["lc-001"]
        }
        
        mock_extract.return_value = ["lc-002"]
        
        mock_load_concepts.return_value = {
            "lc-001": {"name": "Existing Concept", "definition": "Existing"},
            "lc-002": {"name": "Extracted Concept", "definition": "Extracted"}
        }
        
        result = DataService.analyze_corpus_item_concepts("rc-001")
        
        assert result["item_id"] == "rc-001"
        assert result["total_concepts"] == 2
        assert result["existing_concepts"] == 1
        assert result["extracted_concepts"] == 1
        assert len(result["concept_details"]) == 2

    @patch.object(DataService, 'load_corpus_item_by_id')
    def test_analyze_corpus_item_concepts_item_not_found(self, mock_load_item):
        """Test analyzing corpus item concepts when item not found"""
        mock_load_item.return_value = None
        
        result = DataService.analyze_corpus_item_concepts("nonexistent")
        
        assert result == {}

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_corpus_with_concept_matching(self, mock_exists, mock_file):
        """Test searching corpus with concept-based matching"""
        corpus_data = {
            "documents": {
                "doc1": {
                    "title": "Employment Law",
                    "description": "Employment regulations",
                    "research_areas": ["employment"],
                    "legal_concepts": ["lc-001"]
                },
                "doc2": {
                    "title": "Contract Law",
                    "description": "Contract principles",
                    "research_areas": ["contracts"],
                    "legal_concepts": ["lc-002"]
                }
            }
        }
        
        concepts_data = {
            "legal_concepts": {
                "lc-001": {
                    "name": "Employment Termination",
                    "definition": "Process of ending employment"
                },
                "lc-002": {
                    "name": "Contract Breach",
                    "definition": "Failure to perform contract"
                }
            }
        }
        
        def side_effect(path, *args, **kwargs):
            if "research_corpus_index.json" in str(path):
                return mock_open(read_data=json.dumps(corpus_data)).return_value
            elif "research_concepts.json" in str(path):
                return mock_open(read_data=json.dumps(concepts_data)).return_value
            return mock_open(read_data="{}").return_value
        
        mock_file.side_effect = side_effect
        
        result = DataService.search_corpus("termination")
        
        # Should find doc1 because "termination" matches the concept definition
        assert len(result) >= 1
        found_doc1 = any(doc["id"] == "doc1" for doc in result)
        assert found_doc1

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_content_file_success(self, mock_exists, mock_file):
        """Test loading corpus content file successfully"""
        content = "This is the full content of the legal document."
        mock_file.return_value = mock_open(read_data=content).return_value
        
        result = DataService.load_corpus_content_file("contracts", "test_contract.txt")
        
        assert result == content

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_corpus_content_file_not_exists(self, mock_exists):
        """Test loading corpus content file when file doesn't exist"""
        result = DataService.load_corpus_content_file("contracts", "nonexistent.txt")
        
        assert result == ""

    @patch("builtins.open", side_effect=Exception("File read error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_content_file_exception(self, mock_exists, mock_file):
        """Test loading corpus content file with exception"""
        result = DataService.load_corpus_content_file("contracts", "test.txt")
        
        assert result == ""

    @patch("builtins.open", side_effect=Exception("Concept error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_concept_methods_error_handling(self, mock_exists, mock_file):
        """Test error handling in concept analysis methods"""
        # Test that concept methods return empty results on errors
        assert DataService.load_legal_concepts() == {}
        assert DataService.load_concept_relationships() == {}
        assert DataService.extract_concepts_from_text("test") == []
        assert DataService.analyze_concept_relationships("lc-001") == {}
        assert DataService.build_concept_relationship_map() == {}
        assert DataService.analyze_corpus_item_concepts("rc-001") == {}

    # === CORPUS INDEX REGENERATION TESTS ===

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.is_file")
    @patch("json.dump")
    def test_regenerate_corpus_index_success(self, mock_json_dump, mock_is_file, mock_iterdir, mock_exists, mock_file):
        """Test successful corpus index regeneration"""
        # Mock directory structure
        mock_contracts_dir = MagicMock()
        mock_contracts_dir.name = "contracts"
        mock_contracts_dir.is_dir.return_value = True
        
        mock_clauses_dir = MagicMock()
        mock_clauses_dir.name = "clauses"
        mock_clauses_dir.is_dir.return_value = True
        
        # Mock files in directories
        mock_contract_file = MagicMock()
        mock_contract_file.name = "rc-001_employment_contract.txt"
        mock_contract_file.is_file.return_value = True
        mock_contract_file.suffix = ".txt"
        
        mock_clause_file = MagicMock()
        mock_clause_file.name = "rc-004_termination_clause.txt"
        mock_clause_file.is_file.return_value = True
        mock_clause_file.suffix = ".txt"
        
        # Setup directory iteration
        def iterdir_side_effect(path_obj):
            if "contracts" in str(path_obj):
                return [mock_contract_file]
            elif "clauses" in str(path_obj):
                return [mock_clause_file]
            else:
                return [mock_contracts_dir, mock_clauses_dir]
        
        mock_iterdir.side_effect = iterdir_side_effect
        mock_exists.return_value = True
        mock_is_file.return_value = True
        
        # Mock file content
        contract_content = "EMPLOYMENT CONTRACT\nThis agreement covers employment terms..."
        clause_content = "TERMINATION CLAUSE\nEither party may terminate..."
        
        def file_side_effect(path, *args, **kwargs):
            if "employment_contract" in str(path):
                return mock_open(read_data=contract_content).return_value
            elif "termination_clause" in str(path):
                return mock_open(read_data=clause_content).return_value
            else:
                return mock_open().return_value
        
        mock_file.side_effect = file_side_effect
        
        # Test regeneration
        result = DataService.regenerate_corpus_index()
        
        assert result is True
        # Verify json.dump was called to save the index
        mock_json_dump.assert_called()

    @patch("pathlib.Path.exists", return_value=False)
    def test_regenerate_corpus_index_directory_not_exists(self, mock_exists):
        """Test corpus index regeneration when corpus directory doesn't exist"""
        result = DataService.regenerate_corpus_index("nonexistent_path")
        
        assert result is False

    @patch("builtins.open", side_effect=Exception("File write error"))
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.iterdir", return_value=[])
    def test_regenerate_corpus_index_write_error(self, mock_iterdir, mock_exists, mock_file):
        """Test corpus index regeneration with file write error"""
        result = DataService.regenerate_corpus_index()
        
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.is_file")
    @patch("json.dump")
    def test_regenerate_corpus_index_extracts_metadata(self, mock_json_dump, mock_is_file, mock_iterdir, mock_exists, mock_file):
        """Test that corpus index regeneration extracts proper metadata"""
        # Mock a single file
        mock_file_obj = MagicMock()
        mock_file_obj.name = "rc-001_employment_contract.txt"
        mock_file_obj.is_file.return_value = True
        mock_file_obj.suffix = ".txt"
        
        mock_dir = MagicMock()
        mock_dir.name = "contracts"
        mock_dir.is_dir.return_value = True
        
        def iterdir_side_effect(path_obj):
            if "contracts" in str(path_obj):
                return [mock_file_obj]
            else:
                return [mock_dir]
        
        mock_iterdir.side_effect = iterdir_side_effect
        mock_is_file.return_value = True
        
        # Mock file content with employment-related terms
        file_content = """EMPLOYMENT CONTRACT
        
        This employment agreement is between ABC Company and the Employee.
        
        Terms of employment include:
        - Job responsibilities and duties
        - Compensation and benefits
        - Termination procedures
        - Confidentiality requirements
        """
        
        mock_file.return_value = mock_open(read_data=file_content).return_value
        
        # Test regeneration
        result = DataService.regenerate_corpus_index()
        
        assert result is True
        
        # Verify the structure of data passed to json.dump
        call_args = mock_json_dump.call_args
        saved_data = call_args[0][0]  # First argument to json.dump
        
        assert 'documents' in saved_data
        assert 'categories' in saved_data
        assert 'corpus_metadata' in saved_data
        
        # Check that the document was processed
        assert len(saved_data['documents']) > 0
        
        # Check document structure
        doc_id = list(saved_data['documents'].keys())[0]
        document = saved_data['documents'][doc_id]
        
        assert 'name' in document or 'title' in document
        assert 'category' in document
        assert 'filename' in document
        assert document['category'] == 'contracts'

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.is_file")
    @patch("json.dump")
    def test_regenerate_corpus_index_handles_multiple_categories(self, mock_json_dump, mock_is_file, mock_iterdir, mock_exists, mock_file):
        """Test corpus index regeneration with multiple categories"""
        # Mock files in different categories
        mock_contract_file = MagicMock()
        mock_contract_file.name = "rc-001_contract.txt"
        mock_contract_file.is_file.return_value = True
        mock_contract_file.suffix = ".txt"
        
        mock_statute_file = MagicMock()
        mock_statute_file.name = "rc-002_statute.txt"
        mock_statute_file.is_file.return_value = True
        mock_statute_file.suffix = ".txt"
        
        # Mock directories
        mock_contracts_dir = MagicMock()
        mock_contracts_dir.name = "contracts"
        mock_contracts_dir.is_dir.return_value = True
        
        mock_statutes_dir = MagicMock()
        mock_statutes_dir.name = "statutes"
        mock_statutes_dir.is_dir.return_value = True
        
        def iterdir_side_effect(path_obj):
            if "contracts" in str(path_obj):
                return [mock_contract_file]
            elif "statutes" in str(path_obj):
                return [mock_statute_file]
            else:
                return [mock_contracts_dir, mock_statutes_dir]
        
        mock_iterdir.side_effect = iterdir_side_effect
        mock_is_file.return_value = True
        
        # Mock file contents
        def file_side_effect(path, *args, **kwargs):
            if "contract" in str(path):
                return mock_open(read_data="Contract content here").return_value
            elif "statute" in str(path):
                return mock_open(read_data="Statute content here").return_value
            else:
                return mock_open().return_value
        
        mock_file.side_effect = file_side_effect
        
        # Test regeneration
        result = DataService.regenerate_corpus_index()
        
        assert result is True
        
        # Verify multiple categories were processed
        call_args = mock_json_dump.call_args
        saved_data = call_args[0][0]
        
        assert 'contracts' in saved_data['categories']
        assert 'statutes' in saved_data['categories']
        
        # Verify documents from both categories
        documents = saved_data['documents']
        categories_found = set(doc['category'] for doc in documents.values())
        assert 'contracts' in categories_found
        assert 'statutes' in categories_found  
  # === DOCUMENT ANALYSIS REGENERATION TESTS ===

    @patch.object(DataService, 'load_cases')
    @patch.object(DataService, 'load_case_documents')
    @patch.object(DataService, 'load_document_content')
    @patch('app.services.ai_service.AIService.analyze_document')
    @patch('app.services.ai_service.AIService.save_analysis')
    @patch.object(DataService, '_save_document_analysis_stats')
    def test_regenerate_document_analysis_success(self, mock_save_stats, mock_save_analysis, 
                                                mock_analyze, mock_load_content, mock_load_docs, mock_load_cases):
        """Test successful document analysis regeneration"""
        # Mock data
        mock_load_cases.return_value = [{'id': 'case-001'}]
        mock_load_docs.return_value = [{'id': 'doc-001'}, {'id': 'doc-002'}]
        mock_load_content.side_effect = ['Content 1', 'Content 2']
        mock_analyze.side_effect = [
            {'overall_confidence': 0.9, 'document_id': 'doc-001'},
            {'overall_confidence': 0.8, 'document_id': 'doc-002'}
        ]
        
        # Test regeneration
        result = DataService.regenerate_document_analysis()
        
        assert result is True
        
        # Verify calls
        mock_load_cases.assert_called_once()
        mock_load_docs.assert_called_once_with('case-001')
        assert mock_load_content.call_count == 2
        assert mock_analyze.call_count == 2
        assert mock_save_analysis.call_count == 2
        mock_save_stats.assert_called_once()

    @patch.object(DataService, 'load_cases')
    def test_regenerate_document_analysis_no_cases(self, mock_load_cases):
        """Test document analysis regeneration with no cases"""
        mock_load_cases.return_value = []
        
        result = DataService.regenerate_document_analysis()
        
        assert result is True  # Should succeed even with no cases

    @patch.object(DataService, 'load_cases')
    @patch.object(DataService, 'load_case_documents')
    @patch.object(DataService, 'load_document_content')
    @patch('app.services.ai_service.AIService.analyze_document')
    @patch('app.services.ai_service.AIService.save_analysis')
    @patch.object(DataService, '_save_document_analysis_stats')
    def test_regenerate_document_analysis_handles_failures(self, mock_save_stats, mock_save_analysis,
                                                          mock_analyze, mock_load_content, mock_load_docs, mock_load_cases):
        """Test document analysis regeneration handles individual document failures"""
        # Mock data with one failure
        mock_load_cases.return_value = [{'id': 'case-001'}]
        mock_load_docs.return_value = [{'id': 'doc-001'}, {'id': 'doc-002'}]
        mock_load_content.side_effect = ['Content 1', '']  # Second document has no content
        mock_analyze.return_value = {'overall_confidence': 0.9, 'document_id': 'doc-001'}
        
        result = DataService.regenerate_document_analysis()
        
        assert result is True
        
        # Should only analyze the first document
        assert mock_analyze.call_count == 1
        assert mock_save_analysis.call_count == 1
        
        # Should still save stats
        mock_save_stats.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_document_analysis_stats_success(self, mock_exists, mock_file):
        """Test getting document analysis statistics successfully"""
        stats_data = {
            "total_documents": 10,
            "analyzed_documents": 8,
            "failed_documents": 2,
            "average_confidence": 0.85,
            "last_regenerated": "2024-01-01T12:00:00"
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(stats_data)).return_value
        
        result = DataService.get_document_analysis_stats()
        
        assert result["total_documents"] == 10
        assert result["analyzed_documents"] == 8
        assert result["failed_documents"] == 2
        assert result["average_confidence"] == 0.85

    @patch("pathlib.Path.exists", return_value=False)
    def test_get_document_analysis_stats_no_file(self, mock_exists):
        """Test getting document analysis statistics when file doesn't exist"""
        result = DataService.get_document_analysis_stats()
        
        assert result["total_documents"] == 0
        assert result["analyzed_documents"] == 0
        assert result["failed_documents"] == 0
        assert result["average_confidence"] == 0.0

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.mkdir")
    @patch("json.dump")
    def test_save_document_analysis_stats_success(self, mock_json_dump, mock_mkdir, mock_file):
        """Test saving document analysis statistics successfully"""
        stats = {
            "total_documents": 10,
            "analyzed_documents": 8,
            "failed_documents": 2,
            "average_confidence": 0.85,
            "confidence_scores": [0.9, 0.8]  # Should be cleaned up
        }
        
        DataService._save_document_analysis_stats(stats)
        
        # Verify json.dump was called
        mock_json_dump.assert_called_once()
        
        # Verify the data structure passed to json.dump
        call_args = mock_json_dump.call_args
        saved_data = call_args[0][0]
        
        assert saved_data["total_documents"] == 10
        assert saved_data["analyzed_documents"] == 8
        assert saved_data["failed_documents"] == 2
        assert saved_data["average_confidence"] == 0.85
        assert "last_regenerated" in saved_data
        assert "confidence_scores" not in saved_data  # Should be cleaned up 
   # === DOCUMENT ANALYSIS STATUS TESTS ===

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_case_documents_adds_analysis_completed_field(self, mock_exists, mock_file):
        """Test that load_case_documents adds analysis_completed field"""
        # Mock case documents
        case_docs_data = {
            "case_documents": [
                {"id": "doc-001", "case_id": "case-001", "name": "Test Doc 1"},
                {"id": "doc-002", "case_id": "case-001", "name": "Test Doc 2"}
            ]
        }
        
        # Mock analysis data (only doc-001 has analysis)
        analysis_data = {
            "doc-001": {"document_id": "doc-001", "overall_confidence": 0.9}
        }
        
        def file_side_effect(path, *args, **kwargs):
            if "case_documents_index.json" in str(path):
                return mock_open(read_data=json.dumps(case_docs_data)).return_value
            elif "case_documents_analysis.json" in str(path):
                return mock_open(read_data=json.dumps(analysis_data)).return_value
            return mock_open(read_data="{}").return_value
        
        mock_file.side_effect = file_side_effect
        mock_exists.return_value = True
        
        # Test loading case documents
        result = DataService.load_case_documents("case-001")
        
        assert len(result) == 2
        assert result[0]["id"] == "doc-001"
        assert result[0]["analysis_completed"] is True  # Has analysis
        assert result[1]["id"] == "doc-002"
        assert result[1]["analysis_completed"] is False  # No analysis

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_has_document_analysis_success(self, mock_exists, mock_file):
        """Test _has_document_analysis method"""
        analysis_data = {
            "doc-001": {"document_id": "doc-001", "overall_confidence": 0.9},
            "doc-002": {"document_id": "doc-002", "overall_confidence": 0.8}
        }
        
        # Mock file to return the same data each time it's opened
        mock_file.side_effect = lambda *args, **kwargs: mock_open(read_data=json.dumps(analysis_data)).return_value
        mock_exists.return_value = True
        
        # Test existing analysis
        assert DataService._has_document_analysis("doc-001") is True
        assert DataService._has_document_analysis("doc-002") is True
        
        # Test non-existing analysis
        assert DataService._has_document_analysis("doc-999") is False

    @patch("pathlib.Path.exists", return_value=False)
    def test_has_document_analysis_no_file(self, mock_exists):
        """Test _has_document_analysis when analysis file doesn't exist"""
        result = DataService._has_document_analysis("doc-001")
        assert result is False

    @patch.object(DataService, 'load_document_analysis')
    def test_load_document_risks_success(self, mock_load_analysis):
        """Test loading document risks successfully"""
        mock_analysis = {
            "potential_issues": ["Risk 1", "Risk 2"],
            "risk_level": "medium",
            "confidence_scores": {"risks": 0.85}
        }
        mock_load_analysis.return_value = mock_analysis
        
        result = DataService.load_document_risks("doc-001")
        
        assert result is not None
        assert result["document_id"] == "doc-001"
        assert result["risks"] == ["Risk 1", "Risk 2"]
        assert result["risk_level"] == "medium"
        assert result["confidence_score"] == 0.85

    @patch.object(DataService, 'load_document_analysis')
    def test_load_document_compliance_success(self, mock_load_analysis):
        """Test loading document compliance successfully"""
        mock_analysis = {
            "compliance_status": "compliant",
            "compliance_issues": ["Issue 1"],
            "confidence_scores": {"compliance": 0.9}
        }
        mock_load_analysis.return_value = mock_analysis
        
        result = DataService.load_document_compliance("doc-001")
        
        assert result is not None
        assert result["document_id"] == "doc-001"
        assert result["compliance_status"] == "compliant"
        assert result["compliance_issues"] == ["Issue 1"]
        assert result["confidence_score"] == 0.9

    @patch.object(DataService, 'load_document_analysis')
    def test_load_document_deadlines_success(self, mock_load_analysis):
        """Test loading document deadlines successfully"""
        mock_analysis = {
            "critical_deadlines": [{"date": "2024-12-31", "type": "completion"}],
            "confidence_scores": {"deadlines": 0.75}
        }
        mock_load_analysis.return_value = mock_analysis
        
        result = DataService.load_document_deadlines("doc-001")
        
        assert result is not None
        assert result["document_id"] == "doc-001"
        assert result["deadlines"] == [{"date": "2024-12-31", "type": "completion"}]
        assert result["confidence_score"] == 0.75

    @patch.object(DataService, 'load_document_analysis')
    def test_analysis_methods_handle_missing_confidence_scores(self, mock_load_analysis):
        """Test that analysis methods handle missing confidence scores gracefully"""
        # Analysis without confidence_scores field
        mock_analysis = {
            "summary": "Test summary",
            "key_dates": ["2024-01-01"],
            "parties": ["Party A"],
            "risks": ["Risk 1"],
            "compliance_status": "compliant",
            "deadlines": []
        }
        mock_load_analysis.return_value = mock_analysis
        
        # All methods should handle missing confidence scores
        summary = DataService.load_document_summary("doc-001")
        assert summary["confidence_score"] == 0.0
        
        dates = DataService.load_document_key_dates("doc-001")
        assert dates["confidence_score"] == 0.0
        
        parties = DataService.load_document_parties("doc-001")
        assert parties["confidence_score"] == 0.0
        
        risks = DataService.load_document_risks("doc-001")
        assert risks["confidence_score"] == 0.0
        
        compliance = DataService.load_document_compliance("doc-001")
        assert compliance["confidence_score"] == 0.0
        
        deadlines = DataService.load_document_deadlines("doc-001")
        assert deadlines["confidence_score"] == 0.0

    @patch.object(DataService, 'load_document_analysis')
    def test_analysis_methods_handle_missing_fields(self, mock_load_analysis):
        """Test that analysis methods handle missing analysis fields gracefully"""
        # Analysis with minimal fields
        mock_analysis = {
            "document_id": "doc-001"
        }
        mock_load_analysis.return_value = mock_analysis
        
        # All methods should handle missing fields with defaults
        summary = DataService.load_document_summary("doc-001")
        assert summary["summary"] == ""
        assert summary["key_points"] == []
        
        dates = DataService.load_document_key_dates("doc-001")
        assert dates["key_dates"] == []
        
        parties = DataService.load_document_parties("doc-001")
        assert parties["parties"] == []
        
        risks = DataService.load_document_risks("doc-001")
        assert risks["risks"] == []
        assert risks["risk_level"] == "unknown"
        
        compliance = DataService.load_document_compliance("doc-001")
        assert compliance["compliance_status"] == "unknown"
        assert compliance["compliance_issues"] == []
        
        deadlines = DataService.load_document_deadlines("doc-001")
        assert deadlines["deadlines"] == []

    @patch("builtins.open", side_effect=Exception("File read error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_document_analysis_error_handling(self, mock_exists, mock_file):
        """Test that load_document_analysis handles file read errors gracefully"""
        result = DataService.load_document_analysis("doc-001")
        assert result is None

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_document_analysis_invalid_json(self, mock_exists, mock_file):
        """Test that load_document_analysis handles invalid JSON gracefully"""
        mock_file.side_effect = lambda *args, **kwargs: mock_open(read_data="invalid json").return_value
        mock_exists.return_value = True
        
        result = DataService.load_document_analysis("doc-001")
        assert result is None

    @patch.object(DataService, 'load_document_analysis', side_effect=Exception("Analysis error"))
    def test_analysis_methods_error_handling(self, mock_load_analysis):
        """Test that all analysis methods handle errors gracefully"""
        # All methods should return None when load_document_analysis raises an exception
        assert DataService.load_document_summary("doc-001") is None
        assert DataService.load_document_key_dates("doc-001") is None
        assert DataService.load_document_parties("doc-001") is None
        assert DataService.load_document_risks("doc-001") is None
        assert DataService.load_document_compliance("doc-001") is None
        assert DataService.load_document_deadlines("doc-001") is None

    def test_analysis_methods_handle_missing_analysis_gracefully(self):
        """Test that analysis loading methods handle missing analysis gracefully"""
        with patch.object(DataService, 'load_document_analysis', return_value=None):
            # Test all methods return None when no analysis exists
            assert DataService.load_document_summary("doc-999") is None
            assert DataService.load_document_key_dates("doc-999") is None
            assert DataService.load_document_parties("doc-999") is None
            assert DataService.load_document_risks("doc-999") is None
            assert DataService.load_document_compliance("doc-999") is None
            assert DataService.load_document_deadlines("doc-999") is None