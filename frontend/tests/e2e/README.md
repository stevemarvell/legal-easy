# End-to-End Tests for Case Document Analysis

This directory contains comprehensive end-to-end tests for the case document analysis feature.

## Test Coverage

### 🎯 **Core User Journeys**
- Navigate to case documents page
- View case summary and document summary
- Select and view document content
- Trigger AI document analysis
- View analysis results
- Navigate between document and analysis tabs

### 🔧 **Technical Tests**
- API endpoint integration
- Error handling and edge cases
- Performance and load times
- Responsive design across devices
- State management between components

### 📱 **Cross-Browser Testing**
- Chrome, Firefox, Safari, Edge
- Mobile Chrome and Safari
- Different screen sizes and orientations

## Test Files

### `case-document-analysis.spec.ts`
Main test suite covering:
- **Display Tests**: Case summary, document summary, document list
- **Interaction Tests**: Document selection, content viewing, analysis triggering
- **Navigation Tests**: Tab switching, state management
- **Error Handling**: Non-existent cases/documents
- **Responsive Design**: Mobile, tablet, desktop views
- **Performance Tests**: Load times, content rendering

## Running Tests

### Prerequisites
```bash
# Install Playwright
npm install @playwright/test
npx playwright install
```

### Backend Setup
```bash
# Start backend server (from backend directory)
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Start frontend server (from frontend directory)
cd frontend
npm run dev
```

### Run Tests
```bash
# Run all E2E tests
npm run test:e2e

# Run tests with browser UI
npm run test:e2e:headed

# Debug tests
npm run test:e2e:debug

# Run tests with Playwright UI
npm run test:e2e:ui

# View test report
npm run test:e2e:report
```

## Test Data

### Test Case: `case-001`
- **Title**: "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions"
- **Type**: Employment Dispute
- **Client**: Sarah Chen
- **Documents**: 3 documents (Employment Contract, Safety Report, Termination Notice)

### Test Documents
- **doc-001**: Employment Contract - Sarah Chen
- **doc-002**: Safety Violation Report  
- **doc-003**: Termination Notice Email

## Test Scenarios

### 1. **Happy Path Flow**
```
1. Navigate to /cases/case-001/documents
2. Verify case summary displays
3. Verify document summary shows correct counts
4. Select first document
5. Verify document content loads
6. Click "Analyze Document" (if not analyzed)
7. Wait for analysis completion
8. Switch to "AI Analysis" tab
9. Verify analysis results display
10. Verify document list updates with analysis status
```

### 2. **Error Scenarios**
```
1. Navigate to non-existent case
2. Verify error handling
3. Test network failures
4. Test malformed responses
```

### 3. **Performance Tests**
```
1. Measure page load time
2. Measure document content load time
3. Measure analysis completion time
4. Test with large documents
```

### 4. **Responsive Design**
```
1. Test on mobile (375x667)
2. Test on tablet (768x1024)  
3. Test on desktop (1920x1080)
4. Verify layout adapts correctly
```

## Test Data Attributes

Components include `data-testid` attributes for reliable element selection:

- `data-testid="case-summary"` - Case summary card
- `data-testid="document-summary"` - Document summary card
- `data-testid="document-list"` - Document list container
- `data-testid="document-item"` - Individual document items
- `data-testid="analysis-status"` - Analysis status indicators
- `data-testid="document-viewer"` - Document viewer container
- `data-testid="document-content"` - Document content area
- `data-testid="analyze-button"` - Analyze document button
- `data-testid="analysis-complete"` - Analysis completion indicator

## CI/CD Integration

### GitHub Actions Example
```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - uses: actions/setup-python@v4
      
      - name: Install dependencies
        run: |
          cd frontend && npm install
          cd backend && pip install -r requirements.txt
          
      - name: Install Playwright
        run: cd frontend && npx playwright install
        
      - name: Run E2E tests
        run: |
          cd backend && python run_e2e_tests.py &
          cd frontend && npm run test:e2e
```

## Debugging Tests

### Visual Debugging
```bash
# Run with browser visible
npm run test:e2e:headed

# Run in debug mode (step through)
npm run test:e2e:debug
```

### Screenshots and Videos
- Screenshots taken on test failure
- Videos recorded for failed tests
- Traces available for debugging

### Test Reports
- HTML report with detailed results
- JSON report for CI integration
- JUnit XML for test result parsing

## Best Practices

### 1. **Reliable Selectors**
- Use `data-testid` attributes
- Avoid CSS selectors that may change
- Use semantic role selectors when appropriate

### 2. **Wait Strategies**
- Wait for network idle on page loads
- Wait for specific elements to appear
- Use proper timeouts for long operations

### 3. **Test Isolation**
- Each test should be independent
- Clean up test data after tests
- Use unique test data when possible

### 4. **Error Handling**
- Test both success and failure scenarios
- Verify error messages are user-friendly
- Test network failure scenarios

## Troubleshooting

### Common Issues

**Tests timing out**
- Increase timeout values
- Check if servers are running
- Verify network connectivity

**Elements not found**
- Check data-testid attributes exist
- Verify element is visible
- Wait for element to load

**Analysis not completing**
- Check backend logs
- Verify API endpoints are working
- Check document content is valid

**Flaky tests**
- Add proper wait conditions
- Check for race conditions
- Verify test data consistency