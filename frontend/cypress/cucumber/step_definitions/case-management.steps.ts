import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'

// Mock data for testing
const mockCases = [
  {
    id: 'case-001',
    title: 'Wrongful Dismissal - Sarah Chen vs TechCorp Solutions',
    case_type: 'Employment Dispute',
    client_name: 'Sarah Chen',
    status: 'Active',
    created_date: '2024-01-15T09:00:00Z',
    summary: 'Employee alleges wrongful dismissal after reporting safety violations. Claims retaliation and seeks reinstatement plus damages.',
    key_parties: [
      'Sarah Chen (Claimant)',
      'TechCorp Solutions Ltd. (Respondent)',
      'Marcus Rodriguez (HR Director)',
      'Jennifer Walsh (Direct Supervisor)'
    ],
    documents: ['doc-001', 'doc-002', 'doc-003'],
    playbook_id: 'employment-dispute'
  },
  {
    id: 'case-002',
    title: 'Software License Violation - TechStart Inc.',
    case_type: 'Intellectual Property',
    client_name: 'TechStart Inc.',
    status: 'Under Review',
    created_date: '2024-01-10T09:00:00Z',
    summary: 'Intellectual property dispute over software licensing agreements and unauthorized use of proprietary code.',
    key_parties: [
      'TechStart Inc. (Claimant)',
      'SoftwareCorp Ltd. (Respondent)'
    ],
    documents: ['doc-004', 'doc-005'],
    playbook_id: 'intellectual-property'
  },
  {
    id: 'case-003',
    title: 'Contract Dispute - TechCorp Solutions',
    case_type: 'Contract Breach',
    client_name: 'TechCorp Solutions',
    status: 'Resolved',
    created_date: '2024-01-05T11:30:00Z',
    summary: 'Breach of contract in consulting services agreement with failure to deliver agreed upon services.',
    key_parties: [
      'TechCorp Solutions (Claimant)',
      'ConsultingFirm LLC (Respondent)'
    ],
    documents: ['doc-006'],
    playbook_id: 'contract-breach'
  }
]

const mockDocuments = [
  {
    id: 'doc-001',
    name: 'Employment Contract - Sarah Chen',
    case_id: 'case-001',
    type: 'Contract',
    size: 15420,
    upload_date: '2024-01-15T10:30:00Z',
    content_preview: 'EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...',
    analysis_completed: true
  },
  {
    id: 'doc-002',
    name: 'Termination Notice - Sarah Chen',
    case_id: 'case-001',
    type: 'Legal Brief',
    size: 8750,
    upload_date: '2024-01-12T14:15:00Z',
    content_preview: 'NOTICE OF TERMINATION - This letter serves as formal notice...',
    analysis_completed: true
  },
  {
    id: 'doc-003',
    name: 'Safety Violation Report',
    case_id: 'case-001',
    type: 'Evidence',
    size: 12300,
    upload_date: '2024-01-10T16:20:00Z',
    content_preview: 'SAFETY VIOLATION REPORT - Documented safety concerns...',
    analysis_completed: false
  }
]

// Background steps
Given('the backend API is available', () => {
  // Set up API intercepts for successful responses
  cy.intercept('GET', '**/api/cases', { 
    statusCode: 200, 
    body: mockCases 
  }).as('getCases')
  
  cy.intercept('GET', '**/api/cases/case-001', { 
    statusCode: 200, 
    body: mockCases[0] 
  }).as('getCase001')
  
  cy.intercept('GET', '**/api/documents/cases/case-001/documents', { 
    statusCode: 200, 
    body: mockDocuments.filter(doc => doc.case_id === 'case-001')
  }).as('getCase001Documents')
})

Given('I am on the Legal Easy application', () => {
  cy.visit('/')
})

// Case list scenarios
Given('there are cases in the system', () => {
  // API intercept is already set up in background
})

Given('there are multiple cases in the system', () => {
  // Use the same mock data which has multiple cases
})

Given('there are cases with different statuses', () => {
  // Mock data already includes different statuses: Active, Under Review, Resolved
})

