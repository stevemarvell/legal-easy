#!/usr/bin/env python3

from app.services.rag_service import RAGService

rag_service = RAGService()

print('=== DEBUGGING RAG SERVICE INITIALIZATION ===')

print(f'\n1. RAG Service Configuration:')
print(f'   use_full_corpus: {rag_service.use_full_corpus}')
print(f'   use_simple_vector: {rag_service.use_simple_vector}')
print(f'   has corpus_service: {hasattr(rag_service, "corpus_service") and rag_service.corpus_service is not None}')
print(f'   has vector_service: {hasattr(rag_service, "vector_service") and rag_service.vector_service is not None}')

print(f'\n2. Demo Corpus Test:')
demo_corpus = rag_service._load_demo_corpus()
print(f'   Demo corpus loaded: {len(demo_corpus)} documents')

print(f'\n3. Corpus Statistics:')
stats = rag_service.get_corpus_statistics()
print(f'   Statistics: {stats}')

print(f'\n4. Initialize Vector Database:')
try:
    count = rag_service.initialize_vector_database()
    print(f'   Initialized with: {count} documents')
except Exception as e:
    print(f'   Error: {e}')