import json
import os
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np
from app.models.legal_research import SearchResult, LegalClause


class SimpleVectorService:
    """Simple vector database service using basic embeddings and cosine similarity"""
    
    def __init__(self):
        self.corpus_path = Path("app/data/legal_corpus")
        self.embeddings_path = Path("app/data/embeddings")
        self.embeddings_path.mkdir(exist_ok=True)
        
        # Legal document categories
        self.categories = {
            'contracts': 'Contract Templates',
            'clauses': 'Legal Clauses',
            'precedents': 'Case Law and Precedents',
            'statutes': 'Statutes and Regulations'
        }
        
        # Simple word-based embeddings (TF-IDF style)
        self.vocabulary = {}
        self.corpus_data = []
        self.embeddings = {}
    
    def initialize_vector_database(self) -> int:
        """Initialize vector database with simple embeddings"""
        print("Compiling legal corpus...")
        corpus = self.compile_legal_corpus()
        
        if not corpus:
            print("No legal documents found in corpus directory")
            return 0
        
        print(f"Building vocabulary and embeddings for {len(corpus)} documents...")
        self.build_vocabulary(corpus)
        embeddings = self.generate_simple_embeddings(corpus)
        
        print("Saving corpus and embeddings...")
        self.save_corpus_and_embeddings(corpus, embeddings)
        
        print(f"Vector database initialized with {len(corpus)} documents")
        return len(corpus)
    
    def compile_legal_corpus(self) -> List[Dict[str, Any]]:
        """Compile all legal documents into structured corpus"""
        corpus = []
        
        for category, category_name in self.categories.items():
            category_path = self.corpus_path / category
            if category_path.exists():
                for file_path in category_path.glob("*.txt"):
                    content = self._read_file_content(file_path)
                    if content:
                        # Split content into chunks for better search
                        chunks = self._split_into_chunks(content)
                        
                        for i, chunk in enumerate(chunks):
                            doc_id = f"{category}_{file_path.stem}_{i}"
                            corpus.append({
                                'id': doc_id,
                                'content': chunk,
                                'source_document': file_path.name,
                                'category': category,
                                'category_name': category_name,
                                'legal_area': self._determine_legal_area(file_path.name),
                                'document_type': self._determine_document_type(category, file_path.name)
                            })
        
        return corpus
    
    def build_vocabulary(self, corpus: List[Dict[str, Any]]):
        """Build vocabulary from corpus for simple embeddings"""
        word_counts = {}
        
        for doc in corpus:
            words = self._tokenize(doc['content'])
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Keep words that appear at least twice and create vocabulary with proper indexing
        filtered_words = [word for word, count in word_counts.items() if count >= 2]
        self.vocabulary = {word: idx for idx, word in enumerate(filtered_words)}
    
    def generate_simple_embeddings(self, corpus: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Generate simple TF-IDF style embeddings"""
        embeddings = {}
        vocab_size = len(self.vocabulary)
        
        for doc in corpus:
            doc_id = doc['id']
            words = self._tokenize(doc['content'])
            
            # Create simple bag-of-words vector
            vector = np.zeros(vocab_size)
            word_counts = {}
            
            for word in words:
                if word in self.vocabulary:
                    word_counts[word] = word_counts.get(word, 0) + 1
            
            # Simple TF weighting
            for word, count in word_counts.items():
                if word in self.vocabulary:
                    vector[self.vocabulary[word]] = count / len(words)
            
            # Normalize vector
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            
            embeddings[doc_id] = vector
        
        return embeddings
    
    def save_corpus_and_embeddings(self, corpus: List[Dict[str, Any]], embeddings: Dict[str, np.ndarray]):
        """Save corpus metadata and embeddings to disk"""
        # Save corpus metadata
        corpus_file = self.embeddings_path / "legal_corpus.json"
        with open(corpus_file, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
        
        # Save embeddings
        embeddings_file = self.embeddings_path / "simple_embeddings.npz"
        np.savez_compressed(embeddings_file, **embeddings)
        
        # Save vocabulary
        vocab_file = self.embeddings_path / "vocabulary.json"
        with open(vocab_file, 'w') as f:
            json.dump(self.vocabulary, f, indent=2)
    
    def load_corpus_and_embeddings(self) -> tuple[List[Dict[str, Any]], Dict[str, np.ndarray]]:
        """Load corpus and embeddings from disk"""
        corpus_file = self.embeddings_path / "legal_corpus.json"
        embeddings_file = self.embeddings_path / "simple_embeddings.npz"
        vocab_file = self.embeddings_path / "vocabulary.json"
        
        if not all([corpus_file.exists(), embeddings_file.exists(), vocab_file.exists()]):
            return [], {}
        
        # Load corpus
        with open(corpus_file, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
        
        # Load embeddings
        embeddings_data = np.load(embeddings_file)
        embeddings = {key: embeddings_data[key] for key in embeddings_data.files}
        
        # Load vocabulary
        with open(vocab_file, 'r') as f:
            self.vocabulary = json.load(f)
        
        return corpus, embeddings
    
    def semantic_search(self, query: str, corpus: List[Dict[str, Any]], 
                       embeddings: Dict[str, np.ndarray], top_k: int = 10) -> List[SearchResult]:
        """Perform semantic search using simple embeddings"""
        if not corpus or not embeddings or not self.vocabulary:
            return []
        
        # Generate query embedding
        query_words = self._tokenize(query)
        query_vector = np.zeros(len(self.vocabulary))
        
        for word in query_words:
            if word in self.vocabulary:
                query_vector[self.vocabulary[word]] = 1.0 / len(query_words)
        
        # Normalize query vector
        query_norm = np.linalg.norm(query_vector)
        if query_norm > 0:
            query_vector = query_vector / query_norm
        
        # Calculate similarities
        similarities = []
        for doc in corpus:
            doc_id = doc['id']
            if doc_id in embeddings:
                doc_embedding = embeddings[doc_id]
                similarity = np.dot(query_vector, doc_embedding)
                similarities.append((doc, similarity))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc, score in similarities[:top_k]:
            if score > 0:  # Only return results with positive similarity
                result = SearchResult(
                    content=doc['content'],
                    source_document=doc['source_document'],
                    relevance_score=float(score),
                    document_type=doc['document_type'],
                    citation=f"{doc['category_name']} - {doc['source_document']}"
                )
                results.append(result)
        
        return results
    
    def get_relevant_clauses(self, context: str, legal_area: str = None) -> List[LegalClause]:
        """Get relevant legal clauses for given context"""
        corpus, embeddings = self.load_corpus_and_embeddings()
        
        # Filter for clauses if legal area specified
        if legal_area:
            corpus = [doc for doc in corpus if doc.get('legal_area', '').lower() == legal_area.lower()]
        
        # Focus on clauses category
        clause_corpus = [doc for doc in corpus if doc['category'] == 'clauses']
        
        if not clause_corpus:
            return []
        
        # Perform semantic search
        search_results = self.semantic_search(context, clause_corpus, embeddings, top_k=5)
        
        # Convert to LegalClause objects
        clauses = []
        for result in search_results:
            clause = LegalClause(
                id=hashlib.md5(result.content.encode()).hexdigest()[:8],
                content=result.content,
                source_document=result.source_document,
                legal_area=legal_area or "General",
                clause_type=self._determine_clause_type(result.content),
                relevance_score=result.relevance_score
            )
            clauses.append(clause)
        
        return clauses
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def _split_into_chunks(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into smaller chunks for better search"""
        # Split by double newlines (paragraphs) first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        import re
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return words
    
    def _determine_legal_area(self, filename: str) -> str:
        """Determine legal area from filename"""
        filename_lower = filename.lower()
        if 'employment' in filename_lower:
            return "Employment Law"
        elif 'contract' in filename_lower:
            return "Contract Law"
        elif 'liability' in filename_lower or 'indemnif' in filename_lower:
            return "Liability and Risk"
        elif 'intellectual' in filename_lower or 'ip' in filename_lower:
            return "Intellectual Property"
        elif 'termination' in filename_lower:
            return "Contract Termination"
        else:
            return "General"
    
    def _determine_document_type(self, category: str, filename: str) -> str:
        """Determine document type from category and filename"""
        if category == 'contracts':
            return "Contract Template"
        elif category == 'clauses':
            return "Legal Clause"
        elif category == 'precedents':
            return "Case Law"
        elif category == 'statutes':
            return "Statute/Regulation"
        else:
            return "Legal Document"
    
    def _determine_clause_type(self, content: str) -> str:
        """Determine clause type from content"""
        content_lower = content.lower()
        if 'termination' in content_lower:
            return "Termination Clause"
        elif 'liability' in content_lower or 'indemnif' in content_lower:
            return "Liability Clause"
        elif 'intellectual property' in content_lower or 'copyright' in content_lower:
            return "IP Clause"
        elif 'confidential' in content_lower or 'non-disclosure' in content_lower:
            return "Confidentiality Clause"
        else:
            return "General Clause"