import json
import hashlib
from typing import List, Optional
from pathlib import Path
from app.models.legal_research import SearchResult, LegalClause


class RAGService:
    """Service for RAG-based legal research"""
    
    def __init__(self):
        self.demo_corpus_path = Path("app/data/demo_legal_corpus.json")
        
        # Try to use advanced corpus service first, then simple vector service, then demo
        try:
            from app.services.legal_corpus_service import LegalCorpusService
            self.corpus_service = LegalCorpusService()
            self.use_full_corpus = True
            self.use_simple_vector = False
        except ImportError:
            try:
                from app.services.simple_vector_service import SimpleVectorService
                self.vector_service = SimpleVectorService()
                self.corpus_service = None
                self.use_full_corpus = False
                self.use_simple_vector = True
            except ImportError:
                # Fallback to demo data if no vector services available
                self.corpus_service = None
                self.vector_service = None
                self.use_full_corpus = False
                self.use_simple_vector = False
    
    def search_legal_corpus(self, query: str, top_k: int = 10, min_relevance_score: float = 0.0, 
                           legal_area: str = None, document_type: str = None, sort_by: str = "relevance") -> List[SearchResult]:
        """Search through legal document corpus using RAG with filtering and ranking"""
        results = []
        
        if self.use_full_corpus and self.corpus_service:
            try:
                corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                
                if not corpus or not embeddings:
                    # Initialize corpus if not exists
                    self.initialize_vector_database()
                    corpus, embeddings = self.corpus_service.load_corpus_and_embeddings()
                
                # Apply filters to corpus before search
                filtered_corpus = self._apply_filters(corpus, legal_area, document_type)
                results = self.corpus_service.semantic_search(query, filtered_corpus, embeddings, top_k * 2)
            except Exception:
                # Fall back to simple vector search
                pass
        
        if not results and self.use_simple_vector and self.vector_service:
            try:
                corpus, embeddings = self.vector_service.load_corpus_and_embeddings()
                
                if not corpus or not embeddings:
                    # Initialize vector database if not exists
                    self.initialize_vector_database()
                    corpus, embeddings = self.vector_service.load_corpus_and_embeddings()
                
                # Apply filters to corpus before search
                filtered_corpus = self._apply_filters(corpus, legal_area, document_type)
                results = self.vector_service.semantic_search(query, filtered_corpus, embeddings, top_k * 2)
            except Exception:
                # Fall back to demo search
                pass
        
        if not results:
            # Use demo corpus with simple text matching
            results = self._demo_search(query, top_k * 2, legal_area=legal_area, document_type=document_type)
        
        # Apply post-processing filters and ranking
        return self._post_process_results(results, min_relevance_score, sort_by, top_k)
    
    def get_relevant_clauses(self, context: str, legal_area: Optional[str] = None) -> List[LegalClause]:
        """Get relevant legal clauses for given context"""
        if self.use_full_corpus and self.corpus_service:
            try:
                return self.corpus_service.get_relevant_clauses(context, legal_area)
            except Exception:
                pass
        
        if self.use_simple_vector and self.vector_service:
            try:
                return self.vector_service.get_relevant_clauses(context, legal_area)
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
                # Fall back to simple vector service
                pass
        
        if self.use_simple_vector and self.vector_service:
            try:
                return self.vector_service.initialize_vector_database()
            except Exception as e:
                print(f"Could not initialize simple vector database: {e}")
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
        
        if self.use_simple_vector and self.vector_service:
            try:
                corpus, embeddings = self.vector_service.load_corpus_and_embeddings()
                filtered_corpus = [doc for doc in corpus if doc['category'] == category]
                return self.vector_service.semantic_search(query, filtered_corpus, embeddings, top_k)
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
        
        if self.use_simple_vector and self.vector_service:
            try:
                corpus, embeddings = self.vector_service.load_corpus_and_embeddings()
                
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
    
    def _demo_search(self, query: str, top_k: int, category_filter: Optional[str] = None, 
                    legal_area: Optional[str] = None, document_type: Optional[str] = None) -> List[SearchResult]:
        """Simple text-based search for demo purposes with filtering"""
        corpus = self._load_demo_corpus()
        
        # Apply filters
        if category_filter:
            corpus = [doc for doc in corpus if doc['category'] == category_filter]
        
        if legal_area:
            corpus = [doc for doc in corpus if doc.get('legal_area', '').lower() == legal_area.lower()]
        
        if document_type:
            corpus = [doc for doc in corpus if doc.get('document_type', '').lower() == document_type.lower()]
        
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
    
    def _apply_filters(self, corpus: List[dict], legal_area: str = None, document_type: str = None) -> List[dict]:
        """Apply filters to corpus before search"""
        filtered_corpus = corpus
        
        if legal_area:
            filtered_corpus = [doc for doc in filtered_corpus 
                             if doc.get('legal_area', '').lower() == legal_area.lower()]
        
        if document_type:
            filtered_corpus = [doc for doc in filtered_corpus 
                             if doc.get('document_type', '').lower() == document_type.lower()]
        
        return filtered_corpus
    
    def _post_process_results(self, results: List[SearchResult], min_relevance_score: float, 
                            sort_by: str, top_k: int) -> List[SearchResult]:
        """Post-process search results with filtering and ranking"""
        # Filter by minimum relevance score
        filtered_results = [r for r in results if r.relevance_score >= min_relevance_score]
        
        # Apply sorting
        if sort_by == "relevance":
            filtered_results.sort(key=lambda x: x.relevance_score, reverse=True)
        elif sort_by == "document_type":
            filtered_results.sort(key=lambda x: (x.document_type, -x.relevance_score))
        elif sort_by == "legal_area":
            # For legal area sorting, we need to extract it from citation or content
            filtered_results.sort(key=lambda x: (self._extract_legal_area(x), -x.relevance_score))
        
        # Apply enhanced relevance scoring
        enhanced_results = []
        for result in filtered_results:
            enhanced_score = self._calculate_enhanced_relevance(result)
            result.relevance_score = enhanced_score
            enhanced_results.append(result)
        
        # Re-sort by enhanced relevance if needed
        if sort_by == "relevance":
            enhanced_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return enhanced_results[:top_k]
    
    def _extract_legal_area(self, result: SearchResult) -> str:
        """Extract legal area from search result"""
        # Try to determine legal area from document type or content
        doc_type = result.document_type.lower()
        content = result.content.lower()
        
        if 'employment' in doc_type or 'employment' in content:
            return "Employment Law"
        elif 'contract' in doc_type or 'contract' in content:
            return "Contract Law"
        elif 'liability' in content or 'indemnif' in content:
            return "Liability and Risk"
        elif 'intellectual' in content or 'copyright' in content:
            return "Intellectual Property"
        else:
            return "General"
    
    def _calculate_enhanced_relevance(self, result: SearchResult) -> float:
        """Calculate enhanced relevance score based on multiple factors"""
        base_score = result.relevance_score
        
        # Boost score based on document type importance
        type_boost = {
            "statute/regulation": 1.2,
            "case law": 1.15,
            "legal clause": 1.1,
            "contract template": 1.05
        }
        
        doc_type_key = result.document_type.lower()
        boost = type_boost.get(doc_type_key, 1.0)
        
        # Boost score based on content quality indicators
        content_lower = result.content.lower()
        quality_indicators = [
            'shall', 'must', 'required', 'obligation', 'liability', 
            'termination', 'breach', 'damages', 'indemnification'
        ]
        
        quality_boost = 1.0
        for indicator in quality_indicators:
            if indicator in content_lower:
                quality_boost += 0.02
        
        # Cap the quality boost
        quality_boost = min(quality_boost, 1.2)
        
        enhanced_score = base_score * boost * quality_boost
        return min(enhanced_score, 1.0)  # Cap at 1.0