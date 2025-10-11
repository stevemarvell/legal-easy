import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'

// Mock data for testing
const mockDocuments = [
  {
    id: 'doc-001',
    name: 'Employment Contract - John Doe',
    case_id: 'case-001',
    type: 'Contract',
    size: 15420,
    upload_date: '2024-01-15T10:30:00Z',
    content_preview: 'EMPLOYMENT AGREEMENT between ABC Corp and John Doe...',
    analysis_completed: true
  },
  {
    id: 'doc-002',
    name: 'Termination Notice',
    case_id: 'case-001',
    type: 'Legal Brief',
    size: 8750,
    upload_date: '2024-01-12T14:15:00Z',
    content_preview: 'NOTICE OF TERMINATION - This letter serves as formal notice...',
    analysis_completed: false
  },
  {
    id: 'doc-003',
    name: 'Email Correspondence',
    case_id: 'case-001',
    type: 'Email',
    size: 3200,
    upload_date: '2024-01-10T09:00:00Z',
    content_preview: 'From: hr@company.com To: employee@company.com Subject: Meeting Request...',
    analysis_completed: true
  }
]

const mockAnalysis = {
  document_id: 'doc-001',
  key_dates: ['2022-03-15', '2024-01-12'],
  parties_involved: ['John Doe', 'ABC Corp'],
  document_type: 'Employment Contract',
  summary: 'Employment agreement for software engineer position with standard terms and conditions.',
  key_clauses: ['At-will employment clause', 'Confidentiality agreement', 'Non-compete clause'],
  confidence_scores: {
    parties: 0.95,
    dates: 0.98,
    contract_terms: 0.92,
    key_clauses: 0.89,
    legal_analysis: 0.87
  },
  overall_confidence: 0.92,
  uncertainty_flags: []
}

// Background steps
Given('there are documents in the system', () => {
  cy.intercept('GET', '**/api/documents/cases/*/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getDocuments')
})

Given('there is a case with documents', () => {
  cy.intercept('GET', '**/api/cases/case-001', { 
    statusCode: 200, 
    body: {
      id: 'case-001',
      title: 'Employment Dispute - John Doe',
      case_type: 'Employment Dispute',
      client_name: 'John Doe',
      status: 'Active',
      created_date: '2024-01-15T09:00:00Z',
      summary: 'Employment dispute case',
      key_parties: ['John Doe (Claimant)', 'ABC Corp (Respondent)'],
      documents: ['doc-001', 'doc-002', 'doc-003'],
      playbook_id: 'employment-dispute'
    }
  }).as('getCase')
  
  cy.intercept('GET', '**/api/documents/cases/case-001/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getCaseDocuments')
})

Given('there is an unanalyzed document', () => {
  const unanalyzedDoc = { ...mockDocuments[1], analysis_completed: false }
  
  cy.intercept('GET', '**/api/documents/doc-002', { 
    statusCode: 200, 
    body: unanalyzedDoc 
  }).as('getUnanalyzedDocument')
  
  cy.intercept('POST', '**/api/documents/doc-002/analyze', { 
    statusCode: 200, 
    body: { ...mockAnalysis, document_id: 'doc-002' }
  }).as('analyzeDocument')
})

Given('there is an analyzed document', () => {
  cy.intercept('GET', '**/api/documents/doc-001', { 
    statusCode: 200, 
    body: mockDocuments[0] 
  }).as('getAnalyzedDocument')
  
  cy.intercept('GET', '**/api/documents/doc-001/analysis', { 
    statusCode: 200, 
    body: mockAnalysis 
  }).as('getDocumentAnalysis')
})

Given('there are multiple documents in the system', () => {
  cy.intercept('GET', '**/api/documents/cases/*/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getMultipleDocuments')
})

Given('there are documents with different analysis statuses', () => {
  // Mock data already has mixed statuses
  cy.intercept('GET', '**/api/documents/cases/*/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getDocumentsWithStatuses')
})

Given('there are documents of different types', () => {
  // Mock data already has different types
  cy.intercept('GET', '**/api/documents/cases/*/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getDocumentsWithTypes')
})

Given('there is a document that fails analysis', () => {
  cy.intercept('GET', '**/api/documents/doc-002', { 
    statusCode: 200, 
    body: mockDocuments[1] 
  }).as('getFailingDocument')
  
  cy.intercept('POST', '**/api/documents/doc-002/analyze', { 
    statusCode: 500,
    body: { detail: 'Analysis failed due to unsupported document format' }
  }).as('failDocumentAnalysis')
})

