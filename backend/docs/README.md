# AI Legal Platform API Documentation

Welcome to the AI Legal Platform API documentation. This API provides comprehensive legal case management capabilities with AI-powered document analysis.

## Quick Start

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://api.ailegalplatform.com`

### Interactive Documentation
- **Swagger UI**: `/docs` - Interactive API documentation with try-it-out functionality
- **ReDoc**: `/redoc` - Alternative documentation interface with better readability

### Health Check
```bash
GET /health
```

## API Overview

### Core Features
- **Case Management**: Create, retrieve, and manage legal cases
- **Document Analysis**: AI-powered analysis of legal documents
- **Statistics & Analytics**: Dashboard statistics and case insights
- **Legal Research**: AI-assisted legal research capabilities
- **Playbook Engine**: Automated legal workflow management

### Authentication
Currently, this API does not require authentication for demo purposes. In production, authentication will be implemented using JWT tokens.

### Rate Limiting
No rate limiting is currently implemented. This will be added in future versions.

## API Endpoints

### Cases API (`/cases`)
- `GET /cases` - Get all cases
- `GET /cases/{case_id}` - Get specific case
- `GET /cases/statistics` - Get case statistics

### Documents API (`/documents`)
- `GET /documents/cases/{case_id}/documents` - Get documents for a case
- `GET /documents/{document_id}` - Get specific document
- `GET /documents/{document_id}/analysis` - Get AI analysis for document

### Additional APIs
- `GET /playbooks` - Playbook management
- `GET /legal-research` - Legal research capabilities

## Data Models

### Case
Represents a legal case in the system with complete metadata, parties, and document associations.

### Document
Represents a legal document with metadata, content preview, and analysis status.

### DocumentAnalysis
AI-generated analysis results including extracted information, summaries, and confidence scores.

## Error Handling

The API uses standard HTTP status codes:
- `200` - Success
- `404` - Resource not found
- `500` - Internal server error

Error responses include detailed error messages in JSON format:
```json
{
  "detail": "Error description"
}
```

## Examples

See the interactive documentation at `/docs` for complete examples and try-it-out functionality.

## Support

For API support, please contact the development team at support@ailegalplatform.com.