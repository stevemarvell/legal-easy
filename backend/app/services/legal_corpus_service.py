import os
import json
from typing import List, Dict, Any
from pathlib import Path
import hashlib
from sentence_transformers import SentenceTransformer
import numpy as np
from app.models.legal_research import LegalClause, SearchResult


class LegalCorpusService:
    """Service for managing legal document corpus and vector embeddings"""
    
    def __init__(self):
        self.corpus_path = Path("app/data/legal_corpus")
        self.embeddings_path = Path("app/data/embeddings")
        self.embeddings_path.mkdir(exist_ok=True)
        
        # Initialize sentence transformer model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Legal document categories
        self.categories = {
            'contracts': 'Contract Templates',
            'clauses': 'Legal Clauses',
            'precedents': 'Case Law and Precedents',
            'statutes': 'Statutes and Regulations'
        }
    
    def compile_legal_corpus(self) -> List[Dict[str, Any]]:
        """Compile all legal documents into structured corpus"""
        corpus = []
        
        for category, category_name in self.categories.items():
            category_path = self.corpus_path / category
            if category_path.exists():
                for file_path in category_path.glob("*.txt"):
                    content = self._read_file_content(file_path)
                    if content:
                        # Split content into chunks for better semantic search
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
    
    def generate_embeddings(self, corpus: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Generate vector embeddings for corpus documents"""
        embeddings = {}
        
        # Extract text content for embedding generation
        texts = [doc['content'] for doc in corpus]
        doc_ids = [doc['id'] for doc in corpus]
        
        # Generate embeddings in batches
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch_texts, convert_to_tensor=False)
            all_embeddings.extend(batch_embeddings)
        
        # Create embeddings dictionary
        for doc_id, embedding in zip(doc_ids, all_embeddings):
            embeddings[doc_id] = embedding
        
        return embeddings
    
    def save_corpus_and_embeddings(self, corpus: List[Dict[str, Any]], embeddings: Dict[str, np.ndarray]):
        """Save corpus metadata and embeddings to disk"""
        # Save corpus metadata
        corpus_file = self.embeddings_path / "legal_corpus.json"
        with open(corpus_file, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
        
        # Save embeddings
        embeddings_file = self.embeddings_path / "legal_embeddings.npz"
        np.savez_compressed(embeddings_file, **embeddings)
        
        # Save index mapping
        index_mapping = {doc['id']: i for i, doc in enumerate(corpus)}
        mapping_file = self.embeddings_path / "index_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump(index_mapping, f, indent=2)
    
    def load_corpus_and_embeddings(self) -> tuple[List[Dict[str, Any]], Dict[str, np.ndarray]]:
        """Load corpus and embeddings from disk"""
        corpus_file = self.embeddings_path / "legal_corpus.json"
        embeddings_file = self.embeddings_path / "legal_embeddings.npz"
        
        if not corpus_file.exists() or not embeddings_file.exists():
            return [], {}
        
        # Load corpus
        with open(corpus_file, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
        
        # Load embeddings
        embeddings_data = np.load(embeddings_file)
        embeddings = {key: embeddings_data[key] for key in embeddings_data.files}
        
        return corpus, embeddings
    
    def semantic_search(self, query: str, corpus: List[Dict[str, Any]], 
                       embeddings: Dict[str, np.ndarray], top_k: int = 10) -> List[SearchResult]:
        """Perform semantic search on legal corpus"""
        if not corpus or not embeddings:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_tensor=False)[0]
        
        # Calculate similarities
        similarities = []
        for doc in corpus:
            doc_id = doc['id']
            if doc_id in embeddings:
                doc_embedding = embeddings[doc_id]
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                similarities.append((doc, similarity))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc, score in similarities[:top_k]:
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
    
    def initialize_corpus(self):
        """Initialize the legal corpus and generate embeddings"""
        print("Compiling legal corpus...")
        corpus = self.compile_legal_corpus()
        
        print(f"Generating embeddings for {len(corpus)} documents...")
        embeddings = self.generate_embeddings(corpus)
        
        print("Saving corpus and embeddings...")
        self.save_corpus_and_embeddings(corpus, embeddings)
        
        print(f"Legal corpus initialized with {len(corpus)} documents")
        return len(corpus)
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def _split_into_chunks(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into smaller chunks for better semantic search"""
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