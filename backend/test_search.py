#!/usr/bin/env python3

from app.services.rag_service import RAGService

rag_service = RAGService()

print('=== TESTING SEARCH FUNCTIONALITY ===')

# Test search for 'employment'
print('\n1. Searching for "employment":')
try:
    results = rag_service.search_legal_corpus('employment', top_k=3)
    print(f'   Found {len(results)} results')
    for i, result in enumerate(results):
        print(f'   {i+1}. {result.document_type} - Score: {result.relevance_score:.2f}')
        print(f'      Content: {result.content[:100]}...')
except Exception as e:
    print(f'   Error: {e}')

# Test search for 'law'
print('\n2. Searching for "law":')
try:
    results = rag_service.search_legal_corpus('law', top_k=3)
    print(f'   Found {len(results)} results')
    for i, result in enumerate(results):
        print(f'   {i+1}. {result.document_type} - Score: {result.relevance_score:.2f}')
        print(f'      Content: {result.content[:100]}...')
except Exception as e:
    print(f'   Error: {e}')

# Test search for 'contract'
print('\n3. Searching for "contract":')
try:
    results = rag_service.search_legal_corpus('contract', top_k=3)
    print(f'   Found {len(results)} results')
    for i, result in enumerate(results):
        print(f'   {i+1}. {result.document_type} - Score: {result.relevance_score:.2f}')
        print(f'      Content: {result.content[:100]}...')
except Exception as e:
    print(f'   Error: {e}')

# Check what documents are available
print('\n4. Available documents:')
demo_corpus = rag_service._load_demo_corpus()
print(f'   Demo corpus: {len(demo_corpus)} documents')
for doc in demo_corpus[:3]:
    print(f'   - {doc.get("document_type", "Unknown")}: {doc.get("content", "")[:50]}...')