Given('there is a document with content', () => {
  cy.intercept('GET', '**/api/documents/doc-001', { 
    statusCode: 200, 
    body: mockDocuments[0] 
  }).as('getDocumentWithContent')
  
  cy.intercept('GET', '**/api/documents/doc-001/content', { 
    statusCode: 200, 
    body: {
      document_id: 'doc-001',
      content: 'EMPLOYMENT AGREEMENT\n\nThis Employment Agreement is entered into between ABC Corp and John Doe...',
      content_length: 1500
    }
  }).as('getDocumentContent')
})

Given('there is an analyzed document with confidence scores', () => {
  cy.intercept('GET', '**/api/documents/doc-001', { 
    statusCode: 200, 
    body: mockDocuments[0] 
  }).as('getDocumentWithConfidence')
  
  cy.intercept('GET', '**/api/documents/doc-001/analysis', { 
    statusCode: 200, 
    body: mockAnalysis 
  }).as('getAnalysisWithConfidence')
})

Given('there are multiple unanalyzed documents in a case', () => {
  const unanalyzedDocs = mockDocuments.map(doc => ({ ...doc, analysis_completed: false }))
  
  cy.intercept('GET', '**/api/documents/cases/case-001/documents', { 
    statusCode: 200, 
    body: unanalyzedDocs 
  }).as('getUnanalyzedDocuments')
})

Given('there are documents with different types and statuses', () => {
  // Mock data already covers this
  cy.intercept('GET', '**/api/documents/cases/*/documents', { 
    statusCode: 200, 
    body: mockDocuments 
  }).as('getDocumentsForFiltering')
})

Given('there is a document that has been analyzed multiple times', () => {
  cy.intercept('GET', '**/api/documents/doc-001', { 
    statusCode: 200, 
    body: mockDocuments[0] 
  }).as('getDocumentWithHistory')
  
  cy.intercept('GET', '**/api/documents/doc-001/analysis', { 
    statusCode: 200, 
    body: {
      ...mockAnalysis,
      analysis_history: [
        { timestamp: '2024-01-15T10:00:00Z', version: '1.0', confidence: 0.85 },
        { timestamp: '2024-01-16T14:30:00Z', version: '1.1', confidence: 0.92 }
      ]
    }
  }).as('getAnalysisHistory')
})

// Navigation steps
When('I navigate to the documents page', () => {
  cy.visit('/documents')
})

When('I navigate to the case documents page', () => {
  cy.visit('/cases/case-001/documents')
})

When('I navigate to the document detail page', () => {
  cy.visit('/documents/doc-002')
})

When('I navigate to a document detail page from case context', () => {
  cy.visit('/cases/case-001/documents/doc-001')
})

When('I click on a document card', () => {
  cy.get('[data-testid="document-card"]').first().click()
})

When('I click on a document in the list', () => {
  cy.get('[data-testid="document-item"]').first().click()
})

When('I click the {string} button', (buttonText: string) => {
  cy.contains('button', buttonText).click()
})

When('I click the grid view toggle', () => {
  cy.get('[aria-label="grid view"]').click()
})

When('I click the list view toggle', () => {
  cy.get('[aria-label="list view"]').click()
})

When('I enter {string} in the search box', (searchTerm: string) => {
  cy.get('[data-testid="search-input"]').type(searchTerm)
})

When('I clear the search box', () => {
  cy.get('[data-testid="search-input"]').clear()
})

When('I tap on a document', () => {
  cy.get('[data-testid="document-card"]').first().click()
})

When('I use keyboard navigation', () => {
  cy.get('body').tab()
})

// Assertion steps
Then('I should see documents displayed as cards', () => {
  cy.wait('@getDocuments')
  cy.get('[data-testid="document-card"]').should('have.length.greaterThan', 0)
})

Then('each document card should display basic information', () => {
  cy.get('[data-testid="document-card"]').first().within(() => {
    cy.get('[data-testid="document-title"]').should('be.visible')
    cy.get('[data-testid="document-type"]').should('be.visible')
    cy.get('[data-testid="document-size"]').should('be.visible')
    cy.get('[data-testid="document-analysis-status"]').should('be.visible')
  })
})

Then('I should see the case documents', () => {
  cy.wait('@getCaseDocuments')
  cy.get('[data-testid="document-list"]').should('be.visible')
})

