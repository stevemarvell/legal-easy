# Data Models

This document describes the data models used in the AI Legal Platform API.

## Case Model

Represents a legal case in the system.

### Schema

```json
{
  "id": "string",
  "title": "string",
  "case_type": "string",
  "client_name": "string",
  "status": "string",
  "created_date": "datetime",
  "summary": "string",
  "key_parties": ["string"],
  "documents": ["string"],
  "playbook_id": "string"
}
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier for the case | `"case-001"` |
| `title` | string | Descriptive title of the case | `"Wrongful Dismissal - Sarah Chen vs TechCorp Solutions"` |
| `case_type` | string | Type of legal case | `"Employment Dispute"` |
| `client_name` | string | Name of the client | `"Sarah Chen"` |
| `status` | string | Current status of the case | `"Active"` |
| `created_date` | datetime | Date when the case was created | `"2024-01-15T09:00:00Z"` |
| `summary` | string | Brief summary of the case | `"Employee alleges wrongful dismissal..."` |
| `key_parties` | array[string] | List of key parties involved | `["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"]` |
| `documents` | array[string] | List of document IDs associated with this case | `["doc-001", "doc-002", "doc-003"]` |
| `playbook_id` | string | ID of the playbook used for this case type | `"employment-dispute"` |

### Enums

#### case_type
- `"Employment Dispute"`
- `"Contract Breach"`
- `"Debt Claim"`

#### status
- `"Active"`
- `"Under Review"`
- `"Resolved"`

### Example

```json
{
  "id": "case-001",
  "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
  "case_type": "Employment Dispute",
  "client_name": "Sarah Chen",
  "status": "Active",
  "created_date": "2024-01-15T09:00:00Z",
  "summary": "Employee alleges wrongful dismissal after reporting safety violations. Claims retaliation and seeks reinstatement plus damages. Company claims dismissal was due to performance issues and budget cuts.",
  "key_parties": [
    "Sarah Chen (Claimant)",
    "TechCorp Solutions Ltd. (Respondent)",
    "Marcus Rodriguez (HR Director)",
    "Jennifer Walsh (Direct Supervisor)"
  ],
  "documents": ["doc-001", "doc-002", "doc-003"],
  "playbook_id": "employment-dispute"
}
```

## CaseStatistics Model

Provides dashboard statistics about cases in the system.

### Schema

```json
{
  "total_cases": "integer",
  "active_cases": "integer",
  "resolved_cases": "integer",
  "under_review_cases": "integer",
  "recent_activity_count": "integer"
}
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `total_cases` | integer | Total number of cases in the system | `6` |
| `active_cases` | integer | Number of cases with 'Active' status | `3` |
| `resolved_cases` | integer | Number of cases with 'Resolved' status | `1` |
| `under_review_cases` | integer | Number of cases with 'Under Review' status | `2` |
| `recent_activity_count` | integer | Number of cases with activity in the last 30 days | `4` |

### Example

```json
{
  "total_cases": 6,
  "active_cases": 3,
  "resolved_cases": 1,
  "under_review_cases": 2,
  "recent_activity_count": 4
}
```

## Document Model

Represents a legal document in the system.

### Schema

```json
{
  "id": "string",
  "case_id": "string",
  "name": "string",
  "type": "string",
  "size": "integer",
  "upload_date": "datetime",
  "content_preview": "string",
  "analysis_completed": "boolean"
}
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier for the document | `"doc-001"` |
| `case_id` | string | ID of the case this document belongs to | `"case-001"` |
| `name` | string | Human-readable name of the document | `"Employment Contract - Sarah Chen"` |
| `type` | string | Type of document | `"Contract"` |
| `size` | integer | File size in bytes | `245760` |
| `upload_date` | datetime | Date when the document was uploaded | `"2024-01-15T09:30:00Z"` |
| `content_preview` | string | Preview of the document content | `"EMPLOYMENT AGREEMENT between..."` |
| `analysis_completed` | boolean | Whether AI analysis has been completed | `true` |

### Enums

#### type
- `"Contract"`
- `"Email"`
- `"Legal Brief"`
- `"Evidence"`

### Example

```json
{
  "id": "doc-001",
  "case_id": "case-001",
  "name": "Employment Contract - Sarah Chen",
  "type": "Contract",
  "size": 245760,
  "upload_date": "2024-01-15T09:30:00Z",
  "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen. Position: Senior Safety Engineer. Start Date: 15 March 2022. At-will employment with 30-day notice provision...",
  "analysis_completed": true
}
```

## DocumentAnalysis Model

Contains AI-generated analysis results for a document.

### Schema

```json
{
  "document_id": "string",
  "key_dates": ["date"],
  "parties_involved": ["string"],
  "document_type": "string",
  "summary": "string",
  "key_clauses": ["string"],
  "confidence_scores": {
    "string": "float"
  }
}
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `document_id` | string | ID of the analyzed document | `"doc-001"` |
| `key_dates` | array[date] | Important dates extracted from the document | `["2022-03-15", "2024-01-12"]` |
| `parties_involved` | array[string] | Parties mentioned in the document | `["Sarah Chen", "TechCorp Solutions Inc."]` |
| `document_type` | string | AI-determined document type | `"Employment Contract"` |
| `summary` | string | AI-generated summary of the document | `"At-will employment agreement..."` |
| `key_clauses` | array[string] | Important clauses or sections identified | `["At-will employment clause", "Safety reporting obligations"]` |
| `confidence_scores` | object | Confidence scores for different analysis aspects | `{"parties": 0.95, "dates": 0.98}` |

