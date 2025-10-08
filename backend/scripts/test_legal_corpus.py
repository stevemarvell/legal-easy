#!/usr/bin/env python3
"""
Test script for the legal document corpus and RAG functionality.
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.rag_service import RAGService


def test_rag_functionality():
    """Test the RAG service functionality"""
    print("Testing Legal RAG System")
    print("=" * 30)
    
    # Initialize RAG service
    rag_service = RAGService()
    
    # Test queries
    test_queries = [
        "employment contract termination",
        "confidentiality agreement",
        "liability limitation clauses",
        "intellectual property rights",
        "unfair dismissal protection"
    ]
    
    print("\n🔍 Testing semantic search...")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = rag_service.search_legal_corpus(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result.document_type} - {result.source_document}")
                print(f"     Relevance: {result.relevance_score:.3f}")
                print(f"     Preview: {result.content[:100]}...")
        else:
            print("  No results found")
    
    print("\n📊 Corpus Statistics:")
    stats = rag_service.get_corpus_statistics()
    print(f"  Total documents: {stats['total_documents']}")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count} documents")
    
    print("\n🔧 Testing clause retrieval...")
    clauses = rag_service.get_relevant_clauses("employee termination notice period")
    if clauses:
        for clause in clauses[:2]:
            print(f"  - {clause.clause_type} (Score: {clause.relevance_score:.3f})")
            print(f"    {clause.content[:150]}...")
    
    print("\n✅ RAG system test completed!")


if __name__ == "__main__":
    test_rag_functionality()