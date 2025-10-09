# Technical Documentation

## Overview

Technical documentation for architects, developers, and DevOps teams working with the Shift AI Legal Platform.

## Key Documents

- [System Architecture](./architecture.md) - High-level system design and components
- [API Documentation](./api-documentation.md) - REST API reference and examples
- [Development Setup](./development-setup.md) - Local development environment
- [Database Schema](./database-schema.md) - Data models and relationships
- [Deployment Guide](./deployment.md) - Production deployment procedures
- [Security Implementation](./security.md) - Security measures and protocols
- [Performance Optimization](./performance.md) - Scaling and optimization strategies
- [Testing Strategy](./testing.md) - Testing approaches and frameworks

## Quick Links

### Backend Documentation
🔗 **[Backend API Docs](../../backend/docs/README.md)** - Comprehensive backend documentation

### Frontend Documentation
- [Component Architecture](./frontend-architecture.md)
- [State Management](./state-management.md)
- [UI/UX Guidelines](./ui-guidelines.md)

### Infrastructure
- [Cloud Architecture](./cloud-architecture.md)
- [CI/CD Pipeline](./cicd.md)
- [Monitoring & Logging](./monitoring.md)

## Technology Stack

### Frontend
- **React 18** with TypeScript
- **Material-UI v7** for component library
- **React Router** for navigation
- **Vite** for build tooling

### Backend
- **FastAPI** with Python 3.11+
- **PostgreSQL** for primary database
- **Redis** for caching and sessions
- **Pydantic** for data validation

### AI & ML
- **[PLANNED]** Claude AI API for natural language processing
- **Vector Database** (Pinecone/Weaviate) for semantic search
- **CrewAI** for multi-agent workflows
- **Custom ML Models** for legal predictions

### Infrastructure
- **Docker** for containerization
- **Kubernetes** for orchestration
- **AWS/Azure/GCP** for cloud services
- **GitHub Actions** for CI/CD

## Getting Started

1. **Setup Development Environment**: Follow [Development Setup](./development-setup.md)
2. **Understand Architecture**: Review [System Architecture](./architecture.md)
3. **Explore APIs**: Check [API Documentation](./api-documentation.md)
4. **Run Tests**: See [Testing Strategy](./testing.md)