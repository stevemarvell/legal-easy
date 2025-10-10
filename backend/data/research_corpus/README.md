# UK Research Document Corpus

This directory contains a comprehensive collection of UK research documents, clauses, precedents, and statutes for use in the RAG (Retrieval-Augmented Generation) system.

## Structure

### 📄 Contracts (`/contracts/`)
Template contracts commonly used in UK legal practice:
- **employment_template.txt** - Standard UK employment contract template
- **service_agreement_template.txt** - Professional services agreement template
- **non_disclosure_agreement.txt** - UK confidentiality agreement template

### 📋 Clauses (`/clauses/`)
Library of standard research clauses organized by type:
- **termination_clauses.txt** - Various termination clause templates
- **liability_clauses.txt** - Liability limitation and indemnification clauses
- **intellectual_property_clauses.txt** - IP ownership and licensing clauses

### ⚖️ Precedents (`/precedents/`)
Key case law and research principles:
- **employment_law_precedents.txt** - Major UK employment law cases and principles
- **contract_law_precedents.txt** - Fundamental UK contract law precedents

### 📚 Statutes (`/statutes/`)
Key UK legislation and regulations:
- **employment_statutes.txt** - Major UK employment law statutes
- **contract_statutes.txt** - UK contract and consumer protection law

## Research Areas Covered

- **Employment Law**: Contracts, dismissal, discrimination, working time
- **Contract Law**: Formation, breach, remedies, consumer protection
- **Intellectual Property**: Copyright, patents, licensing
- **Data Protection**: UK GDPR, privacy rights
- **Commercial Law**: Service agreements, liability, indemnification

## Usage

The corpus is automatically processed by the `ResearchCorpusService` to:
1. Extract and chunk document content
2. Generate semantic embeddings using sentence transformers
3. Enable semantic search for legal research queries
4. Provide relevant research clause suggestions

## Initialization

To initialize the corpus and generate embeddings:

```python
from app.services.ai_service import AIService

ai_service = AIService()
ai_service.initialize_research_corpus(corpus_path)
```

To test the RAG functionality:

```python
from app.services.ai_service import AIService

ai_service = AIService()
result = ai_service.test_research_corpus()
```

## Technical Details

- **Embedding Model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Chunk Size**: Maximum 1000 characters per chunk
- **Search Method**: Cosine similarity on vector embeddings
- **Storage**: JSON metadata + compressed NumPy arrays

## Compliance

All documents are templates and examples based on UK law. They should be reviewed by qualified legal professionals before use in actual legal matters.