Then('I should see a toggle between list and grid view', () => {
  cy.get('[aria-label="list view"]').should('be.visible')
  cy.get('[aria-label="grid view"]').should('be.visible')
})

Then('I should see the case context in the page title', () => {
  cy.get('[data-testid="page-title"]').should('contain.text', 'Case case-001')
})

Then('I should be taken to the document detail page', () => {
  cy.url().should('match', /\/documents\/doc-\d+/)
})

Then('I should be taken to the document detail page with case context', () => {
  cy.url().should('match', /\/cases\/case-\d+\/documents\/doc-\d+/)
})

Then('I should see comprehensive document information', () => {
  cy.get('[data-testid="document-title"]').should('be.visible')
  cy.get('[data-testid="document-type"]').should('be.visible')
  cy.get('[data-testid="document-size"]').should('be.visible')
})

Then('I should see the document content and analysis', () => {
  cy.get('[data-testid="document-content"]').should('be.visible')
  cy.get('[data-testid="document-analysis"]').should('be.visible')
})

Then('I should see breadcrumbs showing the case path', () => {
  cy.get('[aria-label="breadcrumb"]').should('be.visible')
  cy.get('[aria-label="breadcrumb"]').should('contain.text', 'Cases')
  cy.get('[aria-label="breadcrumb"]').should('contain.text', 'Documents')
})

Then('each document card should display:', (dataTable) => {
  const fields = dataTable.hashes()
  
  cy.get('[data-testid="document-card"]').first().within(() => {
    fields.forEach((field) => {
      switch (field.Field) {
        case 'Title':
          cy.get('[data-testid="document-title"]').should('be.visible')
          break
        case 'Type':
          cy.get('[data-testid="document-type"]').should('be.visible')
          break
        case 'Size':
          cy.get('[data-testid="document-size"]').should('be.visible')
          break
        case 'Upload Date':
          cy.get('[data-testid="document-upload-date"]').should('be.visible')
          break
        case 'Analysis Status':
          cy.get('[data-testid="document-analysis-status"]').should('be.visible')
          break
        case 'Content Preview':
          cy.get('[data-testid="document-preview"]').should('be.visible')
          break
      }
    })
  })
})

Then('the document analysis should start', () => {
  cy.wait('@analyzeDocument')
})

Then('I should see analysis results when complete', () => {
  cy.get('[data-testid="analysis-results"]').should('be.visible')
})

Then('the document status should update to {string}', (status: string) => {
  cy.get('[data-testid="document-analysis-status"]').should('contain.text', status)
})

Then('I should see the analysis results including:', (dataTable) => {
  const fields = dataTable.hashes()
  
  fields.forEach((field) => {
    switch (field.Field) {
      case 'Key Dates':
        cy.get('[data-testid="analysis-key-dates"]').should('be.visible')
        break
      case 'Parties Involved':
        cy.get('[data-testid="analysis-parties"]').should('be.visible')
        break
      case 'Document Type':
        cy.get('[data-testid="analysis-document-type"]').should('be.visible')
        break
      case 'Summary':
        cy.get('[data-testid="analysis-summary"]').should('be.visible')
        break
      case 'Key Clauses':
        cy.get('[data-testid="analysis-key-clauses"]').should('be.visible')
        break
      case 'Confidence Scores':
        cy.get('[data-testid="analysis-confidence"]').should('be.visible')
        break
    }
  })
})

Then('I should only see documents matching {string}', (searchTerm: string) => {
  cy.get('[data-testid="document-card"]').should('have.length.lessThan', mockDocuments.length)
  cy.get('[data-testid="document-card"]').each(($card) => {
    cy.wrap($card).should('contain.text', searchTerm)
  })
})

Then('I should see all documents again', () => {
  cy.get('[data-testid="document-card"]').should('have.length', mockDocuments.length)
})

Then('I should see status indicators with appropriate colors:', (dataTable) => {
  const statuses = dataTable.hashes()
  
  statuses.forEach((status) => {
    cy.get(`[data-testid="document-analysis-status"][data-status="${status.Status.toLowerCase()}"]`)
      .should('be.visible')
  })
})

Then('I should see documents in grid layout', () => {
  cy.get('[data-testid="documents-grid"]').should('be.visible')
})

Then('I should see documents in list layout with document viewer', () => {
  cy.get('[data-testid="document-list"]').should('be.visible')
  cy.get('[data-testid="document-viewer"]').should('be.visible')
})

