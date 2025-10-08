# Legal Corpus Setup Guide

This guide explains how to set up the legal document corpus for RAG (Retrieval-Augmented Generation) functionality.

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
python scripts/initialize_legal_corpus.py
```

This will:
- Process all legal documents in `app/data/legal_corpus/`
- Generate vector embeddings using sentence-transformers
- Save the corpus and embeddings for fast retrieval

### 3. Test the System

```bash
python scripts/test_legal_corpus.py
```

## Legal Corpus Contents

### 📄 Contract Templates (UK)
- Employment contracts
- Service agreements  
- Confidentiality agreements

### 📋 Legal Clauses Library
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

### Search Legal Corpus
```http
POST /legal-research/search
Content-Type: application/json

{
  "query": "employment termination notice",
  "limit": 10
}
```

### Get Relevant Clauses
```http
GET /legal-research/clauses?context=employee dismissal&legal_area=Employment Law
```

### Search by Category
```http
POST /legal-research/search/contracts
Content-Type: application/json

{
  "query": "confidentiality agreement",
  "limit": 5
}
```

### Get Corpus Statistics
```http
GET /legal-research/corpus/stats
```

## Technical Architecture

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **Provider**: sentence-transformers library
- **Language**: Optimized for English legal text

### Document Processing
1. **Chunking**: Documents split into ~1000 character chunks
2. **Metadata**: Each chunk tagged with category, legal area, document type
3. **Indexing**: Vector embeddings generated for semantic search

### Search Method
- **Similarity**: Cosine similarity between query and document embeddings
- **Ranking**: Results ranked by relevance score
- **Filtering**: Support for category and legal area filtering

## Fallback Mode

If ML dependencies are not available, the system automatically falls back to:
- Demo corpus with 8 sample documents
- Simple keyword-based search
- Basic relevance scoring

## File Structure

```
backend/app/data/
├── legal_corpus/           # Source legal documents
│   ├── contracts/         # Contract templates
│   ├── clauses/          # Legal clauses library
│   ├── precedents/       # Case law and precedents
│   ├── statutes/         # UK statutes and regulations
│   └── README.md         # Corpus documentation
├── embeddings/           # Generated embeddings (after initialization)
│   ├── legal_corpus.json    # Processed corpus metadata
│   ├── legal_embeddings.npz # Vector embeddings
│   └── index_mapping.json   # Document index mapping
└── demo_legal_corpus.json   # Demo data for fallback mode
```

## Performance Notes

- **Initialization**: ~30 seconds for full corpus (one-time setup)
- **Search Speed**: <100ms for typical queries
- **Memory Usage**: ~50MB for embeddings in memory
- **Storage**: ~10MB for corpus and embeddings on disk

## Legal Compliance

⚠️ **Important**: All documents are templates and examples based on UK law. They should be reviewed by qualified legal professionals before use in actual legal matters.

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError: No module named 'sentence_transformers'`:
- The system will automatically use demo mode
- Install dependencies for full functionality: `pip install sentence-transformers numpy`

### Empty Search Results
- Check that corpus initialization completed successfully
- Verify legal documents exist in `app/data/legal_corpus/`
- Try broader search terms

### Performance Issues
- Ensure embeddings are pre-generated (run initialization script)
- Consider reducing `top_k` parameter for faster searches
- Monitor memory usage with large corpora