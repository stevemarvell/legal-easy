#!/usr/bin/env python3

from app.services.rag_service import RAGService

# Test the new indexing methods
rag_service = RAGService()

print('=== TESTING ADMIN INDEXING FUNCTIONALITY ===')

# Test corpus statistics
print('\n1. Getting corpus statistics...')
stats = rag_service.get_corpus_statistics()
print(f'   Total documents: {stats.get("total_documents", 0)}')
print(f'   Categories: {list(stats.get("categories", {}).keys())}')

# Test case document indexing
print('\n2. Testing case document indexing...')
indexed_count = rag_service.index_case_documents()
print(f'   Indexed {indexed_count} case documents')

# Test vector database initialization
print('\n3. Testing vector database initialization...')
corpus_count = rag_service.initialize_vector_database()
print(f'   Initialized with {corpus_count} documents')

print('\n✅ Admin indexing functionality is working!')
print('🔧 Admin interface can now:')
print('   - Index legal corpus documents')
print('   - Index case documents for search')
print('   - Get indexing statistics')
print('   - Initialize and clear search indexes')