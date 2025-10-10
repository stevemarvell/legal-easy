import { test, expect, Page } from '@playwright/test';

/**
 * End-to-End Tests for Case Document Analysis
 * 
 * These tests cover the complete user journey for document analysis:
 * 1. Navigate to case documents page
 * 2. View case and document summaries
 * 3. Select and view document content
 * 4. Trigger AI analysis
 * 5. View analysis results
 * 6. Verify UI updates
 */

test.describe('Case Document Analysis E2E', () => {
  const TEST_CASE_ID = 'case-001';
  const BASE_URL = 'http://localhost:8080';
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the case documents page
    await page.goto(`${BASE_URL}/cases/${TEST_CASE_ID}/documents`);
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
  });

  test('should display case summary and document summary', async ({ page }) => {
    // Check that case summary is displayed
    await expect(page.locator('[data-testid="case-summary"]')).toBeVisible();
    await expect(page.getByText('Case Summary')).toBeVisible();
    
    // Check that document summary is displayed
    await expect(page.getByText('Document Summary')).toBeVisible();
    
    // Verify case information is shown
    await expect(page.getByText('Wrongful Dismissal')).toBeVisible();
    await expect(page.getByText('Employment Dispute')).toBeVisible();
    await expect(page.getByText('Sarah Chen')).toBeVisible();
    
    // Verify document statistics
    await expect(page.getByText('Total Documents')).toBeVisible();
    await expect(page.getByText('Analyzed')).toBeVisible();
  });

  test('should display document list with proper information', async ({ page }) => {
    // Wait for documents to load
    await page.waitForSelector('[data-testid="document-list"]', { timeout: 10000 });
    
    // Check that documents are listed
    const documentItems = page.locator('[data-testid="document-item"]');
    await expect(documentItems).toHaveCountGreaterThan(0);
    
    // Check first document details
    const firstDocument = documentItems.first();
    await expect(firstDocument).toContainText('Employment Contract');
    await expect(firstDocument).toContainText('Sarah Chen');
    
    // Verify analysis status indicators
    const analysisIndicators = page.locator('[data-testid="analysis-status"]');
    await expect(analysisIndicators.first()).toBeVisible();
  });

  test('should select document and display content', async ({ page }) => {
    // Wait for documents to load
    await page.waitForSelector('[data-testid="document-list"]');
    
    // Click on the first document
    const firstDocument = page.locator('[data-testid="document-item"]').first();
    await firstDocument.click();
    
    // Wait for document viewer to load
    await page.waitForSelector('[data-testid="document-viewer"]');
    
    // Check that document header is displayed
    await expect(page.getByText('Employment Contract - Sarah Chen')).toBeVisible();
    
    // Check that document content tab is active
    await expect(page.getByRole('tab', { name: 'Document' })).toHaveAttribute('aria-selected', 'true');
    
    // Check that document content is displayed
    await expect(page.locator('[data-testid="document-content"]')).toBeVisible();
    await expect(page.getByText('EMPLOYMENT AGREEMENT')).toBeVisible();
  });

  test('should trigger document analysis and show results', async ({ page }) => {
    // Select a document that hasn't been analyzed
    await page.waitForSelector('[data-testid="document-list"]');
    
    // Find a document with pending analysis
    const pendingDocument = page.locator('[data-testid="document-item"]')
      .filter({ has: page.locator('[data-testid="analysis-status"][data-status="pending"]') })
      .first();
    
    if (await pendingDocument.count() > 0) {
      await pendingDocument.click();
      
      // Wait for document viewer
      await page.waitForSelector('[data-testid="document-viewer"]');
      
      // Click analyze button
      const analyzeButton = page.getByRole('button', { name: /analyze document/i });
      if (await analyzeButton.isVisible()) {
        await analyzeButton.click();
        
        // Wait for analysis to complete (with timeout)
        await page.waitForSelector('[data-testid="analysis-complete"]', { timeout: 30000 });
        
        // Switch to analysis tab
        await page.getByRole('tab', { name: 'AI Analysis' }).click();
        
        // Verify analysis results are displayed
        await expect(page.getByText('Document Type')).toBeVisible();
        await expect(page.getByText('Key Dates')).toBeVisible();
        await expect(page.getByText('Parties Involved')).toBeVisible();
        await expect(page.getByText('Summary')).toBeVisible();
        
        // Check that confidence scores are shown
        await expect(page.getByText('Confidence Scores')).toBeVisible();
      }
    }
  });

  test('should update document list after analysis', async ({ page }) => {
    // This test verifies that the document list updates after analysis
    
    // Get initial analysis count
    await page.waitForSelector('[data-testid="document-summary"]');
    const initialAnalyzedText = await page.locator('[data-testid="analyzed-count"]').textContent();
    const initialCount = parseInt(initialAnalyzedText?.match(/\d+/)?.[0] || '0');
    
    // Find and analyze a pending document
    const pendingDocument = page.locator('[data-testid="document-item"]')
      .filter({ has: page.locator('[data-testid="analysis-status"][data-status="pending"]') })
      .first();
    
    if (await pendingDocument.count() > 0) {
      await pendingDocument.click();
      await page.waitForSelector('[data-testid="document-viewer"]');
      
      const analyzeButton = page.getByRole('button', { name: /analyze document/i });
      if (await analyzeButton.isVisible()) {
        await analyzeButton.click();
        await page.waitForSelector('[data-testid="analysis-complete"]', { timeout: 30000 });
        
        // Check that the document summary updated
        const updatedAnalyzedText = await page.locator('[data-testid="analyzed-count"]').textContent();
        const updatedCount = parseInt(updatedAnalyzedText?.match(/\d+/)?.[0] || '0');
        
        expect(updatedCount).toBeGreaterThan(initialCount);
        
        // Check that the document item shows as analyzed
        const documentStatus = page.locator('[data-testid="document-item"]')
          .filter({ hasText: await pendingDocument.textContent() || '' })
          .locator('[data-testid="analysis-status"]');
        
        await expect(documentStatus).toHaveAttribute('data-status', 'completed');
      }
    }
  });

  test('should handle navigation between document and analysis tabs', async ({ page }) => {
    // Select a document
    await page.waitForSelector('[data-testid="document-list"]');
    const firstDocument = page.locator('[data-testid="document-item"]').first();
    await firstDocument.click();
    
    await page.waitForSelector('[data-testid="document-viewer"]');
    
    // Test tab navigation
    const documentTab = page.getByRole('tab', { name: 'Document' });
    const analysisTab = page.getByRole('tab', { name: 'AI Analysis' });
    
    // Should start on document tab
    await expect(documentTab).toHaveAttribute('aria-selected', 'true');
    
    // Switch to analysis tab
    await analysisTab.click();
    await expect(analysisTab).toHaveAttribute('aria-selected', 'true');
    
    // Switch back to document tab
    await documentTab.click();
    await expect(documentTab).toHaveAttribute('aria-selected', 'true');
    
    // Verify document content is visible
    await expect(page.locator('[data-testid="document-content"]')).toBeVisible();
  });

  test('should display proper error handling', async ({ page }) => {
    // Test error handling by trying to access non-existent case
    await page.goto(`${BASE_URL}/cases/non-existent-case/documents`);
    
    // Should show error message or redirect
    await expect(page.getByText(/case.*not found|error/i)).toBeVisible();
  });

  test('should be responsive on different screen sizes', async ({ page }) => {
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check that layout adapts
    await expect(page.locator('[data-testid="case-summary"]')).toBeVisible();
    await expect(page.locator('[data-testid="document-summary"]')).toBeVisible();
    
    // Test tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check layout still works
    await expect(page.locator('[data-testid="document-list"]')).toBeVisible();
    
    // Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check full layout
    await expect(page.locator('[data-testid="case-summary"]')).toBeVisible();
    await expect(page.locator('[data-testid="document-summary"]')).toBeVisible();
    await expect(page.locator('[data-testid="document-list"]')).toBeVisible();
  });

  test('should handle document content scrolling', async ({ page }) => {
    // Select a document with substantial content
    await page.waitForSelector('[data-testid="document-list"]');
    const firstDocument = page.locator('[data-testid="document-item"]').first();
    await firstDocument.click();
    
    await page.waitForSelector('[data-testid="document-viewer"]');
    
    // Check that document content is scrollable
    const contentArea = page.locator('[data-testid="document-content"]');
    await expect(contentArea).toBeVisible();
    
    // Test scrolling (if content is long enough)
    const scrollHeight = await contentArea.evaluate(el => el.scrollHeight);
    const clientHeight = await contentArea.evaluate(el => el.clientHeight);
    
    if (scrollHeight > clientHeight) {
      // Scroll to bottom
      await contentArea.evaluate(el => el.scrollTop = el.scrollHeight);
      
      // Scroll back to top
      await contentArea.evaluate(el => el.scrollTop = 0);
    }
  });

  test('should maintain state when navigating between documents', async ({ page }) => {
    // Select first document
    await page.waitForSelector('[data-testid="document-list"]');
    const documents = page.locator('[data-testid="document-item"]');
    
    await documents.nth(0).click();
    await page.waitForSelector('[data-testid="document-viewer"]');
    
    // Switch to analysis tab
    await page.getByRole('tab', { name: 'AI Analysis' }).click();
    
    // Select second document
    await documents.nth(1).click();
    
    // Should reset to document tab for new document
    const documentTab = page.getByRole('tab', { name: 'Document' });
    await expect(documentTab).toHaveAttribute('aria-selected', 'true');
  });
});

test.describe('Case Document Analysis Performance', () => {
  test('should load case documents page within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto(`http://localhost:8080/cases/case-001/documents`);
    await page.waitForSelector('[data-testid="document-list"]');
    
    const loadTime = Date.now() - startTime;
    
    // Should load within 5 seconds
    expect(loadTime).toBeLessThan(5000);
  });

  test('should handle large document content efficiently', async ({ page }) => {
    await page.goto(`http://localhost:8080/cases/case-001/documents`);
    await page.waitForSelector('[data-testid="document-list"]');
    
    // Select a document
    const firstDocument = page.locator('[data-testid="document-item"]').first();
    await firstDocument.click();
    
    const startTime = Date.now();
    await page.waitForSelector('[data-testid="document-content"]');
    const contentLoadTime = Date.now() - startTime;
    
    // Content should load within 3 seconds
    expect(contentLoadTime).toBeLessThan(3000);
  });
});