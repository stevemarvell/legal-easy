Feature: Random Number Generator
  As a user
  I want to get random numbers from the API
  So that I can use them for various purposes

  Background:
    Given I am on the Legal Easy homepage

  Scenario: Successfully fetch a random number
    When I click the "Get Random Number" button
    Then I should see a random number between 0 and 100
    And the button should be enabled again

  Scenario: Handle loading state
    Given the API response is delayed
    When I click the "Get Random Number" button
    Then I should see "Loading..." text
    And the button should be disabled
    When the API responds
    Then I should see a random number
    And the button should be enabled

  Scenario: Handle API errors
    Given the API returns an error
    When I click the "Get Random Number" button
    Then I should see an error message
    And the button should be enabled again

  Scenario: Clear previous results
    Given I have previously fetched a random number
    When I click the "Get Random Number" button again
    Then the previous result should be cleared
    And I should see the new result

  Scenario: Display backend information
    Then I should see the backend URL information
    And it should contain "Backend:"

  Scenario Outline: Handle different API error codes
    Given the API returns a <status_code> error
    When I click the "Get Random Number" button
    Then I should see "Error: HTTP <status_code>"

    Examples:
      | status_code |
      | 400         |
      | 404         |
      | 500         |
      | 503         |

  Scenario: Accessibility compliance
    Then the page should have proper heading structure
    And the button should be keyboard accessible
    When I navigate using keyboard
    Then I should be able to trigger the button with Enter key

  Scenario: Mobile responsiveness
    Given I am using a mobile device
    Then all elements should be visible and accessible
    When I tap the button
    Then it should work the same as clicking