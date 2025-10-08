# Testing Strategy

This document outlines the comprehensive testing approach for the Legal Easy application, covering all layers from unit tests to end-to-end testing.

## Testing Pyramid

```
    /\
   /  \     E2E Tests (Cypress)
  /____\    
 /      \   Integration Tests (API + Component)
/________\  
|        |  Unit Tests (Jest + Vitest)
|________|  
```

## Test Types

### 1. Unit Tests
- **Backend**: Python unit tests with pytest
- **Frontend**: React component tests with Vitest + Testing Library
- **Coverage**: Individual functions and components
- **Speed**: Fast (< 1s per test)

### 2. Integration Tests
- **API Integration**: FastAPI test client
- **Component Integration**: React components with API calls
- **Database**: In-memory testing (if applicable)
- **Speed**: Medium (1-5s per test)

### 3. End-to-End Tests
- **Tool**: Cypress
- **Coverage**: Full user workflows
- **Environment**: Against deployed application
- **Speed**: Slow (10-30s per test)

### 4. Contract Tests
- **Tool**: Pact
- **Coverage**: API contracts between frontend and backend
- **Purpose**: Ensure API compatibility
- **Speed**: Medium (2-10s per test)

### 5. BDD Tests
- **Tool**: Cucumber (Gherkin syntax)
- **Coverage**: Business requirements
- **Purpose**: Executable specifications
- **Speed**: Variable

## Test Commands

### Backend Tests
```bash
cd backend
pip install -r requirements-test.txt
pytest                          # Run all tests
pytest --cov                    # With coverage
pytest -v                       # Verbose output
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
```

### Frontend Tests
```bash
cd frontend
npm install
npm test                        # Run all tests
npm run test:unit               # Unit tests only
npm run test:integration        # Integration tests only
npm run test:coverage           # With coverage
npm run test:watch              # Watch mode
```

### E2E Tests
```bash
cd frontend
npm run cypress:open            # Interactive mode
npm run cypress:run             # Headless mode
npm run e2e:local               # Against local servers
npm run e2e:staging             # Against staging environment
```

### Contract Tests
```bash
# Provider (Backend)
cd backend
pytest tests/contract/

# Consumer (Frontend)
cd frontend
npm run test:contract
```

## Test Structure

### Backend Test Structure
```
backend/
├── tests/
│   ├── unit/
│   │   ├── test_main.py
│   │   └── test_random_endpoint.py
│   ├── integration/
│   │   ├── test_api_integration.py
│   │   └── test_cors.py
│   ├── contract/
│   │   └── test_pact_provider.py
│   └── conftest.py
├── requirements-test.txt
└── pytest.ini
```

### Frontend Test Structure
```
frontend/
├── src/
│   ├── __tests__/
│   │   ├── unit/
│   │   │   ├── App.test.tsx
│   │   │   └── utils.test.ts
│   │   ├── integration/
│   │   │   └── api-integration.test.tsx
│   │   └── contract/
│   │       └── pact-consumer.test.ts
├── cypress/
│   ├── e2e/
│   │   ├── random-number.cy.ts
│   │   └── health-check.cy.ts
│   ├── fixtures/
│   ├── support/
│   └── cucumber/
│       ├── features/
│       │   └── random-number.feature
│       └── step_definitions/
├── vitest.config.ts
└── cypress.config.ts
```

## Coverage Targets

| Test Type | Coverage Target | Rationale |
|-----------|----------------|-----------|
| Unit Tests | 90%+ | Core business logic |
| Integration | 80%+ | API endpoints and key flows |
| E2E | Critical paths | User journeys |
| Contract | 100% | All API contracts |

## CI/CD Integration

### GitHub Actions Pipeline
```yaml
Test Pipeline:
1. Unit Tests (parallel)
   - Backend: pytest
   - Frontend: vitest
2. Integration Tests
   - API integration
   - Component integration
3. Contract Tests
   - Pact verification
4. E2E Tests
   - Cypress (staging environment)
5. Coverage Reports
   - Codecov integration
```

## Test Data Management

### Test Fixtures
- **Backend**: JSON fixtures for API responses
- **Frontend**: Mock data for components
- **E2E**: Seed data for consistent test runs

### Environment Management
- **Local**: Docker compose for test services
- **CI**: In-memory databases and mock services
- **Staging**: Dedicated test environment

## Best Practices

### Unit Tests
- Test one thing at a time
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies

### Integration Tests
- Test real API interactions
- Use test databases
- Clean up after each test
- Test error scenarios

### E2E Tests
- Focus on critical user paths
- Use page object pattern
- Make tests independent
- Include accessibility checks

### Contract Tests
- Version your contracts
- Test both happy and error paths
- Keep contracts minimal
- Automate contract verification

## Debugging Tests

### Backend
```bash
pytest --pdb                    # Drop into debugger on failure
pytest -s                       # Show print statements
pytest --lf                     # Run last failed tests
```

### Frontend
```bash
npm test -- --reporter=verbose  # Detailed output
npm run test:debug              # Debug mode
```

### E2E
```bash
npx cypress open --config video=true  # Record videos
```

## Performance Testing

### Load Testing
- **Tool**: Locust (Python)
- **Target**: API endpoints
- **Metrics**: Response time, throughput, error rate

### Frontend Performance
- **Tool**: Lighthouse CI
- **Metrics**: Core Web Vitals
- **Integration**: GitHub Actions

## Security Testing

### Backend Security
- **Tool**: Bandit (Python security linter)
- **Coverage**: Common vulnerabilities
- **Integration**: Pre-commit hooks

### Frontend Security
- **Tool**: npm audit
- **Coverage**: Dependency vulnerabilities
- **Integration**: Automated scanning

## Monitoring and Reporting

### Test Reports
- **Format**: JUnit XML, HTML reports
- **Storage**: CI artifacts
- **Visualization**: Test dashboards

### Metrics Tracking
- Test execution time trends
- Flaky test identification
- Coverage trends over time
- Failure rate analysis