### Confidence Scores

The `confidence_scores` object contains floating-point values between 0.0 and 1.0 indicating the AI's confidence in different aspects of the analysis:

- `parties`: Confidence in party identification
- `dates`: Confidence in date extraction
- `contract_terms`: Confidence in contract term identification
- `key_clauses`: Confidence in key clause extraction
- `legal_analysis`: Confidence in legal analysis

### Example

```json
{
  "document_id": "doc-001",
  "key_dates": ["2022-03-15", "2024-01-12"],
  "parties_involved": [
    "Sarah Chen",
    "TechCorp Solutions Inc.",
    "Marcus Rodriguez",
    "Jennifer Walsh"
  ],
  "document_type": "Employment Contract",
  "summary": "At-will employment agreement for Senior Safety Engineer position with 30-day notice provision and standard benefits package. Contract includes specific safety reporting obligations and anti-retaliation protections.",
  "key_clauses": [
    "At-will employment clause with 30-day notice requirement",
    "Safety reporting obligations and whistleblower protections",
    "Confidentiality agreement with proprietary information restrictions",
    "Annual salary of $95,000 with performance review eligibility",
    "Standard benefits package including health insurance and 401(k)",
    "Equal employment opportunity and anti-discrimination provisions"
  ],
  "confidence_scores": {
    "parties": 0.95,
    "dates": 0.98,
    "contract_terms": 0.92,
    "key_clauses": 0.89,
    "legal_analysis": 0.87
  }
}
```

## KeyInformation Model

Extracted key information from documents for quick reference.

### Schema

```json
{
  "dates": ["date"],
  "parties": ["string"],
  "amounts": ["string"],
  "legal_concepts": ["string"],
  "confidence": "float"
}
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `dates` | array[date] | Important dates found in the document | `["2024-01-15", "2024-02-01"]` |
| `parties` | array[string] | Parties mentioned in the document | `["John Doe", "ABC Corp"]` |
| `amounts` | array[string] | Financial amounts mentioned | `["$50,000", "£25,000"]` |
| `legal_concepts` | array[string] | Legal concepts identified | `["breach of contract", "negligence"]` |
| `confidence` | float | Overall confidence score for the extraction (0.0-1.0) | `0.92` |

### Example

```json
{
  "dates": ["2024-01-15", "2024-02-01"],
  "parties": ["John Doe", "ABC Corp", "Legal Counsel"],
  "amounts": ["$50,000", "£25,000"],
  "legal_concepts": ["breach of contract", "negligence", "damages"],
  "confidence": 0.92
}
```

## Data Relationships

### Case → Documents
- A case can have multiple documents
- Each document belongs to exactly one case
- Documents are referenced by ID in the case's `documents` array

### Document → DocumentAnalysis
- Each document can have one analysis result
- Analysis is linked by `document_id`
- Analysis may not exist if `analysis_completed` is `false`

### Case → Playbook
- Each case is associated with a playbook via `playbook_id`
- Playbooks define the workflow and procedures for case types

## Validation Rules

### Case Validation
- `id` must be unique and non-empty
- `case_type` must be one of the allowed enum values
- `status` must be one of the allowed enum values
- `created_date` must be a valid ISO 8601 datetime
- `key_parties` must contain at least one party
- `documents` array can be empty but must be valid document IDs if present

### Document Validation
- `id` must be unique and non-empty
- `case_id` must reference an existing case
- `type` must be one of the allowed enum values
- `size` must be a positive integer
- `upload_date` must be a valid ISO 8601 datetime
- `analysis_completed` must be a boolean

### DocumentAnalysis Validation
- `document_id` must reference an existing document
- `key_dates` must contain valid ISO 8601 dates
- `confidence_scores` values must be between 0.0 and 1.0
- All arrays can be empty but must be valid arrays

## Future Enhancements

### Planned Model Extensions
- User authentication and authorization fields
- Document versioning and revision history
- Case collaboration and assignment features
- Advanced analytics and reporting models
- Integration with external legal databases

### API Versioning
- Models may evolve with API versions
- Backward compatibility will be maintained
- Deprecated fields will be clearly marked
- Migration guides will be provided for major changes