# AI Legal Platform API Documentation

Welcome to the comprehensive documentation for the AI Legal Platform API.

## Quick Navigation

### 📚 Core Documentation
- **[API Overview](README.md)** - Get started with the API
- **[Data Models](data-models.md)** - Understand the data structures
- **[API Examples](api-examples.md)** - Practical usage examples
- **[Deployment Guide](deployment.md)** - Deploy to various environments

### 🚀 Interactive Documentation
- **[Swagger UI](/docs)** - Interactive API documentation with try-it-out functionality
- **[ReDoc](/redoc)** - Alternative documentation interface with better readability

### 🔗 Quick Links
- **[Health Check](/health)** - API health status
- **[API Root](/)** - API information and endpoints overview

## API Endpoints Overview

### Cases Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cases` | GET | Get all legal cases |
| `/cases/{case_id}` | GET | Get specific case details |
| `/cases/statistics` | GET | Get dashboard statistics |

### Document Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/documents/cases/{case_id}/documents` | GET | Get documents for a case |
| `/documents/{document_id}` | GET | Get specific document |
| `/documents/{document_id}/analysis` | GET | Get AI analysis for document |

### Additional Features
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/playbooks` | GET | Legal workflow management |
| `/legal-research` | GET | AI-assisted legal research |

## Key Features

### 🏛️ Legal Case Management
- Comprehensive case tracking and management
- Multi-party case support
- Status tracking and workflow management
- Integration with legal playbooks

### 📄 AI-Powered Document Analysis
- Automated document type classification
- Key information extraction (dates, parties, amounts)
- Legal clause identification
- Confidence scoring for analysis accuracy

### 📊 Analytics & Reporting
- Real-time case statistics
- Dashboard-ready metrics
- Activity tracking and reporting

### 🔍 Legal Research
- AI-assisted legal research capabilities
- Integration with legal databases
- Precedent and statute analysis

## Getting Started

### 1. Access the API
- **Base URL**: `http://localhost:8000` (development)
- **Production**: `https://api.ailegalplatform.com`

### 2. Explore Interactive Docs
Visit `/docs` for the Swagger UI interface where you can:
- Browse all available endpoints
- View request/response schemas
- Test API calls directly in the browser
- Download OpenAPI specification

### 3. Try Basic Endpoints

```bash
# Get API information
curl http://localhost:8000/

# Check API health
curl http://localhost:8000/health

# Get all cases
curl http://localhost:8000/cases

# Get case statistics
curl http://localhost:8000/cases/statistics
```

### 4. Explore the Data
The API comes with demo data including:
- 6 sample legal cases across different practice areas
- 21+ legal documents with AI analysis
- Comprehensive case statistics
- Real-world legal scenarios

## Authentication

Currently, the API operates without authentication for demo purposes. In production deployments, JWT-based authentication will be implemented.

## Rate Limiting

No rate limiting is currently implemented. This will be added in future versions based on usage patterns and requirements.

## Support & Feedback

- **Technical Issues**: Check the troubleshooting section in the deployment guide
- **API Questions**: Refer to the examples and data models documentation
- **Feature Requests**: Contact the development team

## Version Information

- **Current Version**: 1.0.0
- **API Specification**: OpenAPI 3.0
- **Framework**: FastAPI
- **Python Version**: 3.8+

## License

This API is released under the MIT License. See the license documentation for full details.

---

*Last updated: $(date)*
*For the most current API specification, visit the interactive documentation at `/docs`*