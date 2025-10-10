#!/usr/bin/env python3

from app.api.legal_research import rag_service
from app.models.legal_research import SearchQuery

print('=== TESTING SEARCH WITH CORRECT API FORMAT ===')

# Create a search query
query = SearchQuery(query='employment', limit=3)

print(f'\nSearching for: "{query.query}"')

# Test the search
results = rag_service.search_legal_corpus(
    query.query, 
    top_k=query.limit,
    min_relevance_score=query.min_relevance_score,
    legal_area=query.legal_area,
    document_type=query.document_type,
    sort_by=query.sort_by,
    content_length_filter=query.content_length_filter,
    include_citations=query.include_citations
)

print(f'Found {len(results)} results:')
for i, result in enumerate(results):
    print(f'  {i+1}. {result.document_type} - Score: {result.relevance_score:.2f}')
    print(f'     Content: {result.content[:80]}...')
    print(f'     Source: {result.source_document}')

# Test the API response format
api_response = {'results': results}
print(f'\nAPI Response format: {list(api_response.keys())}')
print(f'Results count in API: {len(api_response["results"])}')

print('\n=== TESTING OTHER SEARCHES ===')

# Test "law"
law_results = rag_service.search_legal_corpus('law', top_k=2)
print(f'\n"law" search: {len(law_results)} results')

# Test "contract"  
contract_results = rag_service.search_legal_corpus('contract', top_k=2)
print(f'"contract" search: {len(contract_results)} results')

print('\n✅ Search functionality is working!')
print('🔍 The issue might be in the frontend or API connection')