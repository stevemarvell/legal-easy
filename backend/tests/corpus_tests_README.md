# Corpus API Unit Tests

This directory contains comprehensive unit tests for the Research Corpus API functionality.

## Test Files

### 📋 `test_corpus_api.py`
Tests the FastAPI endpoints for the corpus API:
- **Corpus Browsing**: Browse all items, filter by category
- **Categories**: Get all categories with metadata
- **Item Retrieval**: Get specific corpus items with content
- **Search**: Search with query, category, and research area filters
- **Research Concepts**: Get legal concept analysis
- **Related Materials**: Find related corpus items
- **Error Handling**: Proper HTTP error responses
- **Integration**: Endpoint registration and response formats

### 🔧 `test_data_service_corpus.py`
Tests the DataService corpus methods:
- **Data Loading**: Load corpus by category, categories, individual items
- **Search**: Text-based corpus search functionality
- **Research Areas**: Get available research areas
- **Related Items**: Find related corpus items based on shared areas
- **Metadata**: Load corpus metadata and statistics
- **Error Handling**: Graceful error handling for missing files

### 📊 `test_corpus_models.py`
Tests the Pydantic models used in the corpus API:
- **CorpusItem**: Validation, optional fields, serialization
- **CorpusCategory**: Category structure validation
- **CorpusMetadata**: Metadata model validation
- **ResearchConcept**: Concept model validation
- **Search Results**: Search result models validation
- **Edge Cases**: Long strings, special characters, large datasets
- **Serialization**: JSON serialization/deserialization

### 🔗 `test_corpus_integration.py`
Integration tests with real data:
- **End-to-End**: Full API workflow with actual data files
- **Data Consistency**: Verify data integrity across endpoints
- **Performance**: Basic response time testing
- **Real Data**: Tests with actual research corpus files

## Running Tests

### Run All Corpus Tests
```bash
# Using the test runner script
python run_corpus_tests.py

# Using pytest directly
python -m pytest tests/unit/test_corpus_*.py tests/integration/test_corpus_integration.py
```

### Run Specific Test Categories
```bash
# API tests only
python -m pytest tests/unit/test_corpus_api.py -v

# Model tests only
python -m pytest tests/unit/test_corpus_models.py -v

# DataService tests only
python -m pytest tests/unit/test_data_service_corpus.py -v

# Integration tests only
python -m pytest tests/integration/test_corpus_integration.py -v
```

### Run with Coverage
```bash
# Generate coverage report
python run_corpus_tests.py --coverage

# Or with pytest directly
python -m pytest tests/unit/test_corpus_*.py \
  --cov=app.api.corpus \
  --cov=app.services.data_service \
  --cov=app.models.corpus \
  --cov-report=html:htmlcov/corpus
```

### Run Specific Tests
```bash
# Single test method
python -m pytest tests/unit/test_corpus_api.py::TestCorpusBrowsing::test_browse_all_corpus_items -v

# Single test class
python -m pytest tests/unit/test_corpus_models.py::TestCorpusItemModel -v

# Tests matching pattern
python -m pytest -k "search" -v
```

## Test Structure

### Mocking Strategy
- **API Tests**: Mock DataService methods to isolate API logic
- **DataService Tests**: Mock file system operations to test data processing
- **Model Tests**: Direct Pydantic validation testing
- **Integration Tests**: Use real data files when available

### Test Data
- **Mock Data**: Realistic test data matching actual corpus structure
- **Edge Cases**: Empty results, missing files, invalid data
- **Error Conditions**: File not found, JSON parsing errors, validation failures

### Assertions
- **Response Codes**: Proper HTTP status codes
- **Data Structure**: Correct response format and required fields
- **Business Logic**: Search filtering, categorization, relationships
- **Error Messages**: Meaningful error messages for failures

## Test Coverage

The tests cover:
- ✅ All API endpoints (GET /api/corpus/*)
- ✅ All DataService corpus methods
- ✅ All Pydantic models and validation
- ✅ Error handling and edge cases
- ✅ Data consistency and integrity
- ✅ Performance characteristics
- ✅ Integration with real data

## Dependencies

Tests require:
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `fastapi[all]` - FastAPI framework
- `pydantic` - Data validation

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 5 seconds for unit tests)
- No external dependencies
- Comprehensive error reporting
- Coverage metrics generation

## Troubleshooting

### Common Issues

**Import Errors**: Ensure you're running from the backend directory
```bash
cd backend
python -m pytest tests/unit/test_corpus_api.py
```

**Missing Data**: Integration tests may skip if corpus data files don't exist
```bash
# Check if data files exist
ls data/research_corpus/research_corpus_index.json
```

**Pydantic Warnings**: Deprecation warnings are expected and don't affect test results

**Path Issues**: Use relative paths from backend directory
```bash
# Correct
python -m pytest tests/unit/test_corpus_models.py

# Incorrect (from wrong directory)
python -m pytest backend/tests/unit/test_corpus_models.py
```

## Contributing

When adding new corpus functionality:
1. Add corresponding unit tests
2. Update integration tests if needed
3. Ensure all tests pass
4. Maintain test coverage above 90%
5. Add docstrings for test methods