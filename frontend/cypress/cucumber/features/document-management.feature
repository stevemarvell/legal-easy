Feature: Document Management - View and Analyze Documents
  As a legal professional
  I want to view and analyze legal documents
  So that I can extract key information and insights from case documents

  Background:
    Given the backend API is available
    And I am on the Legal Easy application

  Scenario: View document list in grid view
    Given there are documents in the system
    When I navigate to the documents page
    Then I should see documents displayed as cards
    And each document card should display basic information
    And I should see the page title "All Documents"

  Scenario: View document list in case context
    Given there is a case with documents
    When I navigate to the case documents page
    Then I should see the case documents
    And I should see a toggle between list and grid view
    And I should see the case context in the page title

  Scenario: Navigate to document details from grid
    Given there are documents in the system
    When I navigate to the documents page
    And I click on a document card
    Then I should be taken to the document detail page
    And I should see comprehensive document information
    And I should see the document content and analysis

  Scenario: Navigate to document details from case context
    Given there is a case with documents
    When I navigate to the case documents page
    And I click on a document in the list
    Then I should be taken to the document detail page with case context
    And I should see breadcrumbs showing the case path

  Scenario: Document card displays required metadata
    Given there are documents in the system
    When I navigate to the documents page
    Then each document card should display:
      | Field | Description |
      | Title | Document name with icon |
      | Type | Document type with appropriate icon |
      | Size | File size in human-readable format |
      | Upload Date | When the document was uploaded |
      | Analysis Status | Whether analysis is completed or pending |
      | Content Preview | Preview of document content |

  Scenario: Document analysis workflow
    Given there is an unanalyzed document
    When I navigate to the document detail page
    And I click the "Analyze Document" button
    Then the document analysis should start
    And I should see analysis results when complete
    And the document status should update to "Analyzed"

  Scenario: View document analysis results
    Given there is an analyzed document
    When I navigate to the document detail page
    Then I should see the analysis results including:
      | Field | Description |
      | Key Dates | Important dates extracted from document |
      | Parties Involved | People and organizations mentioned |
      | Document Type | AI-determined document classification |
      | Summary | AI-generated summary of content |
      | Key Clauses | Important clauses or sections |
      | Confidence Scores | Analysis confidence levels |

  Scenario: Document search functionality
    Given there are multiple documents in the system
    When I navigate to the documents page
    And I enter "contract" in the search box
    Then I should only see documents matching "contract"
    When I clear the search box
    Then I should see all documents again

  Scenario: Document analysis status indicators
    Given there are documents with different analysis statuses
    When I navigate to the documents page
    Then I should see status indicators with appropriate colors:
      | Status | Color | Icon |
      | Analyzed | Success (green) | CheckCircle |
      | Pending | Warning (orange) | Schedule |

  Scenario: Switch between list and grid views
    Given there is a case with documents
    When I navigate to the case documents page
    And I click the grid view toggle
    Then I should see documents in grid layout
    When I click the list view toggle
    Then I should see documents in list layout with document viewer

  Scenario: Document type icons and categorization
    Given there are documents of different types
    When I navigate to the documents page
    Then I should see appropriate icons for each document type:
      | Type | Icon |
      | Contract | Assignment |
      | Email | Email |
      | Legal Brief | Gavel |
      | Evidence | Folder |

  Scenario: Responsive design for document grid
    Given I am using a mobile device
    And there are documents in the system
    When I navigate to the documents page
    Then the document cards should be displayed in a single column
    And all information should be readable
    When I tap on a document
    Then I should navigate to the document detail page

  Scenario: Error handling for document analysis
    Given there is a document that fails analysis
    When I navigate to the document detail page
    And I click the "Analyze Document" button
    Then I should see an error message
    And the document status should remain "Pending"
    And I should be able to retry the analysis

  Scenario: Document content display
    Given there is a document with content
    When I navigate to the document detail page
    Then I should see the full document content
    And I should see document metadata
    And I should see analysis results if available

  Scenario: Navigation breadcrumbs
    Given there is a case with documents
    When I navigate to a document detail page from case context
    Then I should see breadcrumbs showing:
      | Level | Label |
      | 1 | Dashboard |
      | 2 | Cases |
      | 3 | Case {case_id} |
      | 4 | Documents |
      | 5 | {document_name} |

  Scenario: Document analysis confidence indicators
    Given there is an analyzed document with confidence scores
    When I navigate to the document detail page
    Then I should see confidence scores for different analysis aspects
    And I should see overall confidence level
    And I should see uncertainty flags if confidence is low

  Scenario: Bulk document operations
    Given there are multiple unanalyzed documents in a case
    When I navigate to the case documents page
    And I click "Analyze All Pending"
    Then all pending documents should be queued for analysis
    And I should see progress indicators for each document

  Scenario: Document filtering and sorting
    Given there are documents with different types and statuses
    When I navigate to the documents page
    Then I should see filter options for:
      | Filter | Options |
      | Type | Contract, Email, Legal Brief, Evidence |
      | Status | Analyzed, Pending |
      | Date Range | Last 7 days, Last 30 days, Custom |

  Scenario: Document analysis history
    Given there is a document that has been analyzed multiple times
    When I navigate to the document detail page
    Then I should see analysis history
    And I should be able to compare different analysis results
    And I should see timestamps for each analysis

  Scenario: Document sharing and export
    Given there is an analyzed document
    When I navigate to the document detail page
    Then I should see options to:
      | Action | Description |
      | Export Analysis | Download analysis results as PDF/JSON |
      | Share Document | Generate shareable link |
      | Print Summary | Print document summary and analysis |

  Scenario: Accessibility compliance for documents
    Given there are documents in the system
    When I navigate to the documents page
    Then the page should have proper heading structure
    And document cards should be keyboard accessible
    And screen readers should be able to navigate the content
    When I use keyboard navigation
    Then I should be able to access all interactive elements
    And I should be able to navigate to document details using Enter key