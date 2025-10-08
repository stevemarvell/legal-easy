# OpenAPI Specification

The AI Legal Platform API follows the OpenAPI 3.0 specification and provides comprehensive documentation through multiple interfaces.

## Accessing the OpenAPI Specification

### Interactive Documentation

1. **Swagger UI** - `/docs`
   - Full interactive documentation
   - Try-it-out functionality for all endpoints
   - Request/response examples
   - Schema validation
   - Download OpenAPI JSON/YAML

2. **ReDoc** - `/redoc`
   - Clean, readable documentation
   - Better for reference and reading
   - Hierarchical navigation
   - Code samples in multiple languages

### Raw Specification

- **JSON Format**: `/openapi.json`
- **YAML Format**: Available through Swagger UI download

## API Information

```yaml
openapi: 3.0.2
info:
  title: AI Legal Platform API
  description: |
    ## AI-Powered Legal Case Management and Document Analysis API

    This API provides comprehensive legal case management capabilities with AI-powered document analysis.
    
    ### Key Features:
    - **Case Management**: Create, retrieve, and manage legal cases
    - **Document Analysis**: AI-powered analysis of legal documents
    - **Statistics & Analytics**: Dashboard statistics and case insights
    - **Legal Research**: AI-assisted legal research capabilities
    - **Playbook Engine**: Automated legal workflow management
  version: 1.0.0
  contact:
    name: AI Legal Platform Team
    email: support@ailegalplatform.com
  license:
    name: MIT License
    url: https://opensource.org/licenses/MIT
servers:
  - url: http://localhost:8000
    description: Development server
  - url: https://api.ailegalplatform.com
    description: Production server
```

## Tags and Organization

The API endpoints are organized into logical groups:

### Cases
- **Description**: Legal case management operations
- **Endpoints**: `/cases/*`
- **Operations**: List cases, get case details, case statistics

### Documents
- **Description**: Document management and AI analysis
- **Endpoints**: `/documents/*`
- **Operations**: List documents, get document details, AI analysis

## Schema Definitions

### Core Models

#### Case Schema
```yaml
Case:
  type: object
  required:
    - id
    - title
    - case_type
    - client_name
    - status
    - created_date
    - summary
    - key_parties
    - documents
    - playbook_id
  properties:
    id:
      type: string
      description: Unique identifier for the case
      example: case-001
    title:
      type: string
      description: Descriptive title of the case
      example: Wrongful Dismissal - Sarah Chen vs TechCorp Solutions
    case_type:
      type: string
      description: Type of legal case
      enum:
        - Employment Dispute
        - Contract Breach
        - Debt Claim
      example: Employment Dispute
    # ... additional properties
```

#### Document Schema
```yaml
Document:
  type: object
  required:
    - id
    - case_id
    - name
    - type
    - size
    - upload_date
    - content_preview
    - analysis_completed
  properties:
    id:
      type: string
      description: Unique identifier for the document
      example: doc-001
    case_id:
      type: string
      description: ID of the case this document belongs to
      example: case-001
    # ... additional properties
```

## Response Schemas

### Success Responses

All successful responses follow consistent patterns:

- **200 OK**: Successful retrieval
- **Content-Type**: `application/json`
- **Schema**: Defined response models

### Error Responses

```yaml
HTTPError:
  type: object
  properties:
    detail:
      type: string
      description: Error message
      example: Case with ID case-999 not found
```

Common error status codes:
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Request/Response Examples

### Get All Cases

**Request:**
```http
GET /cases HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "case-001",
    "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
    "case_type": "Employment Dispute",
    "client_name": "Sarah Chen",
    "status": "Active",
    "created_date": "2024-01-15T09:00:00Z",
    "summary": "Employee alleges wrongful dismissal...",
    "key_parties": ["Sarah Chen (Claimant)", "TechCorp Solutions Ltd. (Respondent)"],
    "documents": ["doc-001", "doc-002", "doc-003"],
    "playbook_id": "employment-dispute"
  }
]
```

