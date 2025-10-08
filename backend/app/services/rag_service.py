import json
import hashlib
from typing import List, Optional
from pathlib import Path
from app.models.legal_research import SearchResult, LegalClause


class RAGService:
    """Service for RAG-based legal research"""
    
    def __init__(self):
        self.demo_corpus_path = Path("app/data/demo_legal_corpus.json")
        try:
            from app.services.legal_corpus_service import LegalCorpusService
            self.corpus_service = LegalCorpusService()
            self.use_full_corpus = True
        except ImportError:
            # Fallback to demo data if sentence-transformers not available
            self.corpus_service = None
            self.use_full_corpus = False
    
    def search_legal_corpus(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Search through legal document corpus using RAG"""
        if self.use_full_corpus and self.corpus_service:
            try:
                corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                
                if not corpus or not embeddings:
                    # Initialize corpus if not exists
                    self.initialize_vector_database()
                    corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                
                return self.corpus_service.semantic_search(query, corpus, embeddings, top_k)
            except Exception:
                # Fall back to demo search
                pass
        
        # Use demo corpus with simple text matching
        return self._demo_search(query, top_k)
    
    def get_relevant_clauses(self, context: str, legal_area: Optional[str] = None) -> List[LegalClause]:
        """Get relevant legal clauses for given context"""
        if self.use_full_corpus and self.corpus_service:
            try:
                return self.corpus_service.get_relevant_clauses(context, legal_area)
            except Exception:
                pass
        
        # Use demo data for clauses
        return self._demo_get_clauses(context, legal_area)
    
    def initialize_vector_database(self) -> int:
        """Initialize vector database for RAG functionality"""
        if self.use_full_corpus and self.corpus_service:
            try:
                return self.corpus_service.initialize_corpus()
            except Exception as e:
                print(f"Could not initialize full corpus: {e}")
                return 0
        return 0
    
    def search_by_category(self, query: str, category: str, top_k: int = 5) -> List[SearchResult]:
        """Search within specific legal category"""
        if self.use_full_corpus and self.corpus_service:
            try:
                corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                filtered_corpus = [doc for doc in corpus if doc['category'] == category]
                return self.corpus_service.semantic_search(query, filtered_corpus, embeddings, top_k)
            except Exception:
                pass
        
        # Demo search by category
        return self._demo_search(query, top_k, category_filter=category)
    
    def get_document_categories(self) -> List[str]:
        """Get available document categories"""
        return ["contracts", "clauses", "precedents", "statutes"]
    
    def get_corpus_statistics(self) -> dict:
        """Get statistics about the legal corpus"""
        if self.use_full_corpus and self.corpus_service:
            try:
                corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                
                if corpus:
                    stats = {
                        "total_documents": len(corpus),
                        "categories": {}
                    }
                    
                    for doc in corpus:
                        category = doc['category_name']
                        if category not in stats["categories"]:
                            stats["categories"][category] = 0
                        stats["categories"][category] += 1
                    
                    return stats
            except Exception:
                pass
        
        # Demo statistics
        demo_corpus = self._load_demo_corpus()
        stats = {
            "total_documents": len(demo_corpus),
            "categories": {}
        }
        
        for doc in demo_corpus:
            category = doc['category_name']
            if category not in stats["categories"]:
                stats["categories"][category] = 0
            stats["categories"][category] += 1
        
        return stats
    
    def _load_demo_corpus(self) -> List[dict]:
        """Load demo corpus data"""
        try:
            with open(self.demo_corpus_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _demo_search(self, query: str, top_k: int, category_filter: Optional[str] = None) -> List[SearchResult]:
        """Simple text-based search for demo purposes"""
        corpus = self._load_demo_corpus()
        
        if category_filter:
            corpus = [doc for doc in corpus if doc['category'] == category_filter]
        
        query_lower = query.lower()
        results = []
        
        for doc in corpus:
            content_lower = doc['content'].lower()
            # Simple relevance scoring based on keyword matches
            score = 0.0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in content_lower:
                    score += 1.0 / len(query_words)
            
            if score > 0:
                result = SearchResult(
                    content=doc['content'],
                    source_document=doc['source_document'],
                    relevance_score=score,
                    document_type=doc['document_type'],
                    citation=f"{doc['category_name']} - {doc['source_document']}"
                )
                results.append((result, score))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results[:top_k]]
    
    def _demo_get_clauses(self, context: str, legal_area: Optional[str] = None) -> List[LegalClause]:
        """Get clauses from demo data"""
        corpus = self._load_demo_corpus()
        clause_docs = [doc for doc in corpus if doc['category'] == 'clauses']
        
        if legal_area:
            clause_docs = [doc for doc in clause_docs if doc.get('legal_area', '').lower() == legal_area.lower()]
        
        context_lower = context.lower()
        clauses = []
        
        for doc in clause_docs:
            content_lower = doc['content'].lower()
            score = 0.0
            context_words = context_lower.split()
            
            for word in context_words:
                if word in content_lower:
                    score += 1.0 / len(context_words)
            
            if score > 0:
                clause = LegalClause(
                    id=hashlib.md5(doc['content'].encode()).hexdigest()[:8],
                    content=doc['content'],
                    source_document=doc['source_document'],
                    legal_area=doc.get('legal_area', 'General'),
                    clause_type=self._determine_clause_type(doc['content']),
                    relevance_score=score
                )
                clauses.append((clause, score))
        
        # Sort by score and return top 5
        clauses.sort(key=lambda x: x[1], reverse=True)
        return [clause[0] for clause in clauses[:5]]
    
    def _determine_clause_type(self, content: str) -> str:
        """Determine clause type from content"""
        content_lower = content.lower()
        if 'termination' in content_lower or 'terminate' in content_lower:
            return "Termination Clause"
        elif 'liability' in content_lower or 'indemnif' in content_lower:
            return "Liability Clause"
        elif 'intellectual property' in content_lower or 'copyright' in content_lower:
            return "IP Clause"
        elif 'confidential' in content_lower or 'non-disclosure' in content_lower:
            return "Confidentiality Clause"
        else:
            return "General Clause"