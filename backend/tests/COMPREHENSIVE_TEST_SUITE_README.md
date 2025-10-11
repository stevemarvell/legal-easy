# Comprehensive API Test Suite

This directory contains a complete test suite for all API endpoints in the Legal AI System. The test suite provides comprehensive coverage including unit tests, integration tests, performance tests, and security tests.

## Test Structure

### Individual Endpoint Test Suites

1. **`test_cases_api_comprehensive.py`** - Cases API Tests
   - Case listing and retrieval
   - Case statistics
   - Comprehensive case analysis
   - Error handling and edge cases

2. **`test_documents_api_comprehensive.py`** - Documents API Tests
   - Document retrieval by case and ID
   - Document analysis (GET and POST)
   - Document content access
   - Analysis deletion
   - Real-time analysis capabilities

3. **`test_corpus_api_comprehensive.py`** - Corpus API Tests
   - Corpus browsing and category filtering
   - Corpus search functionality
   - Research concept analysis
   - Individual corpus item retrieval
   - Related materials discovery

4. **`test_docs_api_comprehensive.py`** - Documentation API Tests
   - Documentation categories and overview
   - Documentation search functionality
   - JSON schemas retrieval
   - Category-specific documentation access

5. **`test_playbooks_api_comprehensive.py`** - Playbooks API Tests
   - Playbook listing and retrieval
   - Case type matching
   - Comprehensive case analysis using playbooks
   - Playbook rule application and evaluation

### Integration and Performance Tests

6. **`test_api_comprehensive_suite.py`** - Cross-Endpoint Integration Tests
   - Cross-endpoint integration workflows
   - Performance and load testing
   - Error handling validation
   - API contract compliance
   - Basic security testing
   - Documentation compliance

## Test Categories

### Unit Tests
- Individual endpoint functionality
- Request/response validation
- Parameter handling
- Error conditions

### Integration Tests
- Cross-endpoint workflows
- Service integration
- Data consistency
- End-to-end scenarios

### Performance Tests
- Response time validation
- Concurrent request handling
- Large dataset processing
- Load testing scenarios

### Security Tests
- Input validation
- SQL injection protection
- XSS protection
- Parameter sanitization

### Contract Tests
- OpenAPI schema compliance
- Response format consistency
- HTTP method compliance
- Error response standardization

## Running Tests

### Run All Tests
```bash
# Run the comprehensive test suite
python run_comprehensive_tests.py

# Or use pytest directly
pytest tests/ -v
```

### Run Individual Test Suites
```bash
# Run specific endpoint tests
pytest tests/test_cases_api_comprehensive.py -v
pytest tests/test_documents_api_comprehensive.py -v
pytest tests/test_corpus_api_comprehensive.py -v
pytest tests/test_docs_api_comprehensive.py -v
pytest tests/test_playbooks_api_comprehensive.py -v

# Run integration and performance tests
pytest tests/test_api_comprehensive_suite.py -v
```

