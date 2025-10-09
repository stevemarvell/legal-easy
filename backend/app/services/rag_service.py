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
                           legal_area: str = None, document_type: str = None, sort_by: str = "relevance",
                           content_length_filter: str = None, include_citations: bool = True) -> List[SearchResult]:
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
                filtered_corpus = self._apply_filters(corpus, legal_area, document_type, content_length_filter)
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
                filtered_corpus = self._apply_filters(corpus, legal_area, document_type, content_length_filter)
                results = self.vector_service.semantic_search(query, filtered_corpus, embeddings, top_k * 2)
            except Exception:
                # Fall back to demo search
                pass
        
        if not results:
            # Use demo corpus with enhanced text matching
            results = self._demo_search(query, top_k * 2, legal_area=legal_area, 
                                      document_type=document_type, content_length_filter=content_length_filter)
        
        # Apply post-processing filters and ranking
        return self._post_process_results(results, min_relevance_score, sort_by, top_k, include_citations)
    
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
                    legal_area: Optional[str] = None, document_type: Optional[str] = None,
                    content_length_filter: Optional[str] = None) -> List[SearchResult]:
        """Enhanced text-based search for demo purposes with advanced filtering"""
        corpus = self._load_demo_corpus()
        
        # Apply enhanced filters
        corpus = self._apply_filters(corpus, legal_area, document_type, content_length_filter)
        
        if category_filter:
            corpus = [doc for doc in corpus if doc['category'] == category_filter]
        
        query_lower = query.lower()
        results = []
        
        for doc in corpus:
            content_lower = doc['content'].lower()
            
            # Enhanced relevance scoring with multiple factors
            score = self._calculate_demo_relevance_score(query_lower, content_lower, doc)
            
            if score > 0:
                result = SearchResult(
                    content=doc['content'],
                    source_document=doc['source_document'],
                    relevance_score=score,
                    document_type=doc['document_type'],
                    citation=f"{doc['category_name']} - {doc['source_document']}"
                )
                results.append(result)
        
        return results
    
    def _calculate_demo_relevance_score(self, query_lower: str, content_lower: str, doc: dict) -> float:
        """Calculate enhanced relevance score for demo search"""
        score = 0.0
        query_words = query_lower.split()
        
        # Basic keyword matching with position weighting
        for i, word in enumerate(query_words):
            if word in content_lower:
                # Earlier words in query are more important
                word_weight = 1.0 - (i * 0.1)
                word_weight = max(word_weight, 0.5)
                
                # Count occurrences with diminishing returns
                occurrences = content_lower.count(word)
                occurrence_score = min(occurrences * 0.2, 0.8)
                
                score += (word_weight * occurrence_score) / len(query_words)
        
        # Phrase matching bonus
        if len(query_words) > 1:
            query_phrase = ' '.join(query_words)
            if query_phrase in content_lower:
                score += 0.3  # Significant bonus for exact phrase match
        
        # Partial phrase matching
        for i in range(len(query_words) - 1):
            partial_phrase = ' '.join(query_words[i:i+2])
            if partial_phrase in content_lower:
                score += 0.1
        
        # Document quality indicators
        quality_score = self._calculate_document_quality_score(doc)
        score *= (1.0 + quality_score)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _calculate_document_quality_score(self, doc: dict) -> float:
        """Calculate document quality score based on metadata and content"""
        quality = 0.0
        content = doc.get('content', '')
        
        # Content length quality (sweet spot around 300-800 characters)
        length = len(content)
        if 300 <= length <= 800:
            quality += 0.1
        elif 200 <= length <= 1000:
            quality += 0.05
        
        # Document type quality
        doc_type = doc.get('document_type', '').lower()
        type_quality = {
            'statute/regulation': 0.15,
            'case law': 0.12,
            'legal clause': 0.10,
            'contract template': 0.08
        }
        quality += type_quality.get(doc_type, 0.05)
        
        # Content structure quality (presence of legal formatting)
        content_lower = content.lower()
        structure_indicators = [
            'section', 'subsection', 'paragraph', 'clause',
            'whereas', 'therefore', 'notwithstanding'
        ]
        
        structure_count = sum(1 for indicator in structure_indicators if indicator in content_lower)
        quality += min(structure_count * 0.02, 0.1)
        
        return min(quality, 0.3)  # Cap quality bonus
    
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
    
    def _apply_filters(self, corpus: List[dict], legal_area: str = None, document_type: str = None, 
                      content_length_filter: str = None) -> List[dict]:
        """Apply enhanced filters to corpus before search"""
        filtered_corpus = corpus
        
        # Legal area filtering with fuzzy matching
        if legal_area:
            legal_area_lower = legal_area.lower()
            filtered_corpus = [doc for doc in filtered_corpus 
                             if self._matches_legal_area(doc, legal_area_lower)]
        
        # Document type filtering with fuzzy matching
        if document_type:
            document_type_lower = document_type.lower()
            filtered_corpus = [doc for doc in filtered_corpus 
                             if self._matches_document_type(doc, document_type_lower)]
        
        # Content length filtering
        if content_length_filter:
            filtered_corpus = self._apply_content_length_filter(filtered_corpus, content_length_filter)
        
        return filtered_corpus
    
    def _matches_legal_area(self, doc: dict, legal_area_lower: str) -> bool:
        """Check if document matches legal area with fuzzy matching"""
        doc_legal_area = doc.get('legal_area', '').lower()
        doc_content = doc.get('content', '').lower()
        doc_category = doc.get('category_name', '').lower()
        
        # Direct match
        if legal_area_lower in doc_legal_area:
            return True
        
        # Fuzzy matching for common legal area variations
        area_mappings = {
            'employment': ['employment', 'employee', 'workplace', 'labor'],
            'contract': ['contract', 'agreement', 'contractual'],
            'liability': ['liability', 'tort', 'negligence', 'damages'],
            'intellectual property': ['intellectual', 'copyright', 'trademark', 'patent', 'ip'],
            'corporate': ['corporate', 'corporation', 'business', 'company']
        }
        
        for area, keywords in area_mappings.items():
            if legal_area_lower in area or area in legal_area_lower:
                return any(keyword in doc_content or keyword in doc_category for keyword in keywords)
        
        return False
    
    def _matches_document_type(self, doc: dict, document_type_lower: str) -> bool:
        """Check if document matches document type with fuzzy matching"""
        doc_type = doc.get('document_type', '').lower()
        doc_category = doc.get('category', '').lower()
        
        # Direct match
        if document_type_lower in doc_type:
            return True
        
        # Category-based matching
        type_mappings = {
            'contract': ['contracts', 'agreement'],
            'clause': ['clauses', 'provision'],
            'statute': ['statutes', 'regulation', 'law'],
            'precedent': ['precedents', 'case law', 'cases']
        }
        
        for doc_type_key, categories in type_mappings.items():
            if document_type_lower in doc_type_key or doc_type_key in document_type_lower:
                return any(category in doc_category for category in categories)
        
        return False
    
    def _apply_content_length_filter(self, corpus: List[dict], length_filter: str) -> List[dict]:
        """Apply content length filtering"""
        if length_filter == "short":
            return [doc for doc in corpus if len(doc.get('content', '')) < 200]
        elif length_filter == "medium":
            return [doc for doc in corpus if 200 <= len(doc.get('content', '')) < 500]
        elif length_filter == "long":
            return [doc for doc in corpus if len(doc.get('content', '')) >= 500]
        else:
            return corpus
    
    def _post_process_results(self, results: List[SearchResult], min_relevance_score: float, 
                            sort_by: str, top_k: int, include_citations: bool = True) -> List[SearchResult]:
        """Post-process search results with enhanced filtering and ranking"""
        # Filter by minimum relevance score
        filtered_results = [r for r in results if r.relevance_score >= min_relevance_score]
        
        # Apply enhanced relevance scoring first
        enhanced_results = []
        for result in filtered_results:
            enhanced_score = self._calculate_enhanced_relevance(result)
            result.relevance_score = enhanced_score
            
            # Enhance citation if requested
            if include_citations:
                result.citation = self._enhance_citation(result)
            
            enhanced_results.append(result)
        
        # Apply advanced sorting algorithms after enhanced scoring
        enhanced_results = self._apply_advanced_sorting(enhanced_results, sort_by)
        
        # Apply diversity filtering to avoid too many similar results
        diverse_results = self._apply_diversity_filtering(enhanced_results, top_k)
        
        return diverse_results[:top_k]
    
    def _apply_advanced_sorting(self, results: List[SearchResult], sort_by: str) -> List[SearchResult]:
        """Apply advanced sorting algorithms"""
        if sort_by == "relevance":
            # Multi-factor relevance sorting
            results.sort(key=lambda x: (
                x.relevance_score,
                len(x.content),  # Longer content as tiebreaker
                self._get_document_authority_score(x)  # Authority score as final tiebreaker
            ), reverse=True)
        
        elif sort_by == "document_type":
            # Sort by document type hierarchy, then relevance
            type_hierarchy = {
                "statute/regulation": 1,
                "case law": 2,
                "legal precedent": 3,
                "legal clause": 4,
                "contract template": 5,
                "contract": 6,
                "legal document": 7
            }
            results.sort(key=lambda x: (
                type_hierarchy.get(x.document_type.lower(), 99),
                -x.relevance_score
            ))
        
        elif sort_by == "legal_area":
            # Sort by legal area, then relevance
            results.sort(key=lambda x: (
                self._extract_legal_area(x),
                -x.relevance_score
            ))
        
        elif sort_by == "authority":
            # Sort by document authority/importance
            results.sort(key=lambda x: (
                -self._get_document_authority_score(x),
                -x.relevance_score
            ))
        
        return results
    
    def _get_document_authority_score(self, result: SearchResult) -> float:
        """Calculate document authority score based on various factors"""
        score = 0.0
        content_lower = result.content.lower()
        
        # Authority indicators
        authority_terms = [
            'supreme court', 'federal court', 'circuit court', 'appellate',
            'statute', 'regulation', 'code', 'act', 'law'
        ]
        
        for term in authority_terms:
            if term in content_lower:
                score += 0.2
        
        # Document type authority
        type_authority = {
            "statute/regulation": 1.0,
            "case law": 0.9,
            "legal precedent": 0.8,
            "legal clause": 0.6,
            "contract template": 0.4
        }
        
        score += type_authority.get(result.document_type.lower(), 0.2)
        
        return min(score, 1.0)
    
    def _apply_diversity_filtering(self, results: List[SearchResult], target_count: int) -> List[SearchResult]:
        """Apply diversity filtering to ensure varied results"""
        if len(results) <= target_count:
            return results
        
        diverse_results = []
        used_document_types = set()
        used_legal_areas = set()
        
        # First pass: ensure diversity in document types and legal areas
        for result in results:
            doc_type = result.document_type.lower()
            legal_area = self._extract_legal_area(result)
            
            # Add if we haven't seen this combination or if we have room
            if (len(diverse_results) < target_count and 
                (doc_type not in used_document_types or legal_area not in used_legal_areas)):
                diverse_results.append(result)
                used_document_types.add(doc_type)
                used_legal_areas.add(legal_area)
        
        # Second pass: fill remaining slots with highest relevance
        remaining_slots = target_count - len(diverse_results)
        if remaining_slots > 0:
            remaining_results = [r for r in results if r not in diverse_results]
            remaining_results.sort(key=lambda x: x.relevance_score, reverse=True)
            diverse_results.extend(remaining_results[:remaining_slots])
        
        return diverse_results
    
    def _enhance_citation(self, result: SearchResult) -> str:
        """Enhance citation with additional metadata"""
        base_citation = result.citation
        legal_area = self._extract_legal_area(result)
        
        # Add legal area to citation if not already present
        if legal_area != "General" and legal_area.lower() not in base_citation.lower():
            base_citation = f"{base_citation} ({legal_area})"
        
        # Add content length indicator
        content_length = len(result.content)
        if content_length > 500:
            length_indicator = "Detailed"
        elif content_length > 200:
            length_indicator = "Standard"
        else:
            length_indicator = "Brief"
        
        return f"{base_citation} - {length_indicator}"
    
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
        
        # Boost score based on document type importance hierarchy
        type_boost = {
            "statute/regulation": 1.25,
            "case law": 1.20,
            "legal precedent": 1.18,
            "legal clause": 1.15,
            "contract template": 1.10,
            "contract": 1.08,
            "legal document": 1.05
        }
        
        doc_type_key = result.document_type.lower()
        boost = type_boost.get(doc_type_key, 1.0)
        
        # Enhanced content quality scoring
        content_lower = result.content.lower()
        
        # High-value legal terms (stronger boost)
        high_value_terms = [
            'shall', 'must', 'required', 'obligation', 'liability', 
            'indemnification', 'breach', 'damages', 'termination',
            'jurisdiction', 'governing law', 'force majeure'
        ]
        
        # Medium-value legal terms
        medium_value_terms = [
            'agreement', 'contract', 'party', 'parties', 'provision',
            'clause', 'section', 'subsection', 'whereas', 'therefore'
        ]
        
        # Legal structure indicators
        structure_terms = [
            'notwithstanding', 'provided that', 'subject to', 'in accordance with',
            'pursuant to', 'with respect to', 'for the purposes of'
        ]
        
        quality_boost = 1.0
        
        # Apply high-value term boosts
        for term in high_value_terms:
            if term in content_lower:
                quality_boost += 0.04
        
        # Apply medium-value term boosts
        for term in medium_value_terms:
            if term in content_lower:
                quality_boost += 0.02
        
        # Apply structure term boosts
        for term in structure_terms:
            if term in content_lower:
                quality_boost += 0.03
        
        # Boost for content length (longer, more detailed content is often more valuable)
        content_length = len(result.content)
        if content_length > 500:
            quality_boost += 0.05
        elif content_length > 200:
            quality_boost += 0.03
        
        # Boost for specific legal areas based on content analysis
        legal_area_boost = self._calculate_legal_area_boost(content_lower)
        quality_boost += legal_area_boost
        
        # Cap the quality boost to prevent over-inflation
        quality_boost = min(quality_boost, 1.4)
        
        enhanced_score = base_score * boost * quality_boost
        return min(enhanced_score, 1.0)  # Cap at 1.0
    
    def _calculate_legal_area_boost(self, content_lower: str) -> float:
        """Calculate boost based on legal area specialization"""
        legal_area_indicators = {
            'employment': ['employment', 'employee', 'employer', 'workplace', 'termination', 'discrimination'],
            'contract': ['contract', 'agreement', 'breach', 'performance', 'consideration', 'offer', 'acceptance'],
            'liability': ['liability', 'negligence', 'damages', 'indemnification', 'insurance', 'tort'],
            'intellectual_property': ['copyright', 'trademark', 'patent', 'intellectual property', 'trade secret'],
            'corporate': ['corporation', 'shareholder', 'board', 'director', 'merger', 'acquisition']
        }
        
        boost = 0.0
        for area, indicators in legal_area_indicators.items():
            area_matches = sum(1 for indicator in indicators if indicator in content_lower)
            if area_matches >= 2:  # Multiple indicators suggest specialization
                boost += 0.03 * area_matches
        
        return min(boost, 0.15)  # Cap area boost