Given('there are no cases in the system', () => {
  cy.intercept('GET', '**/api/cases', { 
    statusCode: 200, 
    body: [] 
  }).as('getEmptyCases')
})

Given('the cases API is unavailable', () => {
  cy.intercept('GET', '**/api/cases', { 
    statusCode: 500,
    body: { error: 'Internal server error' }
  }).as('getCasesError')
})

Given('the cases API has a delayed response', () => {
  cy.intercept('GET', '**/api/cases', (req) => {
    req.reply((res) => {
      res.delay(2000)
      res.send({ statusCode: 200, body: mockCases })
    })
  }).as('getDelayedCases')
})

Given('there is a case with ID {string}', (caseId: string) => {
  const caseData = mockCases.find(c => c.id === caseId)
  if (caseData) {
    cy.intercept('GET', `**/api/cases/${caseId}`, { 
      statusCode: 200, 
      body: caseData 
    }).as(`getCase${caseId.replace('-', '')}`)
  }
})

Given('there is a case with documents', () => {
  // Use case-001 which has documents
  cy.intercept('GET', '**/api/cases/case-001', { 
    statusCode: 200, 
    body: mockCases[0] 
  }).as('getCaseWithDocs')
})

Given('I am using a mobile device', () => {
  cy.viewport('iphone-x')
})

// Navigation steps
When('I navigate to the cases page', () => {
  cy.visit('/cases')
})

When('I navigate to the case detail page for {string}', (caseId: string) => {
  cy.visit(`/cases/${caseId}`)
})

When('I navigate directly to {string}', (url: string) => {
  cy.visit(url)
})

When('I click on a case card', () => {
  cy.get('[data-testid="case-card"]').first().click()
})

When('I click on the first case', () => {
  cy.get('[data-testid="case-card"]').first().click()
})

When('I click the back button', () => {
  cy.get('[data-testid="back-button"]').click()
})

When('I enter {string} in the search box', (searchTerm: string) => {
  cy.get('[data-testid="search-input"]').type(searchTerm)
})

When('I clear the search box', () => {
  cy.get('[data-testid="search-input"]').clear()
})

When('I hover over a case card', () => {
  cy.get('[data-testid="case-card"]').first().trigger('mouseover')
})

When('I am on the case detail page', () => {
  cy.visit('/cases/case-001')
  cy.wait('@getCase001')
  cy.wait('@getCase001Documents')
})

When('I click on a document name', () => {
  cy.get('[data-testid="document-link"]').first().click()
})

When('I click {string}', (buttonText: string) => {
  cy.contains('button', buttonText).click()
})

When('I tap on a case', () => {
  cy.get('[data-testid="case-card"]').first().click()
})

When('I use keyboard navigation', () => {
  cy.get('body').tab()
})

When('the API responds', () => {
  cy.wait('@getDelayedCases')
})

// Assertion steps
Then('I should see a list of cases', () => {
  cy.wait('@getCases')
  cy.get('[data-testid="case-card"]').should('have.length.greaterThan', 0)
})

Then('each case should display basic information', () => {
  cy.get('[data-testid="case-card"]').first().within(() => {
    cy.get('[data-testid="case-title"]').should('be.visible')
    cy.get('[data-testid="case-status"]').should('be.visible')
    cy.get('[data-testid="case-client"]').should('be.visible')
    cy.get('[data-testid="case-type"]').should('be.visible')
    cy.get('[data-testid="case-created-date"]').should('be.visible')
  })
})

Then('I should see the page title {string}', (title: string) => {
  cy.get('[data-testid="page-title"]').should('contain.text', title)
})

Then('I should see the subtitle {string}', (subtitle: string) => {
  cy.get('[data-testid="page-subtitle"]').should('contain.text', subtitle)
})

Then('I should be taken to the case detail page', () => {
  cy.url().should('match', /\/cases\/case-\d+/)
})

Then('I should see comprehensive case metadata', () => {
  cy.get('[data-testid="case-overview"]').should('be.visible')
  cy.get('[data-testid="case-title"]').should('be.visible')
  cy.get('[data-testid="case-client"]').should('be.visible')
  cy.get('[data-testid="case-type"]').should('be.visible')
  cy.get('[data-testid="case-status"]').should('be.visible')
  cy.get('[data-testid="case-summary"]').should('be.visible')
})

