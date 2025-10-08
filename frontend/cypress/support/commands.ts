/// <reference types="cypress" />

// Custom command to check if element contains a number
Cypress.Commands.add('shouldContainNumber', { prevSubject: true }, (subject) => {
  cy.wrap(subject).should(($el) => {
    const text = $el.text()
    const number = parseInt(text, 10)
    expect(number).to.be.a('number')
    expect(number).to.be.at.least(0)
    expect(number).to.be.at.most(100)
  })
})

// Custom command to wait for API response
Cypress.Commands.add('waitForApiResponse', (endpoint: string) => {
  cy.intercept('GET', `**${endpoint}`).as('apiRequest')
  cy.wait('@apiRequest')
})