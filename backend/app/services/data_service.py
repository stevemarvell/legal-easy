#!/usr/bin/env python3
"""
DataService - Simplified data management service for the Legal AI System

This service handles all data operations including:
- Loading and managing cases, documents, research corpus, and playbooks
- Data structure analysis and validation
- File system operations and data integrity checks
- Index management and data synchronization
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime


class DataService:
    """Simplified data management service for all system data."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.cases_path = self.data_root / "cases"
        self.research_corpus_path = self.data_root / "research_corpus"
        self.playbooks_path = self.data_root / "playbooks"
        
        # Ensure data directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all required data directories exist."""
        for path in [self.cases_path, self.research_corpus_path, self.playbooks_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    # === CASES MANAGEMENT ===
    
    def load_cases(self) -> List[Dict[str, Any]]:
        """Load all cases from the cases index."""
        try:
            cases_index_path = self.cases_path / "cases_index.json"
            if not cases_index_path.exists():
                return []
            
            with open(cases_index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('cases', [])
        except Exception as e:
            print(f"Error loading cases: {e}")
            return []
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific case by ID."""
        cases = self.load_cases()
        for case in cases:
            if case.get('id') == case_id:
                return case
        return None
    
    def get_case_statistics(self) -> Dict[str, Any]:
        """Get statistics about all cases."""
        cases = self.load_cases()
        total_cases = len(cases)
        
        # Count by status
        status_counts = {}
        for case in cases:
            status = case.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count recent activity (last 30 days)
        recent_count = 0
        thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        
        for case in cases:
            created_date = case.get('created_date', '')
            if created_date:
                try:
                    case_timestamp = datetime.fromisoformat(created_date.replace('Z', '+00:00')).timestamp()
                    if case_timestamp > thirty_days_ago:
                        recent_count += 1
                except:
                    pass
        
        return {
            "total_cases": total_cases,
            "active_cases": status_counts.get('Active', 0),
            "resolved_cases": status_counts.get('Resolved', 0),
            "under_review_cases": status_counts.get('Under Review', 0),
            "recent_activity_count": recent_count
        }
    
    # === DOCUMENTS MANAGEMENT ===
    
    def load_case_documents(self, case_id: str) -> List[Dict[str, Any]]:
        """Load all documents for a specific case."""
        try:
            case_docs_path = self.cases_path / "case_documents" / "case_documents_index.json"
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('documents', [])
                
                # Filter documents for the specific case
                case_documents = [doc for doc in documents if doc.get('case_id') == case_id]
                return case_documents
        except Exception as e:
            print(f"Error loading case documents: {e}")
            return []
    
    def get_document_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        try:
            case_docs_path = self.cases_path / "case_documents" / "case_documents_index.json"
            if not case_docs_path.exists():
                return None
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('documents', [])
                
                for doc in documents:
                    if doc.get('id') == document_id:
                        return doc
                return None
        except Exception as e:
            print(f"Error loading document: {e}")
            return None
    
    # === RESEARCH CORPUS MANAGEMENT ===
    
    def load_research_corpus(self) -> Dict[str, Any]:
        """Load the research corpus index."""
        try:
            corpus_index_path = self.research_corpus_path / "research_corpus_index.json"
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading research corpus: {e}")
            return {}
    
    def get_research_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific research corpus document by ID."""
        corpus = self.load_research_corpus()
        documents = corpus.get('documents', {})
        return documents.get(doc_id)
    
    def get_research_documents_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all research documents in a specific category."""
        corpus = self.load_research_corpus()
        categories = corpus.get('categories', {})
        
        if category not in categories:
            return []
        
        document_ids = categories[category].get('document_ids', [])
        documents = corpus.get('documents', {})
        
        return [documents[doc_id] for doc_id in document_ids if doc_id in documents]
    
    # === PLAYBOOKS MANAGEMENT ===
    
    def load_playbooks(self) -> List[Dict[str, Any]]:
        """Load all playbooks from the playbooks index."""
        try:
            playbooks_index_path = self.playbooks_path / "playbooks_index.json"
            if not playbooks_index_path.exists():
                return []
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('playbooks', [])
        except Exception as e:
            print(f"Error loading playbooks: {e}")
            return []
    
    def get_playbook_by_case_type(self, case_type: str) -> Optional[Dict[str, Any]]:
        """Get a playbook for a specific case type."""
        playbooks = self.load_playbooks()
        for playbook in playbooks:
            if playbook.get('case_type') == case_type:
                return playbook
        return None
    
    # === DATA ANALYSIS AND VALIDATION ===
    
    def analyze_data_structure(self) -> Dict[str, Any]:
        """Analyze the current data structure and generate a report."""
        analysis_results = {
            "metadata": {
                "analysis_date": datetime.now().isoformat(),
                "data_root": str(self.data_root),
                "total_files": 0,
                "total_directories": 0,
                "total_size_bytes": 0
            },
            "cases": {
                "total_cases": 0,
                "total_documents": 0,
                "status_distribution": {}
            },
            "research_corpus": {
                "total_documents": 0,
                "categories": {},
                "research_areas": []
            },
            "playbooks": {
                "total_playbooks": 0,
                "case_types": []
            },
            "issues_identified": [],
            "recommendations": []
        }
        
        try:
            # Analyze file system
            total_files = 0
            total_dirs = 0
            total_size = 0
            
            for root, dirs, files in os.walk(self.data_root):
                total_dirs += len(dirs)
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        total_files += 1
                        total_size += file_path.stat().st_size
            
            analysis_results["metadata"]["total_files"] = total_files
            analysis_results["metadata"]["total_directories"] = total_dirs
            analysis_results["metadata"]["total_size_bytes"] = total_size
            
            # Analyze cases
            cases = self.load_cases()
            analysis_results["cases"]["total_cases"] = len(cases)
            
            status_dist = {}
            for case in cases:
                status = case.get('status', 'Unknown')
                status_dist[status] = status_dist.get(status, 0) + 1
            analysis_results["cases"]["status_distribution"] = status_dist
            
            # Count total documents across all cases
            total_docs = 0
            for case in cases:
                case_docs = self.load_case_documents(case.get('id', ''))
                total_docs += len(case_docs)
            analysis_results["cases"]["total_documents"] = total_docs
            
            # Analyze research corpus
            corpus = self.load_research_corpus()
            corpus_docs = corpus.get('documents', {})
            analysis_results["research_corpus"]["total_documents"] = len(corpus_docs)
            
            categories = corpus.get('categories', {})
            category_counts = {}
            for cat_name, cat_data in categories.items():
                category_counts[cat_name] = len(cat_data.get('document_ids', []))
            analysis_results["research_corpus"]["categories"] = category_counts
            analysis_results["research_corpus"]["research_areas"] = corpus.get('research_areas', [])
            
            # Analyze playbooks
            playbooks = self.load_playbooks()
            analysis_results["playbooks"]["total_playbooks"] = len(playbooks)
            analysis_results["playbooks"]["case_types"] = [pb.get('case_type') for pb in playbooks]
            
            # Identify potential issues
            if len(cases) == 0:
                analysis_results["issues_identified"].append("No cases found in the system")
            
            if len(corpus_docs) == 0:
                analysis_results["issues_identified"].append("No research corpus documents found")
            
            if len(playbooks) == 0:
                analysis_results["issues_identified"].append("No playbooks found in the system")
            
            # Generate recommendations
            if total_docs == 0:
                analysis_results["recommendations"].append("Consider adding sample documents to cases")
            
            if len(corpus.get('research_areas', [])) < 3:
                analysis_results["recommendations"].append("Consider expanding research areas coverage")
            
        except Exception as e:
            analysis_results["issues_identified"].append(f"Error during analysis: {str(e)}")
        
        return analysis_results
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate data integrity across all data sources."""
        validation_results = {
            "validation_date": datetime.now().isoformat(),
            "overall_status": "PASS",
            "cases_validation": {"status": "PASS", "issues": []},
            "documents_validation": {"status": "PASS", "issues": []},
            "corpus_validation": {"status": "PASS", "issues": []},
            "playbooks_validation": {"status": "PASS", "issues": []}
        }
        
        try:
            # Validate cases
            cases = self.load_cases()
            for case in cases:
                if not case.get('id'):
                    validation_results["cases_validation"]["issues"].append("Case missing ID")
                    validation_results["cases_validation"]["status"] = "FAIL"
                
                if not case.get('title'):
                    validation_results["cases_validation"]["issues"].append(f"Case {case.get('id')} missing title")
                    validation_results["cases_validation"]["status"] = "FAIL"
            
            # Validate research corpus
            corpus = self.load_research_corpus()
            documents = corpus.get('documents', {})
            
            for doc_id, doc_data in documents.items():
                if not doc_data.get('filename'):
                    validation_results["corpus_validation"]["issues"].append(f"Document {doc_id} missing filename")
                    validation_results["corpus_validation"]["status"] = "FAIL"
                
                # Check if file exists
                category = doc_data.get('category')
                filename = doc_data.get('filename')
                if category and filename:
                    file_path = self.research_corpus_path / category / filename
                    if not file_path.exists():
                        validation_results["corpus_validation"]["issues"].append(f"File not found: {file_path}")
                        validation_results["corpus_validation"]["status"] = "FAIL"
            
            # Validate playbooks
            playbooks = self.load_playbooks()
            for playbook in playbooks:
                if not playbook.get('id'):
                    validation_results["playbooks_validation"]["issues"].append("Playbook missing ID")
                    validation_results["playbooks_validation"]["status"] = "FAIL"
                
                if not playbook.get('case_type'):
                    validation_results["playbooks_validation"]["issues"].append(f"Playbook {playbook.get('id')} missing case_type")
                    validation_results["playbooks_validation"]["status"] = "FAIL"
            
            # Set overall status
            if any(v["status"] == "FAIL" for v in [
                validation_results["cases_validation"],
                validation_results["documents_validation"],
                validation_results["corpus_validation"],
                validation_results["playbooks_validation"]
            ]):
                validation_results["overall_status"] = "FAIL"
        
        except Exception as e:
            validation_results["overall_status"] = "ERROR"
            validation_results["error"] = str(e)
        
        return validation_results
    
    # === UTILITY METHODS ===
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        return {
            "cases": self.get_case_statistics(),
            "research_corpus": {
                "total_documents": len(self.load_research_corpus().get('documents', {})),
                "categories": len(self.load_research_corpus().get('categories', {}))
            },
            "playbooks": {
                "total_playbooks": len(self.load_playbooks())
            },
            "data_analysis": self.analyze_data_structure()
        }