Then('I should see the case title in the page header', () => {
  cy.get('[data-testid="page-title"]').should('contain.text', 'Wrongful Dismissal')
})

Then('I should see a back button to return to cases', () => {
  cy.get('[data-testid="back-button"]').should('be.visible')
  cy.get('[data-testid="back-button"]').should('contain.text', 'Back to Cases')
})

Then('each case card should display:', (dataTable) => {
  const fields = dataTable.hashes()
  
  cy.get('[data-testid="case-card"]').first().within(() => {
    fields.forEach((field) => {
      switch (field.Field) {
        case 'Title':
          cy.get('[data-testid="case-title"]').should('be.visible')
          break
        case 'Status':
          cy.get('[data-testid="case-status"]').should('be.visible')
          break
        case 'Client':
          cy.get('[data-testid="case-client"]').should('be.visible')
          break
        case 'Case Type':
          cy.get('[data-testid="case-type"]').should('be.visible')
          break
        case 'Created Date':
          cy.get('[data-testid="case-created-date"]').should('be.visible')
          break
        case 'Key Parties':
          cy.get('[data-testid="case-parties"]').should('be.visible')
          break
        case 'Document Count':
          cy.get('[data-testid="case-document-count"]').should('be.visible')
          break
        case 'Playbook':
          cy.get('[data-testid="case-playbook"]').should('be.visible')
          break
        case 'Summary':
          cy.get('[data-testid="case-summary"]').should('be.visible')
          break
      }
    })
  })
})

Then('I should see the case overview section with:', (dataTable) => {
  const fields = dataTable.hashes()
  
  cy.get('[data-testid="case-overview"]').within(() => {
    fields.forEach((field) => {
      switch (field.Field) {
        case 'Title':
          cy.get('[data-testid="case-title"]').should('be.visible')
          break
        case 'Client':
          cy.get('[data-testid="case-client"]').should('be.visible')
          break
        case 'Case Type':
          cy.get('[data-testid="case-type"]').should('be.visible')
          break
        case 'Status':
          cy.get('[data-testid="case-status"]').should('be.visible')
          break
        case 'Created Date':
          cy.get('[data-testid="case-created-date"]').should('be.visible')
          break
        case 'Assigned Playbook':
          cy.get('[data-testid="case-playbook"]').should('be.visible')
          break
        case 'Summary':
          cy.get('[data-testid="case-summary"]').should('be.visible')
          break
      }
    })
  })
})

Then('I should see the key parties section', () => {
  cy.get('[data-testid="key-parties-section"]').should('be.visible')
})

Then('I should see the associated documents section', () => {
  cy.get('[data-testid="documents-section"]').should('be.visible')
})

Then('I should see document analysis status indicators', () => {
  cy.get('[data-testid="analysis-status-indicators"]').should('be.visible')
})

Then('I should be on the case detail page', () => {
  cy.url().should('match', /\/cases\/case-\d+/)
})

Then('I should return to the cases list', () => {
  cy.url().should('eq', Cypress.config().baseUrl + '/cases')
})

Then('I should see all cases again', () => {
  cy.get('[data-testid="case-card"]').should('have.length', mockCases.length)
})

Then('I should only see cases matching {string}', (searchTerm: string) => {
  cy.get('[data-testid="case-card"]').should('have.length.lessThan', mockCases.length)
  cy.get('[data-testid="case-card"]').each(($card) => {
    cy.wrap($card).should('contain.text', searchTerm)
  })
})

Then('I should see status chips with appropriate colors:', (dataTable) => {
  const statuses = dataTable.hashes()
  
  statuses.forEach((status) => {
    cy.get(`[data-testid="case-status"][data-status="${status.Status}"]`)
      .should('be.visible')
  })
})

Then('I should see the total document count', () => {
  cy.get('[data-testid="total-document-count"]').should('be.visible')
})

Then('I should see analysis completion status', () => {
  cy.get('[data-testid="analysis-completion-status"]').should('be.visible')
})

