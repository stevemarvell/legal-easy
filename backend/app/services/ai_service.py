#!/usr/bin/env python3
"""
AIService - Simplified AI service for the Legal AI System

This service handles all AI-powered operations including:
- Document analysis and content extraction
- AI-powered case assessment
- Research corpus processing and embeddings
- Analysis result storage and retrieval
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class AIService:
    """Simplified AI service for document analysis and AI operations."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.ai_data_path = self.data_root / "ai"
        self.analysis_storage_path = self.ai_data_path / "analysis_results.json"
        
        # Ensure AI data directory exists
        self.ai_data_path.mkdir(parents=True, exist_ok=True)
    
    # === DOCUMENT ANALYSIS ===
    
    def analyze_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform AI analysis on a document.
        
        Note: This is a simplified implementation that extracts basic information.
        In a full implementation, this would integrate with OpenAI API or similar.
        """
        document_id = document.get('id', '')
        content = self._get_document_content(document)
        
        # Simplified analysis - in production this would use AI
        analysis = {
            "document_id": document_id,
            "analysis_date": datetime.now().isoformat(),
            "key_dates": self._extract_dates(content),
            "parties_involved": self._extract_parties(content),
            "document_type": self._classify_document_type(document, content),
            "summary": self._generate_summary(content),
            "key_clauses": self._extract_key_clauses(content),
            "confidence_scores": {
                "parties": 0.85,
                "dates": 0.90,
                "document_type": 0.95,
                "summary": 0.80
            }
        }
        
        return analysis
    
    def _get_document_content(self, document: Dict[str, Any]) -> str:
        """Get the full content of a document."""
        # Try to load from file if path exists
        content_path = document.get('full_content_path')
        if content_path and Path(content_path).exists():
            try:
                with open(content_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                pass
        
        # Fallback to content preview
        return document.get('content_preview', '')
    
    def _extract_dates(self, content: str) -> List[str]:
        """Extract key dates from document content."""
        import re
        
        # Simple date pattern matching
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD or YYYY-MM-DD
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates.extend(matches)
        
        # Return unique dates, limited to first 5
        return list(set(dates))[:5]
    
    def _extract_parties(self, content: str) -> List[str]:
        """Extract parties/entities from document content."""
        import re
        
        # Simple pattern matching for common legal entities
        party_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Person names (First Last)
            r'\b[A-Z][a-zA-Z\s]+ (?:Ltd|Limited|Inc|Corporation|Corp|Company|Co)\b',  # Company names
            r'\b[A-Z][a-zA-Z\s]+ (?:LLC|LLP|Partnership)\b'  # Other business entities
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, content)
            parties.extend(matches)
        
        # Return unique parties, limited to first 5
        return list(set(parties))[:5]
    
    def _classify_document_type(self, document: Dict[str, Any], content: str) -> str:
        """Classify the document type based on content and metadata."""
        doc_type = document.get('type', '').lower()
        
        # Use existing type if available
        if doc_type:
            return doc_type.title()
        
        # Simple keyword-based classification
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['employment', 'employee', 'employer', 'termination']):
            return 'Employment Document'
        elif any(word in content_lower for word in ['contract', 'agreement', 'terms']):
            return 'Contract'
        elif any(word in content_lower for word in ['confidential', 'non-disclosure', 'nda']):
            return 'Confidentiality Agreement'
        elif any(word in content_lower for word in ['invoice', 'payment', 'billing']):
            return 'Financial Document'
        else:
            return 'Legal Document'
    
    def _generate_summary(self, content: str) -> str:
        """Generate a simple summary of the document."""
        # Simple summary - take first few sentences
        sentences = content.split('.')[:3]
        summary = '. '.join(sentence.strip() for sentence in sentences if sentence.strip())
        
        if len(summary) > 200:
            summary = summary[:200] + "..."
        
        return summary or "Document summary not available"
    
    def _extract_key_clauses(self, content: str) -> List[str]:
        """Extract key clauses from the document."""
        import re
        
        # Look for common legal clause indicators
        clause_patterns = [
            r'(?:termination|liability|confidentiality|intellectual property|payment|dispute resolution)\s+clause',
            r'(?:shall|must|will)\s+[^.]{20,100}',
            r'(?:party|parties)\s+(?:agree|acknowledges?|undertakes?)\s+[^.]{20,100}'
        ]
        
        clauses = []
        for pattern in clause_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            clauses.extend(matches)
        
        # Clean up and return unique clauses
        cleaned_clauses = []
        for clause in clauses:
            clause = clause.strip()
            if len(clause) > 20 and clause not in cleaned_clauses:
                cleaned_clauses.append(clause)
        
        return cleaned_clauses[:5]  # Limit to 5 key clauses
    
    # === ANALYSIS STORAGE ===
    
    def save_analysis(self, document_id: str, analysis: Dict[str, Any]) -> bool:
        """Save analysis results to storage."""
        try:
            # Load existing analyses
            analyses = self._load_analyses()
            
            # Add or update analysis
            analyses[document_id] = analysis
            
            # Save back to file
            with open(self.analysis_storage_path, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return False
    
    def get_analysis(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get stored analysis results for a document."""
        try:
            analyses = self._load_analyses()
            return analyses.get(document_id)
        except Exception as e:
            print(f"Error loading analysis: {e}")
            return None
    
    def delete_analysis(self, document_id: str) -> bool:
        """Delete stored analysis results for a document."""
        try:
            analyses = self._load_analyses()
            if document_id in analyses:
                del analyses[document_id]
                
                with open(self.analysis_storage_path, 'w', encoding='utf-8') as f:
                    json.dump(analyses, f, indent=2, ensure_ascii=False)
                
                return True
            return False
        except Exception as e:
            print(f"Error deleting analysis: {e}")
            return False
    
    def clear_all_analyses(self) -> bool:
        """Clear all stored analysis results."""
        try:
            with open(self.analysis_storage_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            return True
        except Exception as e:
            print(f"Error clearing analyses: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get statistics about stored analyses."""
        try:
            analyses = self._load_analyses()
            
            total_analyses = len(analyses)
            analysis_dates = []
            
            for analysis in analyses.values():
                if 'analysis_date' in analysis:
                    analysis_dates.append(analysis['analysis_date'])
            
            return {
                "total_analyses": total_analyses,
                "storage_file": str(self.analysis_storage_path),
                "latest_analysis": max(analysis_dates) if analysis_dates else None,
                "oldest_analysis": min(analysis_dates) if analysis_dates else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _load_analyses(self) -> Dict[str, Any]:
        """Load all stored analyses."""
        if not self.analysis_storage_path.exists():
            return {}
        
        try:
            with open(self.analysis_storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    # === BATCH OPERATIONS ===
    
    def run_batch_document_analysis(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run AI analysis on multiple documents."""
        results = {
            "start_time": datetime.now().isoformat(),
            "total_documents": len(documents),
            "successful_analyses": 0,
            "failed_analyses": 0,
            "analyses": [],
            "errors": []
        }
        
        for document in documents:
            try:
                document_id = document.get('id', '')
                print(f"Analyzing document: {document_id}")
                
                # Perform analysis
                analysis = self.analyze_document(document)
                
                # Save analysis
                if self.save_analysis(document_id, analysis):
                    results["successful_analyses"] += 1
                    results["analyses"].append({
                        "document_id": document_id,
                        "status": "success",
                        "analysis_summary": {
                            "parties_found": len(analysis.get("parties_involved", [])),
                            "dates_found": len(analysis.get("key_dates", [])),
                            "document_type": analysis.get("document_type"),
                            "confidence": analysis.get("confidence_scores", {}).get("summary", 0)
                        }
                    })
                else:
                    results["failed_analyses"] += 1
                    results["errors"].append(f"Failed to save analysis for {document_id}")
                
            except Exception as e:
                results["failed_analyses"] += 1
                results["errors"].append(f"Error analyzing {document.get('id', 'unknown')}: {str(e)}")
        
        results["end_time"] = datetime.now().isoformat()
        return results
    
    # === RESEARCH CORPUS PROCESSING ===
    
    def initialize_research_corpus(self, corpus_path: Path) -> int:
        """
        Initialize research corpus processing.
        
        Note: This is a simplified implementation. In production, this would
        generate embeddings and set up vector search capabilities.
        """
        try:
            if not corpus_path.exists():
                raise FileNotFoundError(f"Research corpus directory not found: {corpus_path}")
            
            # Load corpus index
            index_path = corpus_path / "research_corpus_index.json"
            if not index_path.exists():
                raise FileNotFoundError(f"Research corpus index not found: {index_path}")
            
            with open(index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            processed_count = 0
            
            # Process each document (simplified - would generate embeddings in production)
            for doc_id, doc_info in documents.items():
                category = doc_info.get('category')
                filename = doc_info.get('filename')
                
                if category and filename:
                    file_path = corpus_path / category / filename
                    if file_path.exists():
                        # In production: generate embeddings, chunk content, etc.
                        processed_count += 1
                        print(f"Processed: {doc_id} - {doc_info.get('name')}")
            
            print(f"Successfully processed {processed_count} research corpus documents")
            return processed_count
            
        except Exception as e:
            print(f"Error initializing research corpus: {e}")
            raise
    
    def test_research_corpus(self) -> Dict[str, Any]:
        """Test research corpus functionality."""
        return {
            "test_date": datetime.now().isoformat(),
            "status": "simplified_implementation",
            "message": "Research corpus testing requires full AI implementation with embeddings",
            "available_features": [
                "Document loading",
                "Basic content processing",
                "Index validation"
            ],
            "missing_features": [
                "Vector embeddings",
                "Semantic search",
                "Similarity scoring"
            ]
        }