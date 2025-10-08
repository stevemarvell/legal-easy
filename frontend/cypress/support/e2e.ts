// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Add custom assertions
declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to check if element contains number
       * @example cy.get('[data-testid="output"]').shouldContainNumber()
       */
      shouldContainNumber(): Chainable<Element>
      
      /**
       * Custom command to wait for API response
       * @example cy.waitForApiResponse('/random')
       */
      waitForApiResponse(endpoint: string): Chainable<Element>
    }
  }
}