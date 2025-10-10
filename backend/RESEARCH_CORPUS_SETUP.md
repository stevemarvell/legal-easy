# Research Corpus Setup Guide

This guide explains how to set up the research document corpus for RAG (Retrieval-Augmented Generation) functionality.

## Quick Start (Demo Mode)

The system includes demo data that works immediately without additional dependencies:

```bash
cd backend
python -c "from app.services.rag_service import RAGService; rag = RAGService(); print('Demo corpus loaded:', rag.get_corpus_statistics())"
```

## Full Setup (Production Mode)

For full semantic search capabilities, install the required ML dependencies:

### 1. Install Dependencies

```bash
cd backend
pip install sentence-transformers==2.2.2 numpy==1.24.3
```

### 2. Initialize the Corpus

```bash
python scripts/initialize_research_corpus.py
```

This will:
- Process all research documents in `app/data/research_corpus/`
- Generate vector embeddings using sentence-transformers
- Save the corpus and embeddings for fast retrieval

### 3. Test the System

```bash
python scripts/test_research_corpus.py
```

## Research Corpus Contents

### 📄 Contract Templates (UK)
- Employment contracts
- Service agreements  
- Confidentiality agreements

### 📋 Research Clauses Library
- Termination clauses
- Liability and indemnification clauses
- Intellectual property clauses

### ⚖️ Case Law and Precedents
- UK employment law precedents
- UK contract law precedents

### 📚 UK Statutes and Regulations
- Employment law statutes
- Contract and consumer protection law

## API Endpoints

Once set up, the following endpoints are available:

### Search Research Corpus
```http
GET /api/corpus/search?q=employment termination notice
```

### Get Corpus Categories
```http
GET /api/corpus/categories
```

### Browse by Category
```http
GET /api/corpus?category=contracts
```

### Get Specific Item
```http
GET /api/corpus/{item_id}
```

### Get Research Concepts
```http
GET /api/corpus/concepts
```

### Get Related Materials
```http
GET /api/corpus/{item_id}/related
```

## Technical Architecture

### Data Structure
- **Index File**: `research_corpus_index.json` contains metadata for all documents
- **Categories**: contracts, clauses, precedents, statutes
- **Research Areas**: Employment Law, Contract Law, Intellectual Property, etc.

### Document Processing
1. **Organization**: Documents organized by category in subdirectories
2. **Metadata**: Each document tagged with category, research areas, document type
3. **Content**: Full document content loaded on demand

### Search Method
- **Text Search**: Search across names, descriptions, and research areas
- **Category Filtering**: Filter results by document category
- **Research Area Filtering**: Filter by legal domain
- **Related Items**: Find related documents based on shared research areas

## File Structure

```
backend/data/
├── research_corpus/           # Source research documents
│   ├── research_corpus_index.json  # Main index file
│   ├── contracts/         # Contract templates
│   ├── clauses/          # Research clauses library
│   ├── precedents/       # Case law and precedents
│   ├── statutes/         # UK statutes and regulations
│   └── README.md         # Corpus documentation
```

## Performance Notes

- **Search Speed**: <100ms for typical queries
- **Memory Usage**: Minimal - content loaded on demand
- **Storage**: ~10MB for corpus documents

## Legal Compliance

⚠️ **Important**: All documents are templates and examples based on UK law. They should be reviewed by qualified legal professionals before use in actual legal matters.

## Troubleshooting

### Empty Search Results
- Check that corpus files exist in `backend/data/research_corpus/`
- Verify the research_corpus_index.json file is properly formatted
- Try broader search terms

### Missing Categories
- Ensure all category directories exist (contracts, clauses, precedents, statutes)
- Check that document files are in the correct category directories
- Verify filenames match those listed in the index file