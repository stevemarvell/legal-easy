#!/usr/bin/env python3
"""
ClauseExtractor - Core clause extraction service for the Legal AI System

This service handles the extraction of individual clauses from legal documents,
including boundary identification, content extraction, and processing status tracking.
"""

import re
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from ..models.clause import (
    ExtractedClause, ClauseBoundary, ClauseContent, ProcessingResult, 
    ExtractionMetrics, ClauseType, ExtractionMethod, ProcessingStatus
)
from .clause_storage import ClauseStorageService


class ClauseExtractor:
    """Service for extracting clauses from legal documents."""
    
    def __init__(self):
        """Initialize the clause extractor."""
        self.backend_dir = Path(__file__).parent.parent.parent
        
        # Processing status tracking
        self.processing_status: Dict[str, ProcessingStatus] = {}
    
    def extract_clauses_from_document(self, document_id: str) -> List[ExtractedClause]:
        """
        Extract clauses from a specific document.
        
        Args:
            document_id: ID of the document to process
            
        Returns:
            List of extracted clauses
        """
        try:
            # Update processing status
            self.processing_status[document_id] = ProcessingStatus.IN_PROGRESS
            
            # Load document content and metadata
            document_data = self._load_document_data(document_id)
            if not document_data:
                self.processing_status[document_id] = ProcessingStatus.FAILED
                return []
            
            content = document_data['content']
            category = document_data.get('category', 'unknown')
            title = document_data.get('name', document_id)
            
            # Identify clause boundaries based on document type
            boundaries = self.identify_clause_boundaries(content, category)
            
            # Extract clause content for each boundary
            extracted_clauses = []
            for i, boundary in enumerate(boundaries, 1):
                clause_content = self.extract_clause_content(content, boundary)
                
                # Create clause ID
                clause_id = f"{document_id}_clause_{i:03d}"
                
                # Create extracted clause
                clause = ExtractedClause(
                    id=clause_id,
                    title=clause_content.title,
                    content=clause_content.content,
                    source_document_id=document_id,
                    source_document_title=title,
                    category=category,
                    clause_number=i,
                    legal_concepts=clause_content.legal_concepts,
                    metadata={
                        'extraction_timestamp': datetime.now().isoformat(),
                        'extraction_method': self._get_extraction_method(category),
                        'confidence_score': boundary.confidence_score,
                        'formatting_preserved': clause_content.formatting_preserved,
                        'original_section': boundary.title,
                        'clause_type': boundary.clause_type
                    }
                )
                
                extracted_clauses.append(clause)
            
            # Save extracted clauses to individual JSON files
            self._save_clauses_to_files(extracted_clauses)
            
            # Update processing status
            self.processing_status[document_id] = ProcessingStatus.COMPLETED
            
            return extracted_clauses
            
        except Exception as e:
            print(f"Error extracting clauses from document {document_id}: {e}")
            self.processing_status[document_id] = ProcessingStatus.FAILED
            return []
    
    def process_all_unprocessed_documents(self) -> ProcessingResult:
        """
        Process all unprocessed documents in the corpus.
        
        Returns:
            Processing result summary
        """
        try:
            start_time = time.time()
            
            # Load corpus items
            corpus_items = self._load_corpus_items()
            total_clauses = 0
            processed_documents = 0
            
            for item in corpus_items:
                document_id = item.get('id')
                if not document_id:
                    continue
                
                # Check if already processed
                if self._is_document_processed(document_id):
                    continue
                
                # Extract clauses
                clauses = self.extract_clauses_from_document(document_id)
                total_clauses += len(clauses)
                processed_documents += 1
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                document_id="batch_processing",
                status=ProcessingStatus.COMPLETED,
                clauses_extracted=total_clauses,
                processing_time_seconds=processing_time,
                extraction_method=ExtractionMethod.AI_TEXT_ANALYSIS
            )
            
        except Exception as e:
            return ProcessingResult(
                document_id="batch_processing",
                status=ProcessingStatus.FAILED,
                error_message=str(e),
                extraction_method=ExtractionMethod.AI_TEXT_ANALYSIS
            )
    
    def identify_clause_boundaries(self, content: str, document_type: str) -> List[ClauseBoundary]:
        """
        Identify clause boundaries within document content.
        All documents follow the pattern: Title/Summary + Numbered clauses
        
        Args:
            content: Document content
            document_type: Type of document (contracts, clauses, precedents, statutes)
            
        Returns:
            List of identified clause boundaries
        """
        # All document types follow the same pattern: header + numbered clauses
        return self._extract_header_and_numbered_clauses(content, document_type)
    
    def extract_clause_content(self, content: str, boundary: ClauseBoundary) -> ClauseContent:
        """
        Extract clause content from document based on boundary.
        
        Args:
            content: Full document content
            boundary: Clause boundary information
            
        Returns:
            Extracted clause content
        """
        try:
            # Extract content within boundary
            clause_text = content[boundary.start_position:boundary.end_position].strip()
            
            # Identify legal concepts (basic keyword matching)
            legal_concepts = self._identify_legal_concepts(clause_text)
            
            return ClauseContent(
                title=boundary.title,
                content=clause_text,
                formatting_preserved=True,
                legal_concepts=legal_concepts
            )
            
        except Exception as e:
            print(f"Error extracting clause content: {e}")
            return ClauseContent(
                title=boundary.title,
                content="",
                formatting_preserved=False,
                legal_concepts=[]
            )
    
    def get_processing_status(self, document_id: str) -> ProcessingStatus:
        """Get processing status for a document."""
        return self.processing_status.get(document_id, ProcessingStatus.NOT_STARTED)
    
    def update_processing_status(self, document_id: str, status: ProcessingStatus) -> None:
        """Update processing status for a document."""
        self.processing_status[document_id] = status
    
    # Private helper methods
    
    def _load_document_data(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Load document data from corpus."""
        try:
            from .corpus_service import CorpusService
            return CorpusService.load_corpus_item_by_id(document_id)
        except Exception as e:
            print(f"Error loading document data for {document_id}: {e}")
            return None
    
    def _load_corpus_items(self) -> List[Dict[str, Any]]:
        """Load all corpus items."""
        try:
            from .corpus_service import CorpusService
            return CorpusService.load_corpus_items()
        except Exception as e:
            print(f"Error loading corpus items: {e}")
            return []
    
    def _is_document_processed(self, document_id: str) -> bool:
        """Check if document has already been processed."""
        # Check if any clause files exist for this document
        clauses_dir = self.backend_dir / "data" / "ai" / "research_corpus" / "clauses"
        if not clauses_dir.exists():
            return False
        
        pattern = f"{document_id}_clause_*.json"
        clause_files = list(clauses_dir.glob(pattern))
        return len(clause_files) > 0
    
    def _get_extraction_method(self, category: str) -> str:
        """Get extraction method based on document category."""
        method_map = {
            "clauses": ExtractionMethod.NUMBERED_LIST_PARSER,
            "contracts": ExtractionMethod.SECTION_HEADER_PARSER,
            "precedents": ExtractionMethod.AI_TEXT_ANALYSIS,
            "statutes": ExtractionMethod.LEGAL_SECTION_PARSER
        }
        return method_map.get(category, ExtractionMethod.PARAGRAPH_SPLITTER)
    
    def _extract_header_and_numbered_clauses(self, content: str, document_type: str) -> List[ClauseBoundary]:
        """
        Extract document header/summary and numbered clauses.
        All documents follow the pattern: Title/Summary + Numbered clauses (1. TITLE)
        """
        boundaries = []
        
        # Pattern for numbered clauses like "1. TITLE" or "1. Title"
        # More flexible pattern to handle various title formats
        pattern = r'^(\d+)\.\s+([A-Z][A-Z\s\-&/()]+)$'
        lines = content.split('\n')
        
        # Find the first numbered clause to determine where header ends
        first_clause_line = None
        first_clause_pos = None
        
        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())
            if match and match.group(1) == "1":  # First numbered clause
                first_clause_line = i
                first_clause_pos = content.find(line)
                break
        
        # Extract header/summary if there's content before first numbered clause
        if first_clause_pos and first_clause_pos > 0:
            header_content = content[:first_clause_pos].strip()
            if header_content:
                # Get document title from first line
                header_lines = header_content.split('\n')
                document_title = header_lines[0].strip() if header_lines else "Document Header"
                
                boundaries.append(ClauseBoundary(
                    start_position=0,
                    end_position=first_clause_pos,
                    title=f"DOCUMENT HEADER: {document_title}",
                    clause_type=ClauseType.TITLED,
                    confidence_score=0.95
                ))
        
        # Extract numbered clauses
        current_start = first_clause_pos if first_clause_pos else 0
        current_title = ""
        
        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())
            if match:
                # If we have a previous clause, create boundary
                if current_title and current_start < len(content):
                    end_pos = content.find(line, current_start)
                    if end_pos > current_start:
                        clause_type = self._get_clause_type_for_document(document_type)
                        boundaries.append(ClauseBoundary(
                            start_position=current_start,
                            end_position=end_pos,
                            title=current_title,
                            clause_type=clause_type,
                            confidence_score=0.95
                        ))
                
                # Start new clause
                current_title = match.group(2).strip()
                current_start = content.find(line)
        
        # Handle last clause
        if current_title and current_start < len(content):
            clause_type = self._get_clause_type_for_document(document_type)
            boundaries.append(ClauseBoundary(
                start_position=current_start,
                end_position=len(content),
                title=current_title,
                clause_type=clause_type,
                confidence_score=0.95
            ))
        
        return boundaries
    
    def _get_clause_type_for_document(self, document_type: str) -> ClauseType:
        """Get appropriate clause type based on document category."""
        type_map = {
            "contracts": ClauseType.SECTION,
            "clauses": ClauseType.NUMBERED,
            "precedents": ClauseType.NUMBERED,
            "statutes": ClauseType.SECTION
        }
        return type_map.get(document_type, ClauseType.NUMBERED)
    
    def _extract_paragraphs(self, content: str) -> List[ClauseBoundary]:
        """Fallback paragraph-based extraction."""
        boundaries = []
        paragraphs = content.split('\n\n')
        
        current_pos = 0
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                # Use first line or first few words as title
                title = paragraph.split('\n')[0][:50] + "..." if len(paragraph) > 50 else paragraph.split('\n')[0]
                
                boundaries.append(ClauseBoundary(
                    start_position=current_pos,
                    end_position=current_pos + len(paragraph),
                    title=title,
                    clause_type=ClauseType.PARAGRAPH,
                    confidence_score=0.7
                ))
            
            current_pos += len(paragraph) + 2  # +2 for \n\n
        
        return boundaries
    
    def _identify_legal_concepts(self, text: str) -> List[str]:
        """Identify legal concepts in text using keyword matching."""
        concepts = []
        text_lower = text.lower()
        
        # Enhanced legal concept keywords with more comprehensive matching
        concept_keywords = {
            'termination': ['terminat', 'dismiss', 'end', 'expir', 'cease', 'conclude'],
            'liability': ['liabil', 'damag', 'loss', 'harm', 'responsible', 'accountable'],
            'confidentiality': ['confidential', 'secret', 'disclos', 'proprietary', 'private', 'non-disclosure'],
            'employment': ['employ', 'work', 'job', 'position', 'staff', 'personnel'],
            'contract': ['contract', 'agreement', 'deal', 'arrangement', 'understanding'],
            'payment': ['pay', 'salary', 'wage', 'compensation', 'remuneration', 'fee', 'cost'],
            'notice': ['notice', 'notification', 'inform', 'advise', 'communicate'],
            'breach': ['breach', 'violat', 'default', 'fail', 'non-compliance'],
            'intellectual_property': ['intellectual property', 'copyright', 'patent', 'trademark', 'ip rights'],
            'non_compete': ['non-compete', 'non compete', 'restraint', 'covenant', 'restriction'],
            'discrimination': ['discriminat', 'equal', 'harassment', 'bias', 'prejudice'],
            'health_safety': ['health', 'safety', 'welfare', 'wellbeing', 'security'],
            'data_protection': ['data protection', 'privacy', 'gdpr', 'personal data', 'information'],
            'dispute_resolution': ['dispute', 'arbitration', 'mediation', 'court', 'litigation', 'resolution'],
            'insurance': ['insurance', 'insure', 'cover', 'policy', 'claim', 'premium'],
            'indemnity': ['indemnity', 'indemnif', 'compensat', 'reimburse', 'protect'],
            'force_majeure': ['force majeure', 'act of god', 'unforeseeable', 'beyond control'],
            'governing_law': ['governing law', 'jurisdiction', 'applicable law', 'legal system'],
            'entire_agreement': ['entire agreement', 'whole agreement', 'complete agreement', 'supersede'],
            'amendment': ['amendment', 'modify', 'change', 'alter', 'update', 'revise'],
            'assignment': ['assignment', 'transfer', 'delegate', 'assign'],
            'severability': ['severability', 'severable', 'invalid', 'unenforceable'],
            'waiver': ['waiver', 'waive', 'relinquish', 'abandon', 'give up'],
            'performance': ['performance', 'perform', 'execute', 'fulfill', 'carry out'],
            'standards': ['standard', 'quality', 'specification', 'requirement', 'criteria'],
            'review': ['review', 'assess', 'evaluate', 'examine', 'inspect'],
            'approval': ['approval', 'approve', 'consent', 'authorize', 'permit'],
            'escalation': ['escalat', 'refer', 'elevate', 'raise', 'report'],
            'investigation': ['investigat', 'inquir', 'examine', 'research', 'study'],
            'evidence': ['evidence', 'proof', 'documentation', 'record', 'witness'],
            'precedent': ['precedent', 'case law', 'judicial', 'court decision'],
            'regulation': ['regulation', 'rule', 'law', 'statute', 'requirement'],
            'compliance': ['compliance', 'comply', 'conform', 'adhere', 'follow'],
            'audit': ['audit', 'inspection', 'examination', 'check', 'verification']
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                concepts.append(concept)
        
        return concepts
    
    def _save_clauses_to_files(self, clauses: List[ExtractedClause]) -> None:
        """Save extracted clauses to individual JSON files."""
        # Ensure clauses directory exists
        clauses_dir = self.backend_dir / "data" / "ai" / "research_corpus" / "clauses"
        clauses_dir.mkdir(parents=True, exist_ok=True)
        
        for clause in clauses:
            try:
                file_path = clauses_dir / f"{clause.id}.json"
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(clause.dict(), f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Error saving clause {clause.id}: {e}")