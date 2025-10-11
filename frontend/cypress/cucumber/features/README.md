# Case Management E2E Tests

This directory contains Cucumber feature files for end-to-end testing of the Legal Easy application.

## Features

### case-management.feature

Comprehensive end-to-end tests for the case management functionality, including:

- **Case List View**: Testing the display and navigation of case lists
- **Case Detail View**: Testing comprehensive case information display
- **Search Functionality**: Testing case search and filtering
- **Document Management**: Testing document display and navigation
- **Analysis Status**: Testing document analysis status indicators
- **Responsive Design**: Testing mobile and desktop layouts
- **Accessibility**: Testing keyboard navigation and screen reader support
- **Error Handling**: Testing error states and loading states

## Test Scenarios

The case management tests cover the following scenarios:

1. **Basic Navigation**
   - View case list
   - Navigate to case details
   - Return to case list

2. **Data Display**
   - Case metadata display (title, client, type, status, etc.)
   - Document information (names, types, sizes, analysis status)
   - Key parties information
   - Analysis status indicators

3. **Interactive Features**
   - Search functionality
   - Document navigation
   - Status indicators
   - Hover effects

4. **Responsive Design**
   - Mobile layout testing
   - Desktop layout testing
   - Touch interaction testing

5. **Accessibility**
   - Keyboard navigation
   - Screen reader compatibility
   - Proper heading structure
   - Focus management

6. **Error Handling**
   - Empty states
   - API error states
   - Loading states

## Running the Tests

### Prerequisites

1. Ensure the backend API is running on `http://localhost:8000`
2. Ensure the frontend is running on `http://localhost:8080`
3. Install dependencies: `npm install`

### Run All Case Management Tests

```bash
# Using npm script
npm run test:cases

# Using custom runner
npm run test:e2e:cases

# Using Cypress directly
npx cypress run --spec cypress/cucumber/features/case-management.feature
```

### Run Tests in Interactive Mode

```bash
# Open Cypress Test Runner
npm run cypress:open

# Select the case-management.feature file to run interactively
```

### Run Tests Against Different Environments

```bash
# Local development
npm run e2e:local

# Staging environment
npm run e2e:staging
```

## Test Data

The tests use mock data defined in the step definitions file. The mock data includes:

- **Cases**: 3 sample cases with different statuses (Active, Under Review, Resolved)
- **Documents**: Sample documents with different types and analysis statuses
- **API Responses**: Mocked API responses for various scenarios

## Test Structure

```
cypress/cucumber/
├── features/
│   ├── case-management.feature    # Main feature file
│   └── README.md                  # This file
└── step_definitions/
    └── case-management.steps.ts   # Step implementations
```

## Adding New Tests

To add new test scenarios:

1. Add new scenarios to `case-management.feature`
2. Implement corresponding step definitions in `case-management.steps.ts`
3. Add any necessary test data or API mocks
4. Update component test IDs if needed

## Test IDs

The tests rely on `data-testid` attributes in the components. Key test IDs include:

- `case-card`: Individual case cards
- `case-title`: Case title elements
- `case-status`: Case status chips
- `case-overview`: Case detail overview section
- `documents-section`: Documents section
- `analysis-status-indicators`: Analysis status display
- `search-input`: Search input field
- `back-button`: Navigation back button

## Troubleshooting

### Common Issues

1. **Tests failing due to timing**: Increase timeouts in cypress.config.ts
2. **API mocks not working**: Check that intercepts are set up correctly
3. **Elements not found**: Verify test IDs are present in components
4. **Responsive tests failing**: Check viewport settings

### Debug Mode

Run tests with debug output:

```bash
DEBUG=cypress:* npm run test:cases
```

### Video and Screenshots

Test runs automatically capture:
- Videos of test execution (stored in `cypress/videos/`)
- Screenshots of failures (stored in `cypress/screenshots/`)

## Best Practices

1. **Use descriptive scenario names** that clearly indicate what is being tested
2. **Keep scenarios focused** on a single feature or user journey
3. **Use proper Given-When-Then structure** for clarity
4. **Add data tables** for testing multiple similar scenarios
5. **Mock external dependencies** to ensure test reliability
6. **Test both happy path and error scenarios**
7. **Include accessibility testing** in all scenarios
8. **Test responsive behavior** for different screen sizes