# AI Legal Platform - Project Structure

This document outlines the project structure for the AI Legal Platform demo application.

## Backend Structure (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/                 # Pydantic data models
│   │   ├── __init__.py
│   │   ├── case.py            # Case and CaseStatistics models
│   │   ├── document.py        # Document and DocumentAnalysis models
│   │   ├── playbook.py        # Playbook and related models
│   │   └── legal_research.py  # Search and RAG models
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── case_service.py    # Case management service
│   │   ├── document_service.py # Document management service
│   │   ├── ai_analysis_service.py # AI analysis service
│   │   ├── rag_service.py     # RAG-based legal research
│   │   └── playbook_engine.py # Playbook application engine
│   ├── api/                   # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── cases.py           # Case endpoints
│   │   ├── documents.py       # Document endpoints
│   │   ├── playbooks.py       # Playbook endpoints
│   │   └── legal_research.py  # Legal research endpoints
│   └── data/                  # Demo data files
│       ├── __init__.py
│       ├── demo_cases.json    # Sample legal cases
│       ├── demo_documents.json # Sample documents
│       └── demo_playbooks.json # Case type playbooks
├── main.py                    # FastAPI application entry point
└── requirements.txt           # Python dependencies
```

## Frontend Structure (`frontend/src/`)

```
frontend/src/
├── components/                # React components
│   ├── Dashboard/
│   │   └── Dashboard.tsx      # Main dashboard component
│   ├── CaseManagement/
│   │   ├── CaseList.tsx       # Cases list view
│   │   └── CaseDetail.tsx     # Individual case details
│   ├── DocumentManagement/
│   │   ├── DocumentList.tsx   # Document list component
│   │   └── DocumentViewer.tsx # Document viewer component
│   ├── LegalResearch/
│   │   └── LegalResearch.tsx  # Legal research interface
│   ├── Playbook/
│   │   └── PlaybookViewer.tsx # Playbook display component
│   └── Layout/
│       └── Layout.tsx         # Main layout with navigation
├── types/                     # TypeScript type definitions
│   ├── case.ts               # Case-related types
│   ├── document.ts           # Document-related types
│   ├── playbook.ts           # Playbook-related types
│   └── legal-research.ts     # Legal research types
├── services/                  # API client services
│   ├── api.ts                # Base API client utilities
│   ├── caseService.ts        # Case API calls
│   ├── documentService.ts    # Document API calls
│   ├── playbookService.ts    # Playbook API calls
│   └── legalResearchService.ts # Legal research API calls
├── App.tsx                   # Main application component with routing
└── main.tsx                  # Application entry point
```

## Key Features Implemented

### Backend
- **FastAPI Application**: Modern Python web framework with automatic API documentation
- **Modular Architecture**: Separated models, services, and API routes
- **Pydantic Models**: Type-safe data validation and serialization
- **Demo Data**: JSON files with realistic legal case data
- **CORS Configuration**: Proper cross-origin setup for frontend integration

### Frontend
- **React with TypeScript**: Type-safe React application
- **React Router**: Client-side routing for navigation
- **Component Architecture**: Modular component structure
- **API Services**: Centralized API communication layer
- **Type Definitions**: Comprehensive TypeScript interfaces

### Development Environment
- **Vite**: Fast frontend build tool and dev server
- **Environment Configuration**: Separate dev/production API URLs
- **Code Organization**: Clear separation of concerns

## Next Steps

This structure provides the foundation for implementing the AI Legal Platform features. The next tasks will involve:

1. Loading and serving demo data
2. Implementing API endpoints
3. Building React components
4. Adding AI analysis capabilities
5. Implementing RAG-based legal research

Each component and service has placeholder implementations that will be filled in during subsequent development tasks.