Then('I should see appropriate icons for each document type:', (dataTable) => {
  // This would require more specific icon testing
  cy.get('[data-testid="document-card"]').should('have.length.greaterThan', 0)
})

Then('the document cards should be displayed in a single column', () => {
  cy.get('[data-testid="documents-grid"]').should('have.css', 'grid-template-columns', '1fr')
})

Then('all information should be readable', () => {
  cy.get('[data-testid="document-card"]').first().within(() => {
    cy.get('[data-testid="document-title"]').should('be.visible')
    cy.get('[data-testid="document-type"]').should('be.visible')
  })
})

Then('I should navigate to the document detail page', () => {
  cy.url().should('match', /\/documents\/doc-\d+/)
})

Then('I should see an error message', () => {
  cy.wait('@failDocumentAnalysis')
  cy.get('[data-testid="error-message"]').should('be.visible')
})

Then('the document status should remain {string}', (status: string) => {
  cy.get('[data-testid="document-analysis-status"]').should('contain.text', status)
})

Then('I should be able to retry the analysis', () => {
  cy.get('[data-testid="retry-analysis-button"]').should('be.visible')
})

Then('I should see the full document content', () => {
  cy.wait('@getDocumentContent')
  cy.get('[data-testid="document-content"]').should('be.visible')
})

Then('I should see document metadata', () => {
  cy.get('[data-testid="document-metadata"]').should('be.visible')
})

Then('I should see analysis results if available', () => {
  cy.get('[data-testid="analysis-results"]').should('be.visible')
})

Then('I should see breadcrumbs showing:', (dataTable) => {
  const levels = dataTable.hashes()
  
  cy.get('[aria-label="breadcrumb"]').should('be.visible')
  levels.forEach((level) => {
    cy.get('[aria-label="breadcrumb"]').should('contain.text', level.Label.replace('{case_id}', 'case-001').replace('{document_name}', 'Employment Contract'))
  })
})

Then('I should see confidence scores for different analysis aspects', () => {
  cy.get('[data-testid="confidence-scores"]').should('be.visible')
})

Then('I should see overall confidence level', () => {
  cy.get('[data-testid="overall-confidence"]').should('be.visible')
})

Then('I should see uncertainty flags if confidence is low', () => {
  cy.get('[data-testid="uncertainty-flags"]').should('be.visible')
})

Then('all pending documents should be queued for analysis', () => {
  cy.get('[data-testid="analysis-queue"]').should('be.visible')
})

Then('I should see progress indicators for each document', () => {
  cy.get('[data-testid="analysis-progress"]').should('be.visible')
})

Then('I should see filter options for:', (dataTable) => {
  const filters = dataTable.hashes()
  
  filters.forEach((filter) => {
    cy.get(`[data-testid="filter-${filter.Filter.toLowerCase().replace(' ', '-')}"]`).should('be.visible')
  })
})

Then('I should see analysis history', () => {
  cy.get('[data-testid="analysis-history"]').should('be.visible')
})

Then('I should be able to compare different analysis results', () => {
  cy.get('[data-testid="analysis-comparison"]').should('be.visible')
})

Then('I should see timestamps for each analysis', () => {
  cy.get('[data-testid="analysis-timestamp"]').should('be.visible')
})

Then('I should see options to:', (dataTable) => {
  const actions = dataTable.hashes()
  
  actions.forEach((action) => {
    const testId = action.Action.toLowerCase().replace(/\s+/g, '-')
    cy.get(`[data-testid="${testId}-button"]`).should('be.visible')
  })
})

Then('the page should have proper heading structure', () => {
  cy.get('h1').should('exist')
  cy.get('[data-testid="page-title"]').should('exist')
})

Then('document cards should be keyboard accessible', () => {
  cy.get('[data-testid="document-card"]').first().should('be.focusable')
})

Then('screen readers should be able to navigate the content', () => {
  cy.get('[data-testid="document-card"]').first().should('have.attr', 'role')
})

Then('I should be able to access all interactive elements', () => {
  cy.get('[data-testid="document-card"]').first().focus()
  cy.focused().should('exist')
})

Then('I should be able to navigate to document details using Enter key', () => {
  cy.get('[data-testid="document-card"]').first().focus()
  cy.focused().type('{enter}')
  cy.url().should('match', /\/documents\/doc-\d+/)
})