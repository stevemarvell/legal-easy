#!/usr/bin/env python3
"""
DataService - Simplified data service for the Legal AI System

This service handles all JSON data loading and searching operations including:
- Loading cases, documents, research corpus, and playbooks from JSON files
- Simple search functionality across all data types
- Direct file access without complex repository patterns
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DataService:
    """Single service for all JSON data loading and searching."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.cases_path = self.data_root / "cases"
        self.research_corpus_path = self.data_root / "research_corpus"
        self.playbooks_path = self.data_root / "playbooks"
    
    # === CASES MANAGEMENT ===
    
    @staticmethod
    def load_cases() -> List[Dict[str, Any]]:
        """Load all cases from the cases index."""
        try:
            cases_index_path = Path("data/cases/cases_index.json")
            if not cases_index_path.exists():
                return []
            
            with open(cases_index_path, 'r', encoding='utf-8') as f:
                cases_data = json.load(f)
                # Handle both array format and object with 'cases' key
                if isinstance(cases_data, list):
                    return cases_data
                return cases_data.get('cases', [])
        except Exception as e:
            print(f"Error loading cases: {e}")
            return []
    
    # === DOCUMENTS MANAGEMENT ===
    
    @staticmethod
    def load_case_documents(case_id: str) -> List[Dict[str, Any]]:
        """Load all documents for a specific case."""
        try:
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
                
                # Filter documents for the specific case
                case_documents = [doc for doc in documents if doc.get('case_id') == case_id]
                
                # Add analysis_completed field by checking if analysis exists
                for doc in case_documents:
                    doc['analysis_completed'] = DataService._has_document_analysis(doc.get('id'))
                
                return case_documents
        except Exception as e:
            print(f"Error loading case documents: {e}")
            return []
    
    @staticmethod
    def load_document_content(doc_id: str) -> str:
        """Load the full content of a document by ID."""
        try:
            # First get document metadata to find the content path
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return ""
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
                
                # Find the document
                document = None
                for doc in documents:
                    if doc.get('id') == doc_id:
                        document = doc
                        break
                
                if not document:
                    return ""
                
                # Get content from file path
                content_path = document.get('full_content_path', '')
                if content_path:
                    # Fix the path - replace 'data/case_documents' with 'data/cases/case_documents'
                    if content_path.startswith('data/case_documents'):
                        content_path = content_path.replace('data/case_documents', 'data/cases/case_documents')
                    
                    # Try different path constructions
                    possible_paths = [
                        Path(content_path),  # Direct path
                        Path("data") / content_path,  # Prepend data/
                        Path(content_path.replace('data/', '')),  # Remove data/ prefix
                    ]
                    
                    for full_path in possible_paths:
                        if full_path.exists():
                            with open(full_path, 'r', encoding='utf-8') as content_file:
                                return content_file.read()
                
                # Fallback to content preview
                return document.get('content_preview', '')
                
        except Exception as e:
            print(f"Error loading document content: {e}")
            return ""
    
    # === RESEARCH CORPUS MANAGEMENT ===
    
    @staticmethod
    def load_corpus_by_category(category: str) -> List[Dict[str, Any]]:
        """Load research corpus documents by category (contracts, clauses, precedents, statutes)."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            # Get documents for the specified category
            categories = corpus_data.get('categories', {})
            if category not in categories:
                return []
            
            document_ids = categories[category].get('document_ids', [])
            documents = corpus_data.get('documents', {})
            
            # Return list of documents for the category
            result = []
            for doc_id in document_ids:
                if doc_id in documents:
                    doc = documents[doc_id].copy()
                    doc['id'] = doc_id  # Ensure ID is included
                    result.append(doc)
            
            return result
        except Exception as e:
            print(f"Error loading corpus by category: {e}")
            return []
    
    # === PLAYBOOKS MANAGEMENT ===
    
    @staticmethod
    def load_playbooks() -> List[Dict[str, Any]]:
        """Load all playbooks from the playbooks index."""
        try:
            playbooks_index_path = Path("data/playbooks/playbooks_index.json")
            if not playbooks_index_path.exists():
                return []
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                playbooks_data = json.load(f)
                # Handle both array format and object with 'playbooks' key
                if isinstance(playbooks_data, list):
                    return playbooks_data
                return playbooks_data.get('playbooks', [])
        except Exception as e:
            print(f"Error loading playbooks: {e}")
            return []
    
    # === SEARCH METHODS ===
    
    @staticmethod
    def search_cases(query: str) -> List[Dict[str, Any]]:
        """Search cases by title, summary, or client name."""
        try:
            cases = DataService.load_cases()
            if not query:
                return cases
            
            query_lower = query.lower()
            filtered_cases = []
            
            for case in cases:
                # Search in title, summary, client_name, and key_parties
                searchable_text = " ".join([
                    case.get('title', ''),
                    case.get('summary', ''),
                    case.get('client_name', ''),
                    " ".join(case.get('key_parties', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_cases.append(case)
            
            return filtered_cases
        except Exception as e:
            print(f"Error searching cases: {e}")
            return []
    
    @staticmethod
    def search_documents(query: str) -> List[Dict[str, Any]]:
        """Search documents by name, type, or content preview."""
        try:
            # Load all documents from all cases
            case_docs_path = Path("data/cases/case_documents/case_documents_index.json")
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('case_documents', [])
            
            if not query:
                return documents
            
            query_lower = query.lower()
            filtered_documents = []
            
            for doc in documents:
                # Search in name, type, and content_preview
                searchable_text = " ".join([
                    doc.get('name', ''),
                    doc.get('type', ''),
                    doc.get('content_preview', '')
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_documents.append(doc)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    @staticmethod
    def search_corpus(query: str) -> List[Dict[str, Any]]:
        """Search research corpus using concept-based searching."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            concepts_path = Path("data/ai/research_corpus/research_concepts.json")
            
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            
            if not query:
                # Return all documents as list
                result = []
                for doc_id, doc_data in documents.items():
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    result.append(doc)
                return result
            
            query_lower = query.lower()
            filtered_documents = []
            
            # Load legal concepts for enhanced searching
            legal_concepts = {}
            if concepts_path.exists():
                with open(concepts_path, 'r', encoding='utf-8') as f:
                    concepts_data = json.load(f)
                    legal_concepts = concepts_data.get('legal_concepts', {})
            
            # Find matching concepts first
            matching_concept_ids = []
            for concept_id, concept_data in legal_concepts.items():
                concept_text = " ".join([
                    concept_data.get('name', ''),
                    concept_data.get('definition', '')
                ]).lower()
                
                if query_lower in concept_text:
                    matching_concept_ids.append(concept_id)
            
            for doc_id, doc_data in documents.items():
                # Search in name, description, research_areas, and legal concepts
                searchable_text = " ".join([
                    doc_data.get('title', ''),
                    doc_data.get('description', ''),
                    " ".join(doc_data.get('research_areas', []))
                ]).lower()
                
                # Check if document contains matching legal concepts
                doc_legal_concepts = doc_data.get('legal_concepts', [])
                has_matching_concept = any(concept_id in matching_concept_ids for concept_id in doc_legal_concepts)
                
                if query_lower in searchable_text or has_matching_concept:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    # Add relevance score based on concept matching
                    doc['concept_match'] = has_matching_concept
                    filtered_documents.append(doc)
            
            # Sort by concept relevance (concept matches first)
            filtered_documents.sort(key=lambda x: x.get('concept_match', False), reverse=True)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching corpus: {e}")
            return []
    
    # === CORPUS SPECIFIC METHODS ===
    
    @staticmethod
    def load_corpus_categories() -> Dict[str, Dict[str, Any]]:
        """Load all corpus categories."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('categories', {})
        except Exception as e:
            print(f"Error loading corpus categories: {e}")
            return {}
    
    @staticmethod
    def load_corpus_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific corpus item by ID with full content."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return None
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            if item_id not in documents:
                return None
            
            item = documents[item_id].copy()
            item['id'] = item_id
            
            # Load full content from file
            filename = item.get('filename', '')
            category = item.get('category', '')
            
            if filename and category:
                content_path = Path(f"data/research_corpus/{category}/{filename}")
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()
                else:
                    item['content'] = ""
            
            return item
        except Exception as e:
            print(f"Error loading corpus item: {e}")
            return None
    
    @staticmethod
    def load_corpus_content_file(category: str, filename: str) -> str:
        """Load corpus content file by category and filename."""
        try:
            content_path = Path(f"data/research_corpus/{category}/{filename}")
            if content_path.exists():
                with open(content_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            print(f"Error loading corpus content file: {e}")
            return ""
    
    @staticmethod
    def load_corpus_metadata() -> Dict[str, Any]:
        """Load corpus metadata."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return {}
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('corpus_metadata', {})
        except Exception as e:
            print(f"Error loading corpus metadata: {e}")
            return {}
    
    @staticmethod
    def get_corpus_research_areas() -> List[str]:
        """Get all research areas from corpus."""
        try:
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            if not corpus_index_path.exists():
                return []
            
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
                
            return corpus_data.get('research_areas', [])
        except Exception as e:
            print(f"Error loading research areas: {e}")
            return []
    
    @staticmethod
    def get_related_corpus_items(item_id: str) -> List[Dict[str, Any]]:
        """Get related corpus items based on research areas, category, and legal concepts."""
        try:
            # First get the item to find its research areas and category
            item = DataService.load_corpus_item_by_id(item_id)
            if not item:
                return []
            
            item_research_areas = set(item.get('research_areas', []))
            item_category = item.get('category', '')
            item_legal_concepts = set(item.get('legal_concepts', []))
            
            # Load all corpus items
            corpus_index_path = Path("data/ai/research_corpus/research_corpus_index.json")
            with open(corpus_index_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            
            documents = corpus_data.get('documents', {})
            related_items = []
            
            for doc_id, doc_data in documents.items():
                if doc_id == item_id:  # Skip the item itself
                    continue
                
                doc_research_areas = set(doc_data.get('research_areas', []))
                doc_category = doc_data.get('category', '')
                doc_legal_concepts = set(doc_data.get('legal_concepts', []))
                
                # Calculate relevance based on shared research areas, category, and legal concepts
                shared_areas = item_research_areas.intersection(doc_research_areas)
                shared_concepts = item_legal_concepts.intersection(doc_legal_concepts)
                same_category = item_category == doc_category
                
                if shared_areas or same_category or shared_concepts:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    # Add relevance score (concepts weighted highest, then areas, then category)
                    relevance_score = len(shared_concepts) * 3 + len(shared_areas) * 2 + (1 if same_category else 0)
                    doc['relevance_score'] = relevance_score
                    related_items.append(doc)
            
            # Sort by relevance score (highest first)
            related_items.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Return top 5 related items
            return related_items[:5]
        except Exception as e:
            print(f"Error getting related corpus items: {e}")
            return []
    
    @staticmethod
    def load_legal_concepts() -> Dict[str, Dict[str, Any]]:
        """Load all legal concepts from research_concepts.json."""
        try:
            concepts_path = Path("data/ai/research_corpus/research_concepts.json")
            if not concepts_path.exists():
                return {}
            
            with open(concepts_path, 'r', encoding='utf-8') as f:
                concepts_data = json.load(f)
                
            return concepts_data.get('legal_concepts', {})
        except Exception as e:
            print(f"Error loading legal concepts: {e}")
            return {}
    
    @staticmethod
    def load_concept_relationships() -> Dict[str, Dict[str, Any]]:
        """Load concept relationships from research_concepts.json."""
        try:
            concepts_path = Path("data/ai/research_corpus/research_concepts.json")
            if not concepts_path.exists():
                return {}
            
            with open(concepts_path, 'r', encoding='utf-8') as f:
                concepts_data = json.load(f)
                
            return concepts_data.get('concept_relationships', {})
        except Exception as e:
            print(f"Error loading concept relationships: {e}")
            return {}
    
    @staticmethod
    def get_concepts_for_corpus_item(item_id: str) -> List[Dict[str, Any]]:
        """Get legal concepts associated with a specific corpus item."""
        try:
            # Load the corpus item to get its legal concepts
            item = DataService.load_corpus_item_by_id(item_id)
            if not item:
                return []
            
            item_concept_ids = item.get('legal_concepts', [])
            
            # Load all legal concepts
            legal_concepts = DataService.load_legal_concepts()
            
            # Return the concepts for this item
            result = []
            for concept_id in item_concept_ids:
                if concept_id in legal_concepts:
                    concept = legal_concepts[concept_id].copy()
                    concept['id'] = concept_id
                    result.append(concept)
            
            return result
        except Exception as e:
            print(f"Error getting concepts for corpus item: {e}")
            return []
    
    # === CONCEPT ANALYSIS AND EXTRACTION ===
    
    @staticmethod
    def extract_concepts_from_text(text: str) -> List[str]:
        """Extract legal concepts from text content by matching against known concepts."""
        try:
            if not text:
                return []
            
            # Load all legal concepts
            legal_concepts = DataService.load_legal_concepts()
            
            text_lower = text.lower()
            found_concepts = []
            
            # Look for concept names and key terms in the text
            for concept_id, concept_data in legal_concepts.items():
                concept_name = concept_data.get('name', '').lower()
                concept_definition = concept_data.get('definition', '').lower()
                
                # Check if concept name appears in text
                if concept_name in text_lower:
                    found_concepts.append(concept_id)
                    continue
                
                # Check for key terms from the definition
                key_terms = DataService._extract_key_terms_from_definition(concept_definition)
                for term in key_terms:
                    if term in text_lower and len(term) > 3:  # Avoid short common words
                        found_concepts.append(concept_id)
                        break
            
            return list(set(found_concepts))  # Remove duplicates
        except Exception as e:
            print(f"Error extracting concepts from text: {e}")
            return []
    
    @staticmethod
    def _extract_key_terms_from_definition(definition: str) -> List[str]:
        """Extract key terms from a concept definition for matching."""
        # Simple keyword extraction - look for important legal terms
        key_terms = []
        
        # Split definition into words and look for legal terminology
        words = definition.lower().split()
        
        # Common legal term patterns
        legal_indicators = [
            'contract', 'agreement', 'clause', 'liability', 'breach', 'termination',
            'employment', 'dismissal', 'notice', 'statutory', 'legal', 'rights',
            'obligation', 'damages', 'remedy', 'intellectual', 'property',
            'confidential', 'disclosure', 'indemnification', 'consideration'
        ]
        
        for word in words:
            # Remove punctuation
            clean_word = word.strip('.,;:()[]{}"\'-')
            if clean_word in legal_indicators and len(clean_word) > 3:
                key_terms.append(clean_word)
        
        return key_terms
    
    @staticmethod
    def analyze_concept_relationships(concept_id: str) -> Dict[str, Any]:
        """Analyze relationships for a specific legal concept."""
        try:
            legal_concepts = DataService.load_legal_concepts()
            concept_relationships = DataService.load_concept_relationships()
            
            if concept_id not in legal_concepts:
                return {}
            
            concept = legal_concepts[concept_id]
            
            # Get direct relationships
            related_concept_ids = concept.get('related_concepts', [])
            related_concepts = []
            
            for related_id in related_concept_ids:
                if related_id in legal_concepts:
                    related_concept = legal_concepts[related_id].copy()
                    related_concept['id'] = related_id
                    related_concepts.append(related_concept)
            
            # Find concept clusters this concept belongs to
            concept_clusters = []
            for cluster_name, cluster_data in concept_relationships.items():
                cluster_concepts = cluster_data.get('concepts', [])
                if concept_id in cluster_concepts:
                    concept_clusters.append({
                        'name': cluster_name,
                        'description': cluster_data.get('description', ''),
                        'concepts': cluster_concepts
                    })
            
            # Get corpus references
            corpus_references = concept.get('corpus_references', [])
            
            return {
                'concept_id': concept_id,
                'concept_name': concept.get('name', ''),
                'definition': concept.get('definition', ''),
                'related_concepts': related_concepts,
                'concept_clusters': concept_clusters,
                'corpus_references': corpus_references,
                'relationship_strength': len(related_concept_ids)
            }
        except Exception as e:
            print(f"Error analyzing concept relationships: {e}")
            return {}
    
    @staticmethod
    def build_concept_relationship_map() -> Dict[str, List[str]]:
        """Build a comprehensive map of concept relationships."""
        try:
            legal_concepts = DataService.load_legal_concepts()
            relationship_map = {}
            
            for concept_id, concept_data in legal_concepts.items():
                related_concepts = concept_data.get('related_concepts', [])
                relationship_map[concept_id] = related_concepts
            
            return relationship_map
        except Exception as e:
            print(f"Error building concept relationship map: {e}")
            return {}
    
    @staticmethod
    def update_concept_analysis(concept_id: str, analysis_data: Dict[str, Any]) -> bool:
        """Update concept analysis in research_concepts.json."""
        try:
            concepts_path = Path("data/ai/research_corpus/research_concepts.json")
            if not concepts_path.exists():
                return False
            
            # Load existing data
            with open(concepts_path, 'r', encoding='utf-8') as f:
                concepts_data = json.load(f)
            
            # Update the specific concept
            legal_concepts = concepts_data.get('legal_concepts', {})
            if concept_id in legal_concepts:
                legal_concepts[concept_id].update(analysis_data)
                
                # Update metadata
                concepts_data['concepts_metadata']['last_updated'] = datetime.now().isoformat()
                
                # Save back to file
                with open(concepts_path, 'w', encoding='utf-8') as f:
                    json.dump(concepts_data, f, indent=2, ensure_ascii=False)
                
                return True
            
            return False
        except Exception as e:
            print(f"Error updating concept analysis: {e}")
            return False
    
    @staticmethod
    def analyze_corpus_item_concepts(item_id: str) -> Dict[str, Any]:
        """Analyze legal concepts for a specific corpus item."""
        try:
            # Load the corpus item with content
            item = DataService.load_corpus_item_by_id(item_id)
            if not item:
                return {}
            
            content = item.get('content', '')
            existing_concepts = item.get('legal_concepts', [])
            
            # Extract concepts from content
            extracted_concepts = DataService.extract_concepts_from_text(content)
            
            # Combine existing and extracted concepts
            all_concepts = list(set(existing_concepts + extracted_concepts))
            
            # Get detailed concept information
            legal_concepts = DataService.load_legal_concepts()
            concept_details = []
            
            for concept_id in all_concepts:
                if concept_id in legal_concepts:
                    concept = legal_concepts[concept_id].copy()
                    concept['id'] = concept_id
                    concept['source'] = 'existing' if concept_id in existing_concepts else 'extracted'
                    concept_details.append(concept)
            
            return {
                'item_id': item_id,
                'item_title': item.get('title', ''),
                'category': item.get('category', ''),
                'total_concepts': len(all_concepts),
                'existing_concepts': len(existing_concepts),
                'extracted_concepts': len(extracted_concepts),
                'concept_details': concept_details,
                'analysis_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error analyzing corpus item concepts: {e}")
            return {}
    
    # === DOCUMENTATION MANAGEMENT ===
    
    @staticmethod
    def load_documentation_categories() -> Dict[str, Dict[str, Any]]:
        """Load all documentation categories."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return {}
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            return docs_data.get('categories', {})
        except Exception as e:
            print(f"Error loading documentation categories: {e}")
            return {}
    
    @staticmethod
    def load_documentation_by_category(category: str) -> List[Dict[str, Any]]:
        """Load documentation items by category."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            # Get documents for the specified category
            categories = docs_data.get('categories', {})
            if category not in categories:
                return []
            
            document_ids = categories[category].get('document_ids', [])
            documents = docs_data.get('documents', {})
            
            # Return list of documents for the category
            result = []
            for doc_id in document_ids:
                if doc_id in documents:
                    doc = documents[doc_id].copy()
                    doc['id'] = doc_id  # Ensure ID is included
                    result.append(doc)
            
            return result
        except Exception as e:
            print(f"Error loading documentation by category: {e}")
            return []
    
    @staticmethod
    def load_documentation_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific documentation item by ID with full content."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return None
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            if item_id not in documents:
                return None
            
            item = documents[item_id].copy()
            item['id'] = item_id
            
            # Load full content from file
            filename = item.get('filename', '')
            
            if filename:
                # Look for the file in the docs directory
                content_path = Path(f"docs/{filename}")
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()
                else:
                    # Try backend/docs directory
                    content_path = Path(f"backend/docs/{filename}")
                    if content_path.exists():
                        with open(content_path, 'r', encoding='utf-8') as f:
                            item['content'] = f.read()
                    else:
                        item['content'] = ""
            
            return item
        except Exception as e:
            print(f"Error loading documentation item: {e}")
            return None
    
    @staticmethod
    def search_documentation(query: str) -> List[Dict[str, Any]]:
        """Search documentation by name, description, or tags."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            
            if not query:
                # Return all documents as list
                result = []
                for doc_id, doc_data in documents.items():
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    result.append(doc)
                return result
            
            query_lower = query.lower()
            filtered_documents = []
            
            for doc_id, doc_data in documents.items():
                # Search in name, description, and tags
                searchable_text = " ".join([
                    doc_data.get('name', ''),
                    doc_data.get('description', ''),
                    " ".join(doc_data.get('tags', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    doc = doc_data.copy()
                    doc['id'] = doc_id
                    filtered_documents.append(doc)
            
            return filtered_documents
        except Exception as e:
            print(f"Error searching documentation: {e}")
            return []
    
    @staticmethod
    def load_json_schemas() -> Dict[str, Dict[str, Any]]:
        """Load all JSON schemas."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return {}
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                
            return docs_data.get('schemas', {})
        except Exception as e:
            print(f"Error loading JSON schemas: {e}")
            return {}
    
    @staticmethod
    def get_all_documentation_tags() -> List[str]:
        """Get all available documentation tags."""
        try:
            docs_index_path = Path("data/docs/documentation_index.json")
            if not docs_index_path.exists():
                return []
            
            with open(docs_index_path, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
            
            documents = docs_data.get('documents', {})
            all_tags = set()
            
            for doc_data in documents.values():
                tags = doc_data.get('tags', [])
                all_tags.update(tags)
            
            return sorted(list(all_tags))
        except Exception as e:
            print(f"Error getting documentation tags: {e}")
            return []
    
    # === CORPUS INDEX GENERATION ===
    
    @staticmethod
    def generate_corpus_index(corpus_path: str = "data/research_corpus") -> Dict[str, Any]:
        """Generate corpus index by scanning the corpus directory structure."""
        try:
            corpus_root = Path(corpus_path)
            if not corpus_root.exists():
                raise FileNotFoundError(f"Corpus directory not found: {corpus_path}")
            
            # Initialize index structure
            index_data = {
                "corpus_metadata": {
                    "version": "1.0",
                    "created_date": datetime.now().strftime("%Y-%m-%d"),
                    "total_documents": 0,
                    "research_jurisdiction": "United Kingdom",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "legal_concepts_count": 0,
                    "last_updated": datetime.now().strftime("%Y-%m-%d")
                },
                "documents": {},
                "categories": {
                    "contracts": {
                        "name": "Contract Templates",
                        "description": "Standard UK contract templates",
                        "document_ids": []
                    },
                    "clauses": {
                        "name": "Research Clauses", 
                        "description": "Library of standard research clauses",
                        "document_ids": []
                    },
                    "precedents": {
                        "name": "Case Law and Precedents",
                        "description": "Key UK research precedents and principles", 
                        "document_ids": []
                    },
                    "statutes": {
                        "name": "Statutes and Regulations",
                        "description": "UK legislation and regulations",
                        "document_ids": []
                    }
                },
                "research_areas": set(),
                "document_types": set()
            }
            
            # Scan each category directory
            categories = ["contracts", "clauses", "precedents", "statutes"]
            document_counter = 1
            
            for category in categories:
                category_path = corpus_root / category
                if not category_path.exists():
                    continue
                
                # Scan files in category directory
                for file_path in category_path.glob("*.txt"):
                    doc_id = f"rc-{document_counter:03d}"
                    
                    # Extract metadata from filename and content
                    doc_metadata = DataService._extract_document_metadata(file_path, category, doc_id)
                    
                    # Add to documents
                    index_data["documents"][doc_id] = doc_metadata
                    
                    # Add to category
                    index_data["categories"][category]["document_ids"].append(doc_id)
                    
                    # Collect research areas and document types
                    index_data["research_areas"].update(doc_metadata.get("research_areas", []))
                    if doc_metadata.get("document_type"):
                        index_data["document_types"].add(doc_metadata["document_type"])
                    
                    document_counter += 1
            
            # Convert sets to sorted lists
            index_data["research_areas"] = sorted(list(index_data["research_areas"]))
            index_data["document_types"] = sorted(list(index_data["document_types"]))
            
            # Update metadata
            index_data["corpus_metadata"]["total_documents"] = len(index_data["documents"])
            
            # Generate legal concepts and relationships
            DataService._generate_legal_concepts(index_data)
            
            return index_data
            
        except Exception as e:
            print(f"Error generating corpus index: {e}")
            return {}
    
    @staticmethod
    def _extract_document_metadata(file_path: Path, category: str, doc_id: str) -> Dict[str, Any]:
        """Extract metadata from a document file."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from filename
            filename = file_path.name
            title = DataService._filename_to_title(filename)
            
            # Determine document type based on category
            document_type_map = {
                "contracts": "Contract Template",
                "clauses": "Research Clause", 
                "precedents": "Case Law",
                "statutes": "Statute/Regulation"
            }
            document_type = document_type_map.get(category, "Legal Document")
            
            # Extract research areas from content and filename
            research_areas = DataService._extract_research_areas(content, filename)
            
            # Generate description
            description = DataService._generate_description(content, title, category)
            
            # Extract legal concepts (placeholder - would use AI in production)
            legal_concepts = DataService._extract_legal_concepts_from_content(content, category)
            
            return {
                "id": doc_id,
                "title": title,
                "filename": filename,
                "category": category,
                "document_type": document_type,
                "research_areas": research_areas,
                "description": description,
                "legal_concepts": legal_concepts,
                "related_items": [],  # Will be populated after all documents are processed
                "metadata": {
                    "jurisdiction": "United Kingdom",
                    "document_type": document_type,
                    "research_areas": research_areas
                }
            }
            
        except Exception as e:
            print(f"Error extracting metadata from {file_path}: {e}")
            return {}
    
    @staticmethod
    def _filename_to_title(filename: str) -> str:
        """Convert filename to human-readable title."""
        # Remove file extension and ID prefix
        name = filename.replace('.txt', '')
        
        # Remove rc-XXX_ prefix if present
        if name.startswith('rc-') and '_' in name:
            name = name.split('_', 1)[1]
        
        # Replace underscores with spaces and title case
        title = name.replace('_', ' ').title()
        
        return title
    
    @staticmethod
    def _extract_research_areas(content: str, filename: str) -> List[str]:
        """Extract research areas from content and filename."""
        research_areas = []
        
        # Common research area keywords
        area_keywords = {
            "Employment Law": ["employment", "employee", "employer", "dismissal", "termination", "workplace"],
            "Contract Law": ["contract", "agreement", "breach", "consideration", "offer", "acceptance"],
            "Intellectual Property": ["intellectual", "property", "copyright", "patent", "trademark", "confidential"],
            "Data Protection": ["data", "protection", "privacy", "gdpr", "personal", "information"],
            "Commercial Law": ["commercial", "business", "trade", "service", "liability", "indemnity"],
            "Liability and Risk": ["liability", "risk", "damages", "negligence", "indemnification"]
        }
        
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        for area, keywords in area_keywords.items():
            if any(keyword in content_lower or keyword in filename_lower for keyword in keywords):
                research_areas.append(area)
        
        return research_areas if research_areas else ["General Legal"]
    
    @staticmethod
    def _generate_description(content: str, title: str, category: str) -> str:
        """Generate a description for the document."""
        # Extract first meaningful sentence or paragraph
        lines = content.split('\n')
        
        # Look for a description in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 50 and not line.isupper():  # Skip headers
                return line[:200] + "..." if len(line) > 200 else line
        
        # Fallback to generic description
        category_descriptions = {
            "contracts": f"{title} for UK legal practice",
            "clauses": f"{title} templates and examples",
            "precedents": f"Key UK {title.lower()} and principles", 
            "statutes": f"UK {title.lower()} and regulations"
        }
        
        return category_descriptions.get(category, f"UK legal document: {title}")
    
    @staticmethod
    def _extract_legal_concepts_from_content(content: str, category: str) -> List[str]:
        """Extract legal concept IDs from document content."""
        # This is a simplified version - in production would use AI/NLP
        concept_mapping = {
            "employment": ["lc-001", "lc-002", "lc-003"],
            "contract": ["lc-004", "lc-005", "lc-006"],
            "intellectual": ["lc-011", "lc-012", "lc-013"],
            "liability": ["lc-004", "lc-005"],
            "termination": ["lc-001", "lc-002", "lc-003"],
            "confidential": ["lc-011", "lc-012"],
            "statute": ["lc-014", "lc-015"],
            "precedent": ["lc-006", "lc-007", "lc-008", "lc-009", "lc-010"]
        }
        
        content_lower = content.lower()
        legal_concepts = []
        
        for keyword, concepts in concept_mapping.items():
            if keyword in content_lower:
                legal_concepts.extend(concepts)
        
        return list(set(legal_concepts))  # Remove duplicates
    
    @staticmethod
    def _generate_legal_concepts(index_data: Dict[str, Any]) -> None:
        """Generate legal concepts metadata and update concept count."""
        # Count unique legal concepts
        all_concepts = set()
        for doc_data in index_data["documents"].values():
            all_concepts.update(doc_data.get("legal_concepts", []))
        
        index_data["corpus_metadata"]["legal_concepts_count"] = len(all_concepts)
    
    @staticmethod
    def save_corpus_index(index_data: Dict[str, Any], output_path: str = "data/ai/research_corpus/research_corpus_index.json") -> bool:
        """Save the generated corpus index to file."""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            print(f"Corpus index saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving corpus index: {e}")
            return False
    
    @staticmethod
    def regenerate_corpus_index(corpus_path: str = "data/research_corpus") -> bool:
        """Regenerate and save the corpus index."""
        try:
            print("Generating corpus index...")
            index_data = DataService.generate_corpus_index(corpus_path)
            
            if not index_data:
                print("Failed to generate corpus index")
                return False
            
            # Save the index to AI directory
            index_path = "data/ai/research_corpus/research_corpus_index.json"
            success = DataService.save_corpus_index(index_data, index_path)
            
            if success:
                print(f"Successfully regenerated corpus index with {index_data['corpus_metadata']['total_documents']} documents")
                print(f"Research areas: {', '.join(index_data['research_areas'])}")
                print(f"Legal concepts: {index_data['corpus_metadata']['legal_concepts_count']}")
            
            return success
            
        except Exception as e:
            print(f"Error regenerating corpus index: {e}")
            return False
    # === DOCUMENT ANALYSIS REGENERATION ===
    
    @staticmethod
    def regenerate_document_analysis() -> bool:
        """Regenerate AI analysis for all documents in the system."""
        try:
            from app.services.ai_service import AIService
            
            # Statistics tracking
            stats = {
                "total_documents": 0,
                "analyzed_documents": 0,
                "failed_documents": 0,
                "confidence_scores": []
            }
            
            # Load all cases
            cases = DataService.load_cases()
            
            for case in cases:
                case_id = case.get('id') if isinstance(case, dict) else case.id
                documents = DataService.load_case_documents(case_id)
                
                for document in documents:
                    doc_id = document.get('id') if isinstance(document, dict) else document.id
                    stats["total_documents"] += 1
                    
                    try:
                        # Load document content
                        content = DataService.load_document_content(doc_id)
                        if not content:
                            stats["failed_documents"] += 1
                            continue
                        
                        # Perform AI analysis
                        analysis = AIService.analyze_document(doc_id, content)
                        
                        # Save analysis results
                        AIService.save_analysis(doc_id, analysis)
                        
                        stats["analyzed_documents"] += 1
                        stats["confidence_scores"].append(analysis.get("overall_confidence", 0.0))
                        
                    except Exception as e:
                        print(f"Failed to analyze document {doc_id}: {e}")
                        stats["failed_documents"] += 1
            
            # Calculate average confidence
            if stats["confidence_scores"]:
                stats["average_confidence"] = sum(stats["confidence_scores"]) / len(stats["confidence_scores"])
            else:
                stats["average_confidence"] = 0.0
            
            # Save statistics
            DataService._save_document_analysis_stats(stats)
            
            return True
            
        except Exception as e:
            print(f"Error regenerating document analysis: {e}")
            return False
    
    @staticmethod
    def get_document_analysis_stats() -> Dict[str, Any]:
        """Get statistics from the last document analysis regeneration."""
        try:
            stats_path = Path("data/ai/case_documents/analysis_stats.json")
            if not stats_path.exists():
                return {
                    "total_documents": 0,
                    "analyzed_documents": 0,
                    "failed_documents": 0,
                    "average_confidence": 0.0
                }
            
            with open(stats_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading document analysis stats: {e}")
            return {
                "total_documents": 0,
                "analyzed_documents": 0,
                "failed_documents": 0,
                "average_confidence": 0.0
            }
    
    @staticmethod
    def _save_document_analysis_stats(stats: Dict[str, Any]) -> None:
        """Save document analysis statistics."""
        try:
            stats_path = Path("data/ai/case_documents/analysis_stats.json")
            stats_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Clean up stats for JSON serialization
            clean_stats = {
                "total_documents": stats["total_documents"],
                "analyzed_documents": stats["analyzed_documents"],
                "failed_documents": stats["failed_documents"],
                "average_confidence": round(stats["average_confidence"], 3),
                "last_regenerated": datetime.now().isoformat()
            }
            
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(clean_stats, f, indent=2)
                
        except Exception as e:
            print(f"Error saving document analysis stats: {e}")
    
    @staticmethod
    def _has_document_analysis(doc_id: str) -> bool:
        """Check if analysis exists for a document."""
        try:
            analysis_path = Path("data/ai/case_documents/case_documents_analysis.json")
            if not analysis_path.exists():
                return False
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                analyses = json.load(f)
                return doc_id in analyses
                
        except Exception as e:
            print(f"Error checking document analysis: {e}")
            return False
    
    @staticmethod
    def load_document_analysis(doc_id: str) -> Dict[str, Any]:
        """Load AI analysis for a specific document."""
        try:
            analysis_path = Path("data/ai/case_documents/case_documents_analysis.json")
            if not analysis_path.exists():
                return None
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                analyses = json.load(f)
                return analyses.get(doc_id)
                
        except Exception as e:
            print(f"Error loading document analysis: {e}")
            return None
    
    @staticmethod
    def load_document_summary(doc_id: str) -> Dict[str, Any]:
        """Load AI-generated summary for a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "summary": analysis.get("summary", ""),
                "key_points": analysis.get("key_points", []),
                "confidence_score": analysis.get("overall_confidence", 0.0)
            }
        except Exception as e:
            print(f"Error loading document summary: {e}")
            return None
    
    @staticmethod
    def load_document_key_dates(doc_id: str) -> Dict[str, Any]:
        """Load key dates extracted from a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "key_dates": analysis.get("key_dates", []),
                "confidence_score": analysis.get("confidence_scores", {}).get("key_dates", 0.0)
            }
        except Exception as e:
            print(f"Error loading document key dates: {e}")
            return None
    
    @staticmethod
    def load_document_parties(doc_id: str) -> Dict[str, Any]:
        """Load parties extracted from a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "parties": analysis.get("parties_involved", []),
                "confidence_score": analysis.get("confidence_scores", {}).get("parties", 0.0)
            }
        except Exception as e:
            print(f"Error loading document parties: {e}")
            return None
    
    @staticmethod
    def load_document_risks(doc_id: str) -> Dict[str, Any]:
        """Load risk assessment for a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "risks": analysis.get("potential_issues", []),
                "risk_level": analysis.get("risk_level", "unknown"),
                "confidence_score": analysis.get("confidence_scores", {}).get("risks", 0.0)
            }
        except Exception as e:
            print(f"Error loading document risks: {e}")
            return None
    
    @staticmethod
    def load_document_compliance(doc_id: str) -> Dict[str, Any]:
        """Load compliance status for a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "compliance_status": analysis.get("compliance_status", "unknown"),
                "compliance_issues": analysis.get("compliance_issues", []),
                "confidence_score": analysis.get("confidence_scores", {}).get("compliance", 0.0)
            }
        except Exception as e:
            print(f"Error loading document compliance: {e}")
            return None
    
    @staticmethod
    def load_document_deadlines(doc_id: str) -> Dict[str, Any]:
        """Load deadlines extracted from a specific document."""
        try:
            analysis = DataService.load_document_analysis(doc_id)
            if not analysis:
                return None
            
            return {
                "document_id": doc_id,
                "deadlines": analysis.get("critical_deadlines", []),
                "confidence_score": analysis.get("confidence_scores", {}).get("deadlines", 0.0)
            }
        except Exception as e:
            print(f"Error loading document deadlines: {e}")
            return None