### Run Tests with Coverage
```bash
# Install coverage if not already installed
pip install pytest-cov

# Run tests with coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

## Test Configuration

### `conftest.py`
Contains shared test fixtures and configuration:
- Test client setup
- Sample data fixtures
- Mock service fixtures
- Common test utilities

### Test Fixtures Available
- `client` - FastAPI test client
- `sample_case` - Sample case data
- `sample_cases` - List of sample cases
- `sample_document` - Sample document data
- `sample_documents` - List of sample documents
- `sample_document_analysis` - Sample analysis results
- `sample_corpus_item` - Sample corpus item
- `sample_corpus_items` - List of corpus items
- `sample_playbook` - Sample playbook data
- `sample_comprehensive_analysis` - Sample analysis results
- `sample_documentation_categories` - Sample documentation structure
- Mock service fixtures for DataService, AIService, PlaybookService

## Test Coverage

The test suite covers:

### Cases API (`/cases/`)
- ✅ GET `/cases/` - List all cases
- ✅ GET `/cases/statistics` - Case statistics
- ✅ GET `/cases/{case_id}` - Get specific case
- ✅ GET `/cases/{case_id}/comprehensive-analysis` - Case analysis

### Documents API (`/documents/`)
- ✅ GET `/documents/cases/{case_id}/documents` - Case documents
- ✅ GET `/documents/{document_id}` - Get document
- ✅ GET `/documents/{document_id}/analysis` - Get analysis
- ✅ POST `/documents/{document_id}/analyze` - Perform analysis
- ✅ DELETE `/documents/{document_id}/analysis` - Delete analysis
- ✅ GET `/documents/{document_id}/content` - Get content

### Corpus API (`/corpus/`)
- ✅ GET `/corpus/` - Browse corpus
- ✅ GET `/corpus/categories` - Get categories
- ✅ GET `/corpus/search` - Search corpus
- ✅ GET `/corpus/concepts` - Research concepts
- ✅ GET `/corpus/{item_id}` - Get corpus item
- ✅ GET `/corpus/{item_id}/related` - Related materials

### Documentation API (`/docs/`)
- ✅ GET `/docs/` - Documentation overview
- ✅ GET `/docs/search` - Search documentation
- ✅ GET `/docs/schemas` - JSON schemas
- ✅ GET `/docs/{category}` - Category documentation

### Playbooks API (`/playbooks/`)
- ✅ GET `/playbooks/` - List playbooks
- ✅ GET `/playbooks/{case_type}` - Get playbook
- ✅ GET `/playbooks/match/{case_type}` - Match playbook
- ✅ POST `/playbooks/cases/{case_id}/comprehensive-analysis` - Generate analysis

## Test Patterns

### Mocking Strategy
Tests use `unittest.mock.patch` to mock service dependencies:
- `DataService` methods for data access
- `AIService` methods for AI analysis
- `PlaybookService` methods for playbook operations

### Error Testing
Each endpoint is tested for:
- Success scenarios with valid data
- Not found scenarios (404 errors)
- Service error scenarios (500 errors)
- Invalid input scenarios (422 errors)

### Integration Testing
Cross-endpoint workflows test:
- Case → Documents → Analysis workflow
- Corpus → Related Materials workflow
- Documentation → Search → Content workflow
- Playbook → Analysis → Recommendations workflow

## Continuous Integration

The test suite is designed to run in CI/CD environments:

### GitHub Actions Example
```yaml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run comprehensive tests
        run: python run_comprehensive_tests.py
```

## Test Reports

The test runner generates comprehensive reports:
- **Console Output** - Real-time test progress
- **comprehensive_test_report.md** - Detailed test results
- **Coverage Reports** - Code coverage analysis (when using pytest-cov)

## Best Practices

### Writing New Tests
1. Use descriptive test method names
2. Follow the Arrange-Act-Assert pattern
3. Mock external dependencies
4. Test both success and failure scenarios
5. Use fixtures for common test data
6. Group related tests in classes

### Test Data Management
1. Use fixtures for reusable test data
2. Keep test data minimal and focused
3. Avoid hardcoded values where possible
4. Use factories for complex data generation

### Performance Considerations
1. Mock expensive operations
2. Use appropriate timeouts
3. Test with realistic data sizes
4. Monitor test execution time

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify module structure

2. **Mock Failures**
   - Check mock patch paths
   - Verify mock return values
   - Ensure proper mock cleanup

3. **Timeout Issues**
   - Increase timeout values for slow operations
   - Mock time-consuming operations
   - Check for infinite loops in test code

4. **Database/Service Errors**
   - Ensure all external services are mocked
   - Check mock configuration
   - Verify test isolation

### Getting Help

1. Check test output for specific error messages
2. Run individual test files to isolate issues
3. Use pytest's `-v` flag for verbose output
4. Use pytest's `--tb=long` for detailed tracebacks

## Contributing

When adding new API endpoints:
1. Create comprehensive tests following existing patterns
2. Update this README with new test coverage
3. Add appropriate fixtures to `conftest.py`
4. Update the test runner script if needed
5. Ensure all test categories are covered (unit, integration, performance, security)

## Metrics and Goals

### Coverage Goals
- **Unit Test Coverage**: >90%
- **Integration Test Coverage**: >80%
- **API Endpoint Coverage**: 100%
- **Error Scenario Coverage**: >95%

### Performance Goals
- **Response Time**: <1 second for most endpoints
- **Concurrent Requests**: Handle 10+ concurrent requests
- **Large Dataset**: Process 1000+ items without timeout

### Quality Goals
- **Test Reliability**: >99% pass rate
- **Test Speed**: Complete suite in <5 minutes
- **Maintainability**: Clear, readable test code
- **Documentation**: All tests documented and explained