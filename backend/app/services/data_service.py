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
                    # Convert relative path to absolute from data root
                    full_path = Path("data") / content_path.replace('data/', '')
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
            concepts_path = Path("data/research_corpus/concepts/research_concepts.json")
            
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            corpus_index_path = Path("data/research_corpus/research_corpus_index.json")
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
            concepts_path = Path("data/research_corpus/concepts/research_concepts.json")
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
            concepts_path = Path("data/research_corpus/concepts/research_concepts.json")
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
            concepts_path = Path("data/research_corpus/concepts/research_concepts.json")
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