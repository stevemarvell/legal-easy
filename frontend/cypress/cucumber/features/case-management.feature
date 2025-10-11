Feature: Case Management - View Cases
  As a legal professional
  I want to view and navigate through legal cases
  So that I can manage my caseload effectively

  Background:
    Given the backend API is available
    And I am on the Legal Easy application

  Scenario: View case list
    Given there are cases in the system
    When I navigate to the cases page
    Then I should see a list of cases
    And each case should display basic information
    And I should see the page title "Cases"
    And I should see the subtitle "Manage and track all legal cases"

  Scenario: View case details
    Given there are cases in the system
    When I navigate to the cases page
    And I click on a case card
    Then I should be taken to the case detail page
    And I should see comprehensive case metadata
    And I should see the case title in the page header
    And I should see a back button to return to cases

  Scenario: Case list displays required metadata
    Given there are cases in the system
    When I navigate to the cases page
    Then each case card should display:
      | Field | Description |
      | Title | Case title with primary styling |
      | Status | Status chip with appropriate color |
      | Client | Client name with person icon |
      | Case Type | Case type with gavel icon |
      | Created Date | Creation date with schedule icon |
      | Key Parties | List of parties with group icon |
      | Document Count | Number of documents with document icon |
      | Playbook | Assigned playbook with playbook icon |
      | Summary | Case summary (truncated if long) |

  Scenario: Case detail page displays comprehensive information
    Given there is a case with ID "case-001"
    When I navigate to the case detail page for "case-001"
    Then I should see the case overview section with:
      | Field | Description |
      | Title | Full case title |
      | Client | Client name |
      | Case Type | Type of legal case |
      | Status | Current case status |
      | Created Date | When the case was created |
      | Assigned Playbook | Which playbook is being used |
      | Summary | Full case summary |
    And I should see the key parties section
    And I should see the associated documents section
    And I should see document analysis status indicators

  Scenario: Navigate between case list and detail views
    Given there are cases in the system
    When I navigate to the cases page
    And I click on the first case
    Then I should be on the case detail page
    When I click the back button
    Then I should return to the cases list
    And I should see all cases again

  Scenario: Search functionality in case list
    Given there are multiple cases in the system
    When I navigate to the cases page
    And I enter "Employment" in the search box
    Then I should only see cases matching "Employment"
    When I clear the search box
    Then I should see all cases again

  Scenario: Case status indicators
    Given there are cases with different statuses
    When I navigate to the cases page
    Then I should see status chips with appropriate colors:
      | Status | Color |
      | Active | Success (green) |
      | Under Review | Warning (orange) |
      | Resolved | Info (blue) |

  Scenario: Document count and analysis status
    Given there is a case with documents
    When I navigate to the case detail page
    Then I should see the total document count
    And I should see analysis completion status
    And I should see a progress indicator for document analysis
    And I should see individual document analysis status

  Scenario: Responsive design on mobile
    Given I am using a mobile device
    And there are cases in the system
    When I navigate to the cases page
    Then the case cards should be displayed in a single column
    And all information should be readable
    When I tap on a case
    Then I should navigate to the case detail page
    And the layout should be mobile-friendly

  Scenario: Error handling for missing cases
    Given there are no cases in the system
    When I navigate to the cases page
    Then I should see a message "No cases found."
    And I should not see any case cards

  Scenario: Error handling for API failures
    Given the cases API is unavailable
    When I navigate to the cases page
    Then I should see an error message
    And I should see "Failed to load cases. Please try again."

  Scenario: Loading states
    Given the cases API has a delayed response
    When I navigate to the cases page
    Then I should see a loading spinner
    When the API responds
    Then I should see the case list
    And the loading spinner should disappear

  Scenario: Accessibility compliance
    Given there are cases in the system
    When I navigate to the cases page
    Then the page should have proper heading structure
    And case cards should be keyboard accessible
    And screen readers should be able to navigate the content
    When I use keyboard navigation
    Then I should be able to access all interactive elements
    And I should be able to navigate to case details using Enter key

  Scenario: Case card hover effects
    Given there are cases in the system
    When I navigate to the cases page
    And I hover over a case card
    Then the card should have visual feedback
    And it should lift slightly with a shadow
    And the border should change color

  Scenario: Direct URL navigation to case details
    Given there is a case with ID "case-001"
    When I navigate directly to "/cases/case-001"
    Then I should see the case detail page for "case-001"
    And all case information should be displayed correctly

  Scenario: Case documents navigation
    Given there is a case with documents
    When I am on the case detail page
    And I click on a document name
    Then I should navigate to the document detail page
    When I click "View All Documents"
    Then I should navigate to the documents page for this case