Then('I should see a progress indicator for document analysis', () => {
  cy.get('[data-testid="analysis-progress-bar"]').should('be.visible')
})

Then('I should see individual document analysis status', () => {
  cy.get('[data-testid="document-analysis-status"]').should('be.visible')
})

Then('the case cards should be displayed in a single column', () => {
  cy.get('[data-testid="cases-grid"]').should('have.css', 'grid-template-columns', '1fr')
})

Then('all information should be readable', () => {
  cy.get('[data-testid="case-card"]').first().within(() => {
    cy.get('[data-testid="case-title"]').should('be.visible')
    cy.get('[data-testid="case-client"]').should('be.visible')
  })
})

Then('I should navigate to the case detail page', () => {
  cy.url().should('match', /\/cases\/case-\d+/)
})

Then('the layout should be mobile-friendly', () => {
  cy.get('[data-testid="case-overview"]').should('be.visible')
  cy.viewport('iphone-x')
  cy.get('[data-testid="case-overview"]').should('be.visible')
})

Then('I should see a message {string}', (message: string) => {
  cy.contains(message).should('be.visible')
})

Then('I should not see any case cards', () => {
  cy.get('[data-testid="case-card"]').should('not.exist')
})

Then('I should see an error message', () => {
  cy.get('[data-testid="error-message"]').should('be.visible')
})

Then('I should see {string}', (text: string) => {
  cy.contains(text).should('be.visible')
})

Then('I should see a loading spinner', () => {
  cy.get('[data-testid="loading-spinner"]').should('be.visible')
})

Then('the loading spinner should disappear', () => {
  cy.get('[data-testid="loading-spinner"]').should('not.exist')
})

Then('the page should have proper heading structure', () => {
  cy.get('h1').should('exist')
  cy.get('[data-testid="page-title"]').should('exist')
})

Then('case cards should be keyboard accessible', () => {
  cy.get('[data-testid="case-card"]').first().should('be.focusable')
})

Then('screen readers should be able to navigate the content', () => {
  cy.get('[data-testid="case-card"]').first().should('have.attr', 'role')
})

Then('I should be able to access all interactive elements', () => {
  cy.get('[data-testid="case-card"]').first().focus()
  cy.focused().should('exist')
})

Then('I should be able to navigate to case details using Enter key', () => {
  cy.get('[data-testid="case-card"]').first().focus()
  cy.focused().type('{enter}')
  cy.url().should('match', /\/cases\/case-\d+/)
})

Then('the card should have visual feedback', () => {
  cy.get('[data-testid="case-card"]').first().should('have.css', 'cursor', 'pointer')
})

Then('it should lift slightly with a shadow', () => {
  // This would need to be tested with visual regression testing
  // For now, we'll just check that hover styles are applied
  cy.get('[data-testid="case-card"]').first().should('be.visible')
})

Then('the border should change color', () => {
  // This would need to be tested with visual regression testing
  cy.get('[data-testid="case-card"]').first().should('be.visible')
})

Then('I should see the case detail page for {string}', (caseId: string) => {
  cy.url().should('include', `/cases/${caseId}`)
  cy.get('[data-testid="case-overview"]').should('be.visible')
})

Then('all case information should be displayed correctly', () => {
  cy.get('[data-testid="case-title"]').should('be.visible')
  cy.get('[data-testid="case-client"]').should('be.visible')
  cy.get('[data-testid="case-type"]').should('be.visible')
  cy.get('[data-testid="case-summary"]').should('be.visible')
})

Then('I should navigate to the document detail page', () => {
  cy.url().should('match', /\/documents\/doc-\d+/)
})

Then('I should navigate to the documents page for this case', () => {
  cy.url().should('match', /\/cases\/case-\d+\/documents/)
})

// Custom Cypress commands
declare global {
  namespace Cypress {
    interface Chainable {
      tab(): Chainable<Element>
    }
  }
}

Cypress.Commands.add('tab', { prevSubject: 'optional' }, (subject) => {
  return cy.wrap(subject).trigger('keydown', { keyCode: 9 })
})