### Get Document Analysis

**Request:**
```http
GET /documents/doc-001/analysis HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "document_id": "doc-001",
  "key_dates": ["2022-03-15", "2024-01-12"],
  "parties_involved": ["Sarah Chen", "TechCorp Solutions Inc."],
  "document_type": "Employment Contract",
  "summary": "At-will employment agreement for Senior Safety Engineer position...",
  "key_clauses": ["At-will employment clause", "Safety reporting obligations"],
  "confidence_scores": {
    "parties": 0.95,
    "dates": 0.98,
    "contract_terms": 0.92
  }
}
```

## Security Schemes

Currently, no authentication is required. Future versions will implement:

```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
    description: JWT token for API authentication
```

## Extensions and Customizations

### Custom Headers

The API may include custom headers in responses:
- `X-API-Version`: API version
- `X-Request-ID`: Unique request identifier
- `X-Rate-Limit-*`: Rate limiting information (future)

### Vendor Extensions

Custom OpenAPI extensions used:
- `x-code-samples`: Code examples in multiple languages
- `x-response-examples`: Additional response examples
- `x-internal`: Internal-only endpoints (if any)

## Validation Rules

### Request Validation
- All required fields must be present
- Enum values must match allowed options
- Date formats must be ISO 8601
- Numeric values must be within specified ranges

### Response Validation
- All responses conform to defined schemas
- Optional fields may be null or omitted
- Arrays are always valid arrays (may be empty)

## Code Generation

The OpenAPI specification can be used to generate client libraries:

### Supported Generators
- **JavaScript/TypeScript**: Using openapi-generator or swagger-codegen
- **Python**: Using openapi-generator
- **Java**: Using openapi-generator
- **C#**: Using NSwag or openapi-generator
- **Go**: Using openapi-generator
- **PHP**: Using openapi-generator

### Example Generation Commands

```bash
# Generate TypeScript client
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-fetch \
  -o ./generated-client

# Generate Python client
openapi-generator generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o ./python-client
```

## Testing with OpenAPI

### Schema Validation Testing

```python
import requests
import jsonschema

# Get OpenAPI spec
spec = requests.get("http://localhost:8000/openapi.json").json()

# Get API response
response = requests.get("http://localhost:8000/cases")
data = response.json()

# Validate against schema
schema = spec["components"]["schemas"]["Case"]
jsonschema.validate(data[0], schema)
```

### Contract Testing

Use tools like Pact or Dredd for contract testing:

```bash
# Install Dredd
npm install -g dredd

# Run contract tests
dredd http://localhost:8000/openapi.json http://localhost:8000
```

## Specification Maintenance

### Version Management
- Semantic versioning for API versions
- Backward compatibility considerations
- Deprecation notices for removed features

### Documentation Updates
- Keep examples current with actual API behavior
- Update schemas when models change
- Maintain accurate descriptions and metadata

### Quality Assurance
- Validate OpenAPI specification syntax
- Test all documented examples
- Ensure response schemas match actual responses

## Tools and Utilities

### OpenAPI Tools
- **Swagger Editor**: Online editor for OpenAPI specs
- **Swagger Inspector**: API testing tool
- **OpenAPI Generator**: Client/server code generation
- **Spectral**: OpenAPI linting and validation

### Integration Tools
- **Postman**: Import OpenAPI specs for testing
- **Insomnia**: REST client with OpenAPI support
- **Bruno**: Lightweight API client
- **HTTPie**: Command-line HTTP client

## Best Practices

### Documentation
- Use clear, descriptive summaries and descriptions
- Provide realistic examples
- Include error scenarios
- Document all parameters and responses

### Schema Design
- Use consistent naming conventions
- Define reusable components
- Include validation rules
- Provide meaningful examples

### Maintenance
- Keep documentation in sync with code
- Version specifications appropriately
- Test documentation examples regularly
- Gather feedback from API consumers