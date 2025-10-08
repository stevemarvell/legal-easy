import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'

Given('I am on the Legal Easy homepage', () => {
  cy.visit('/')
})

Given('the API response is delayed', () => {
  cy.intercept('GET', '**/random', (req) => {
    req.reply((res) => {
      res.delay(2000)
      res.send({ body: { value: 42 } })
    })
  }).as('delayedResponse')
})

Given('the API returns an error', () => {
  cy.intercept('GET', '**/random', { statusCode: 500 }).as('errorResponse')
})

Given('the API returns a {int} error', (statusCode: number) => {
  cy.intercept('GET', '**/random', { statusCode }).as('specificErrorResponse')
})

Given('I have previously fetched a random number', () => {
  cy.intercept('GET', '**/random', { body: { value: 25 } }).as('firstRequest')
  cy.get('button').contains('Get Random Number').click()
  cy.wait('@firstRequest')
  cy.get('.result').should('contain', '25')
})

Given('I am using a mobile device', () => {
  cy.viewport('iphone-x')
})

When('I click the "Get Random Number" button', () => {
  cy.intercept('GET', '**/random', { body: { value: 73 } }).as('randomRequest')
  cy.get('button').contains('Get Random Number').click()
})

When('I click the "Get Random Number" button again', () => {
  cy.intercept('GET', '**/random', { body: { value: 88 } }).as('secondRequest')
  cy.get('button').contains('Get Random Number').click()
})

When('the API responds', () => {
  cy.wait('@delayedResponse')
})

When('I navigate using keyboard', () => {
  cy.get('button').focus()
})

When('I tap the button', () => {
  cy.intercept('GET', '**/random', { body: { value: 55 } }).as('mobileRequest')
  cy.get('button').contains('Get Random Number').click()
})

Then('I should see a random number between 0 and 100', () => {
  cy.wait('@randomRequest')
  cy.get('.result').should('be.visible')
  cy.get('.result').shouldContainNumber()
})

Then('I should see a random number', () => {
  cy.get('.result').should('be.visible')
  cy.get('.result').shouldContainNumber()
})

Then('the button should be enabled again', () => {
  cy.get('button').should('not.be.disabled')
  cy.get('button').should('contain', 'Get Random Number')
})

Then('the button should be enabled', () => {
  cy.get('button').should('not.be.disabled')
})

Then('I should see "Loading..." text', () => {
  cy.get('button').should('contain', 'Loading...')
})

Then('the button should be disabled', () => {
  cy.get('button').should('be.disabled')
})

Then('I should see an error message', () => {
  cy.wait('@errorResponse')
  cy.get('.error').should('be.visible')
  cy.get('.error').should('contain', 'Error:')
})

Then('I should see "Error: HTTP {int}"', (statusCode: number) => {
  cy.wait('@specificErrorResponse')
  cy.get('.error').should('contain', `Error: HTTP ${statusCode}`)
})

Then('the previous result should be cleared', () => {
  cy.get('.result').should('not.contain', '25')
})

Then('I should see the new result', () => {
  cy.wait('@secondRequest')
  cy.get('.result').should('contain', '88')
})

Then('I should see the backend URL information', () => {
  cy.get('.backend-info').should('be.visible')
})

Then('it should contain "Backend:"', () => {
  cy.get('.backend-info').should('contain', 'Backend:')
})

Then('the page should have proper heading structure', () => {
  cy.get('h1').should('exist')
  cy.get('h1').should('contain', 'Legal Easy')
})

Then('the button should be keyboard accessible', () => {
  cy.get('button').should('be.visible')
  cy.get('button').focus()
  cy.focused().should('contain', 'Get Random Number')
})

Then('I should be able to trigger the button with Enter key', () => {
  cy.intercept('GET', '**/random', { body: { value: 99 } }).as('keyboardRequest')
  cy.focused().type('{enter}')
  cy.wait('@keyboardRequest')
  cy.get('.result').should('contain', '99')
})

Then('all elements should be visible and accessible', () => {
  cy.get('h1').should('be.visible')
  cy.get('button').should('be.visible')
  cy.get('.output').should('be.visible')
})

Then('it should work the same as clicking', () => {
  cy.wait('@mobileRequest')
  cy.get('.result').should('contain', '55')
})