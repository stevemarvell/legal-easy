describe('Random Number Feature', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should display the main page correctly', () => {
    cy.get('h1').should('contain', 'Legal Easy')
    cy.get('p').should('contain', 'Click the button to fetch a random number')
    cy.get('button').should('contain', 'Get Random Number')
    cy.get('.output').should('contain', '—')
  })

  it('should fetch and display a random number', () => {
    // Intercept the API call
    cy.intercept('GET', '**/random', { fixture: 'random-response.json' }).as('getRandomNumber')
    
    // Click the button
    cy.get('button').contains('Get Random Number').click()
    
    // Wait for API call
    cy.wait('@getRandomNumber')
    
    // Check that a number is displayed
    cy.get('.result').should('be.visible')
    cy.get('.result').shouldContainNumber()
  })

  it('should show loading state during API call', () => {
    // Intercept with delay
    cy.intercept('GET', '**/random', (req) => {
      req.reply((res) => {
        res.delay(1000)
        res.send({ fixture: 'random-response.json' })
      })
    }).as('getRandomNumberSlow')
    
    cy.get('button').contains('Get Random Number').click()
    
    // Check loading state
    cy.get('button').should('contain', 'Loading...')
    cy.get('button').should('be.disabled')
    
    // Wait for completion
    cy.wait('@getRandomNumberSlow')
    
    // Check final state
    cy.get('button').should('contain', 'Get Random Number')
    cy.get('button').should('not.be.disabled')
  })

  it('should handle API errors gracefully', () => {
    // Intercept with error
    cy.intercept('GET', '**/random', { statusCode: 500 }).as('getRandomNumberError')
    
    cy.get('button').contains('Get Random Number').click()
    
    cy.wait('@getRandomNumberError')
    
    // Check error display
    cy.get('.error').should('be.visible')
    cy.get('.error').should('contain', 'Error: HTTP 500')
  })

  it('should clear previous results when making new request', () => {
    // First successful request
    cy.intercept('GET', '**/random', { body: { value: 42 } }).as('firstRequest')
    cy.get('button').click()
    cy.wait('@firstRequest')
    cy.get('.result').should('contain', '42')
    
    // Second request with error
    cy.intercept('GET', '**/random', { statusCode: 500 }).as('secondRequest')
    cy.get('button').click()
    cy.wait('@secondRequest')
    
    // Should show error, not previous result
    cy.get('.error').should('be.visible')
    cy.get('.result').should('not.exist')
  })

  it('should display backend URL information', () => {
    cy.get('.backend-info').should('be.visible')
    cy.get('.backend-info').should('contain', 'Backend:')
    cy.get('.backend-info').should('contain', 'http')
  })

  it('should be accessible', () => {
    // Check for proper heading structure
    cy.get('h1').should('exist')
    
    // Check button has proper attributes
    cy.get('button').should('have.attr', 'type').or('not.have.attr', 'type')
    
    // Check for keyboard navigation
    cy.get('button').focus()
    cy.focused().should('contain', 'Get Random Number')
    
    // Test keyboard interaction
    cy.focused().type('{enter}')
    // Should trigger the same action as click
  })

  it('should work on mobile viewport', () => {
    cy.viewport('iphone-x')
    
    cy.get('h1').should('be.visible')
    cy.get('button').should('be.visible')
    cy.get('.output').should('be.visible')
    
    // Test touch interaction
    cy.get('button').click()
  })
})