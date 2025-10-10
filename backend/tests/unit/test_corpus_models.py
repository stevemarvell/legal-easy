"""
Unit tests for Corpus models.

Tests the Pydantic models used in the corpus API including:
- CorpusItem model validation
- CorpusCategory model validation  
- CorpusSearchResult model validation
- ResearchConcept model validation
- ConceptAnalysisResult model validation
- Model serialization and deserialization
"""

import pytest
from pydantic import ValidationError
from app.models.corpus import (
    CorpusItem,
    CorpusCategory,
    CorpusMetadata,
    ResearchConcept,
    CorpusSearchResult,
    ConceptAnalysisResult
)


class TestCorpusItemModel:
    """Test CorpusItem model validation and functionality."""

    def test_corpus_item_valid_data(self):
        """Test CorpusItem creation with valid data."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template"
        }
        
        item = CorpusItem(**data)
        
        assert item.id == "rc-001"
        assert item.name == "Employment Contract Template"
        assert item.category == "contracts"
        assert "Employment Law" in item.research_areas
        assert item.content is None  # Optional field

    def test_corpus_item_with_optional_fields(self):
        """Test CorpusItem with all optional fields populated."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template",
            "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement...",
            "research_concepts": ["employment-termination", "notice-period"],
            "related_items": ["rc-004", "rc-007"],
            "metadata": {"authority": "high", "jurisdiction": "UK"}
        }
        
        item = CorpusItem(**data)
        
        assert item.content is not None
        assert len(item.research_concepts) == 2
        assert len(item.related_items) == 2
        assert item.metadata["authority"] == "high"

    def test_corpus_item_missing_required_fields(self):
        """Test CorpusItem validation with missing required fields."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template"
            # Missing required fields: filename, category, document_type, research_areas, description
        }
        
        with pytest.raises(ValidationError) as exc_info:
            CorpusItem(**data)
        
        errors = exc_info.value.errors()
        required_fields = ["filename", "category", "document_type", "research_areas", "description"]
        error_fields = [error["loc"][0] for error in errors]
        
        for field in required_fields:
            assert field in error_fields

    def test_corpus_item_empty_research_areas(self):
        """Test CorpusItem with empty research areas list."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": [],  # Empty list
            "description": "Standard UK employment contract template"
        }
        
        item = CorpusItem(**data)
        assert item.research_areas == []

    def test_corpus_item_serialization(self):
        """Test CorpusItem JSON serialization."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template"
        }
        
        item = CorpusItem(**data)
        json_data = item.model_dump()
        
        assert json_data["id"] == "rc-001"
        assert json_data["category"] == "contracts"
        assert "Employment Law" in json_data["research_areas"]


class TestCorpusCategoryModel:
    """Test CorpusCategory model validation and functionality."""

    def test_corpus_category_valid_data(self):
        """Test CorpusCategory creation with valid data."""
        data = {
            "name": "Contract Templates",
            "description": "Standard UK contract templates",
            "document_ids": ["rc-001", "rc-002", "rc-003"]
        }
        
        category = CorpusCategory(**data)
        
        assert category.name == "Contract Templates"
        assert category.description == "Standard UK contract templates"
        assert len(category.document_ids) == 3
        assert "rc-001" in category.document_ids

    def test_corpus_category_empty_document_ids(self):
        """Test CorpusCategory with empty document IDs list."""
        data = {
            "name": "Empty Category",
            "description": "Category with no documents",
            "document_ids": []
        }
        
        category = CorpusCategory(**data)
        assert category.document_ids == []

    def test_corpus_category_missing_required_fields(self):
        """Test CorpusCategory validation with missing required fields."""
        data = {
            "name": "Contract Templates"
            # Missing: description, document_ids
        }
        
        with pytest.raises(ValidationError) as exc_info:
            CorpusCategory(**data)
        
        errors = exc_info.value.errors()
        error_fields = [error["loc"][0] for error in errors]
        assert "description" in error_fields
        assert "document_ids" in error_fields


class TestCorpusMetadataModel:
    """Test CorpusMetadata model validation and functionality."""

    def test_corpus_metadata_valid_data(self):
        """Test CorpusMetadata creation with valid data."""
        data = {
            "version": "1.0",
            "created_date": "2024-01-01",
            "total_documents": 10,
            "research_jurisdiction": "United Kingdom"
        }
        
        metadata = CorpusMetadata(**data)
        
        assert metadata.version == "1.0"
        assert metadata.total_documents == 10
        assert metadata.research_jurisdiction == "United Kingdom"
        assert metadata.embedding_model is None  # Optional field

    def test_corpus_metadata_with_optional_fields(self):
        """Test CorpusMetadata with optional fields."""
        data = {
            "version": "1.0",
            "created_date": "2024-01-01",
            "total_documents": 10,
            "research_jurisdiction": "United Kingdom",
            "embedding_model": "all-MiniLM-L6-v2"
        }
        
        metadata = CorpusMetadata(**data)
        assert metadata.embedding_model == "all-MiniLM-L6-v2"


class TestResearchConceptModel:
    """Test ResearchConcept model validation and functionality."""

    def test_research_concept_valid_data(self):
        """Test ResearchConcept creation with valid data."""
        data = {
            "id": "employment-law",
            "name": "Employment Law",
            "definition": "Legal framework governing employer-employee relationships",
            "related_concepts": ["Contract Law", "Labour Rights"],
            "corpus_references": ["rc-001", "rc-007", "rc-009"]
        }
        
        concept = ResearchConcept(**data)
        
        assert concept.id == "employment-law"
        assert concept.name == "Employment Law"
        assert len(concept.related_concepts) == 2
        assert len(concept.corpus_references) == 3
        assert "Contract Law" in concept.related_concepts

    def test_research_concept_empty_lists(self):
        """Test ResearchConcept with empty lists."""
        data = {
            "id": "isolated-concept",
            "name": "Isolated Concept",
            "definition": "A concept with no relationships",
            "related_concepts": [],
            "corpus_references": []
        }
        
        concept = ResearchConcept(**data)
        assert concept.related_concepts == []
        assert concept.corpus_references == []

    def test_research_concept_missing_required_fields(self):
        """Test ResearchConcept validation with missing required fields."""
        data = {
            "id": "employment-law",
            "name": "Employment Law"
            # Missing: definition, related_concepts, corpus_references
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ResearchConcept(**data)
        
        errors = exc_info.value.errors()
        error_fields = [error["loc"][0] for error in errors]
        required_fields = ["definition", "related_concepts", "corpus_references"]
        
        for field in required_fields:
            assert field in error_fields


class TestCorpusSearchResultModel:
    """Test CorpusSearchResult model validation and functionality."""

    def test_corpus_search_result_valid_data(self):
        """Test CorpusSearchResult creation with valid data."""
        corpus_item = CorpusItem(
            id="rc-001",
            name="Employment Contract Template",
            filename="rc-001_employment_template.txt",
            category="contracts",
            document_type="Contract Template",
            research_areas=["Employment Law"],
            description="Standard UK employment contract template"
        )
        
        data = {
            "items": [corpus_item],
            "total_count": 1,
            "query": "employment",
            "categories_found": ["contracts"],
            "research_areas_found": ["Employment Law"]
        }
        
        result = CorpusSearchResult(**data)
        
        assert len(result.items) == 1
        assert result.total_count == 1
        assert result.query == "employment"
        assert "contracts" in result.categories_found
        assert "Employment Law" in result.research_areas_found

    def test_corpus_search_result_empty_results(self):
        """Test CorpusSearchResult with empty results."""
        data = {
            "items": [],
            "total_count": 0,
            "query": "nonexistent",
            "categories_found": [],
            "research_areas_found": []
        }
        
        result = CorpusSearchResult(**data)
        assert len(result.items) == 0
        assert result.total_count == 0

    def test_corpus_search_result_multiple_items(self):
        """Test CorpusSearchResult with multiple items."""
        items = [
            CorpusItem(
                id=f"rc-00{i}",
                name=f"Document {i}",
                filename=f"doc{i}.txt",
                category="contracts",
                document_type="Contract Template",
                research_areas=["Employment Law"],
                description=f"Description {i}"
            )
            for i in range(1, 4)
        ]
        
        data = {
            "items": items,
            "total_count": 3,
            "query": "contract",
            "categories_found": ["contracts"],
            "research_areas_found": ["Employment Law"]
        }
        
        result = CorpusSearchResult(**data)
        assert len(result.items) == 3
        assert result.total_count == 3


class TestConceptAnalysisResultModel:
    """Test ConceptAnalysisResult model validation and functionality."""

    def test_concept_analysis_result_valid_data(self):
        """Test ConceptAnalysisResult creation with valid data."""
        concepts = [
            ResearchConcept(
                id="employment-law",
                name="Employment Law",
                definition="Legal framework governing employer-employee relationships",
                related_concepts=["Contract Law"],
                corpus_references=["rc-001", "rc-007"]
            ),
            ResearchConcept(
                id="contract-law",
                name="Contract Law",
                definition="Legal principles governing contracts",
                related_concepts=["Employment Law"],
                corpus_references=["rc-002", "rc-008"]
            )
        ]
        
        data = {
            "concepts": concepts,
            "total_concepts": 2,
            "categories_analyzed": ["contracts", "clauses", "precedents"],
            "research_areas": ["Employment Law", "Contract Law"]
        }
        
        result = ConceptAnalysisResult(**data)
        
        assert len(result.concepts) == 2
        assert result.total_concepts == 2
        assert len(result.categories_analyzed) == 3
        assert "Employment Law" in result.research_areas

    def test_concept_analysis_result_empty_concepts(self):
        """Test ConceptAnalysisResult with empty concepts."""
        data = {
            "concepts": [],
            "total_concepts": 0,
            "categories_analyzed": [],
            "research_areas": []
        }
        
        result = ConceptAnalysisResult(**data)
        assert len(result.concepts) == 0
        assert result.total_concepts == 0


class TestModelSerialization:
    """Test model serialization and deserialization."""

    def test_corpus_item_round_trip_serialization(self):
        """Test CorpusItem serialization and deserialization."""
        original_data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template",
            "content": "Contract content here...",
            "research_concepts": ["employment-termination"],
            "related_items": ["rc-004"],
            "metadata": {"authority": "high"}
        }
        
        # Create model instance
        item = CorpusItem(**original_data)
        
        # Serialize to dict
        serialized = item.model_dump()
        
        # Deserialize back to model
        deserialized = CorpusItem(**serialized)
        
        # Verify data integrity
        assert deserialized.id == original_data["id"]
        assert deserialized.name == original_data["name"]
        assert deserialized.content == original_data["content"]
        assert deserialized.metadata == original_data["metadata"]

    def test_corpus_search_result_json_serialization(self):
        """Test CorpusSearchResult JSON serialization."""
        corpus_item = CorpusItem(
            id="rc-001",
            name="Test Document",
            filename="test.txt",
            category="contracts",
            document_type="Contract Template",
            research_areas=["Test Law"],
            description="Test description"
        )
        
        search_result = CorpusSearchResult(
            items=[corpus_item],
            total_count=1,
            query="test",
            categories_found=["contracts"],
            research_areas_found=["Test Law"]
        )
        
        # Test JSON serialization
        json_data = search_result.model_dump()
        
        assert json_data["total_count"] == 1
        assert json_data["query"] == "test"
        assert len(json_data["items"]) == 1
        assert json_data["items"][0]["id"] == "rc-001"

    def test_model_validation_with_extra_fields(self):
        """Test model behavior with extra fields."""
        data = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template",
            "extra_field": "This should be ignored"  # Extra field
        }
        
        # Should create successfully, ignoring extra field
        item = CorpusItem(**data)
        assert item.id == "rc-001"
        assert not hasattr(item, "extra_field")


class TestModelEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_corpus_item_very_long_strings(self):
        """Test CorpusItem with very long strings."""
        long_string = "x" * 10000
        
        data = {
            "id": "rc-001",
            "name": long_string,
            "filename": "test.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": long_string,
            "content": long_string
        }
        
        item = CorpusItem(**data)
        assert len(item.name) == 10000
        assert len(item.description) == 10000
        assert len(item.content) == 10000

    def test_corpus_item_special_characters(self):
        """Test CorpusItem with special characters."""
        data = {
            "id": "rc-001",
            "name": "Contract with Special Chars: àáâãäåæçèéêë",
            "filename": "contract_special.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Description with symbols: @#$%^&*()_+-=[]{}|;':\",./<>?"
        }
        
        item = CorpusItem(**data)
        assert "àáâãäåæçèéêë" in item.name
        assert "@#$%^&*()_+-=" in item.description

    def test_research_concept_with_many_references(self):
        """Test ResearchConcept with large number of references."""
        many_refs = [f"rc-{i:03d}" for i in range(1, 101)]  # 100 references
        
        data = {
            "id": "popular-concept",
            "name": "Popular Concept",
            "definition": "A concept referenced by many documents",
            "related_concepts": ["concept-1", "concept-2"],
            "corpus_references": many_refs
        }
        
        concept = ResearchConcept(**data)
        assert len(concept.corpus_references) == 100
        assert "rc-001" in concept.corpus_references
        assert "rc-100" in concept.corpus_references