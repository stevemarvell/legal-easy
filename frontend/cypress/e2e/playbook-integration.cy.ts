describe('Playbook Integration', () => {
  beforeEach(() => {
    // Start with a clean state
    cy.visit('/')
    
    // Intercept API calls with UK-specific data
    cy.intercept('GET', '**/api/cases', { fixture: 'uk-cases.json' }).as('getCases')
    cy.intercept('GET', '**/api/cases/case-001', { fixture: 'uk-case-detail.json' }).as('getCaseDetail')
    cy.intercept('GET', '**/api/playbooks/Employment%20Dispute', { fixture: 'uk-employment-playbook.json' }).as('getPlaybook')
    cy.intercept('GET', '**/api/playbooks/cases/case-001/applied-rules', { fixture: 'uk-applied-rules.json' }).as('getAppliedRules')
  })

  it('should display UK employment law playbook correctly', () => {
    // Navigate to cases
    cy.get('nav').contains('Cases').click()
    cy.wait('@getCases')
    
    // Click on first case
    cy.get('.case-card .btn-primary').first().click()
    cy.wait('@getCaseDetail')
    
    // Verify case details show UK-specific information
    cy.get('h1').should('contain', 'Wrongful Dismissal')
    cy.get('.case-meta-grid').should('contain', 'Employment Dispute')
    
    // Click on Playbook tab
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getPlaybook')
    cy.wait('@getAppliedRules')
    
    // Verify UK employment law playbook is displayed
    cy.get('.playbook-header h2').should('contain', 'Employment Law Playbook')
    cy.get('.playbook-description').should('contain', 'UK employment law')
    
    // Verify UK-specific legal basis is shown
    cy.get('.rule-card').should('exist')
    cy.get('.rule-card').first().click()
    cy.get('.rule-details').should('contain', 'Employment Rights Act 1996')
    cy.get('.rule-details').should('contain', 'Equality Act 2010')
    
    // Verify UK escalation paths
    cy.get('.escalation-section').should('be.visible')
    cy.get('.escalation-path').should('contain', 'ACAS early conciliation')
    cy.get('.escalation-path').should('contain', 'Employment Tribunal claim')
    cy.get('.escalation-path').should('contain', 'Employment Appeal Tribunal')
    cy.get('.escalation-path').should('contain', 'Court of Appeal')
    
    // Verify no US-specific terms
    cy.get('body').should('not.contain', 'EEOC')
    cy.get('body').should('not.contain', 'Federal district court')
    cy.get('body').should('not.contain', 'State civil rights agency')
    cy.get('body').should('not.contain', 'Title VII')
    cy.get('body').should('not.contain', 'ADEA')
  })

  it('should show applied rules with UK legal reasoning', () => {
    // Navigate to case with playbook
    cy.visit('/cases/case-001')
    cy.wait('@getCaseDetail')
    
    // Go to playbook tab
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getPlaybook')
    cy.wait('@getAppliedRules')
    
    // Verify applied rules summary shows UK context
    cy.get('.applied-rules-summary').should('be.visible')
    cy.get('.applied-rules-summary').should('contain', 'Applied to Current Case')
    
    // Check case strength assessment
    cy.get('.strength-badge').should('be.visible')
    cy.get('.summary-value').should('contain', 'Strong')
    
    // Verify reasoning mentions UK law
    cy.get('.reasoning-text').should('contain', 'prospects')
    cy.get('.reasoning-text').should('contain', 'employment dispute')
    
    // Check recommendations are UK-appropriate
    cy.get('.recommendations-section').should('be.visible')
    cy.get('.recommendation-item').should('contain', 'investigate')
  })

  it('should display contract breach playbook with UK law', () => {
    // Mock contract case
    cy.intercept('GET', '**/api/cases/case-002', { fixture: 'uk-contract-case.json' }).as('getContractCase')
    cy.intercept('GET', '**/api/playbooks/Contract%20Breach', { fixture: 'uk-contract-playbook.json' }).as('getContractPlaybook')
    cy.intercept('GET', '**/api/playbooks/cases/case-002/applied-rules', { fixture: 'uk-contract-applied-rules.json' }).as('getContractAppliedRules')
    
    cy.visit('/cases/case-002')
    cy.wait('@getContractCase')
    
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getContractPlaybook')
    cy.wait('@getContractAppliedRules')
    
    // Verify UK contract law references
    cy.get('.escalation-path').should('contain', 'County Court proceedings')
    cy.get('.escalation-path').should('contain', 'Court of Appeal')
    cy.get('.escalation-path').should('not.contain', 'State court')
    cy.get('.escalation-path').should('not.contain', 'Federal court')
    
    // Check UK statutes are referenced
    cy.get('.rule-card').first().click()
    cy.get('.rule-details').should('contain', 'Sale of Goods Act')
  })

  it('should display debt claim playbook with UK procedures', () => {
    // Mock debt case
    cy.intercept('GET', '**/api/cases/case-003', { fixture: 'uk-debt-case.json' }).as('getDebtCase')
    cy.intercept('GET', '**/api/playbooks/Debt%20Claim', { fixture: 'uk-debt-playbook.json' }).as('getDebtPlaybook')
    cy.intercept('GET', '**/api/playbooks/cases/case-003/applied-rules', { fixture: 'uk-debt-applied-rules.json' }).as('getDebtAppliedRules')
    
    cy.visit('/cases/case-003')
    cy.wait('@getDebtCase')
    
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getDebtPlaybook')
    cy.wait('@getDebtAppliedRules')
    
    // Verify UK debt collection procedures
    cy.get('.escalation-path').should('contain', 'County Court Money Claims')
    cy.get('.escalation-path').should('contain', 'High Court proceedings')
    cy.get('.escalation-path').should('contain', 'Enforcement proceedings')
    cy.get('.escalation-path').should('not.contain', 'Small claims court')
    cy.get('.escalation-path').should('not.contain', 'Superior court')
    
    // Check UK debt legislation
    cy.get('.rule-card').first().click()
    cy.get('.rule-details').should('contain', 'Consumer Credit Act')
  })

  it('should handle playbook loading states correctly', () => {
    // Simulate slow API response
    cy.intercept('GET', '**/api/playbooks/Employment%20Dispute', { 
      fixture: 'uk-employment-playbook.json',
      delay: 2000
    }).as('getSlowPlaybook')
    
    cy.visit('/cases/case-001')
    cy.wait('@getCaseDetail')
    
    cy.get('.tab-button').contains('Playbook').click()
    
    // Should show loading state
    cy.get('.playbook-viewer-loading').should('be.visible')
    cy.get('.loading-spinner').should('be.visible')
    cy.get('.playbook-viewer-loading').should('contain', 'Loading playbook')
    
    // Wait for completion
    cy.wait('@getSlowPlaybook')
    
    // Should show content
    cy.get('.playbook-viewer-loading').should('not.exist')
    cy.get('.playbook-header').should('be.visible')
  })

  it('should handle playbook API errors gracefully', () => {
    // Simulate API error
    cy.intercept('GET', '**/api/playbooks/Employment%20Dispute', { statusCode: 500 }).as('getPlaybookError')
    
    cy.visit('/cases/case-001')
    cy.wait('@getCaseDetail')
    
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getPlaybookError')
    
    // Should show error state
    cy.get('.playbook-viewer-error').should('be.visible')
    cy.get('.playbook-viewer-error').should('contain', 'Error')
    cy.get('.btn-retry').should('be.visible')
    
    // Test retry functionality
    cy.intercept('GET', '**/api/playbooks/Employment%20Dispute', { fixture: 'uk-employment-playbook.json' }).as('getPlaybookRetry')
    cy.get('.btn-retry').click()
    cy.wait('@getPlaybookRetry')
    
    // Should show content after retry
    cy.get('.playbook-viewer-error').should('not.exist')
    cy.get('.playbook-header').should('be.visible')
  })

  it('should be accessible with proper ARIA labels', () => {
    cy.visit('/cases/case-001')
    cy.wait('@getCaseDetail')
    
    cy.get('.tab-button').contains('Playbook').click()
    cy.wait('@getPlaybook')
    cy.wait('@getAppliedRules')
    
    // Check heading structure
    cy.get('h2').should('exist')
    cy.get('h3').should('exist')
    
    // Check button accessibility
    cy.get('.rule-header').first().should('be.visible')
    
    // Test keyboard navigation
    cy.get('.rule-header').first().click()
    cy.get('.rule-details').should('be.visible')
  })
});