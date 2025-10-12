#!/usr/bin/env python3
"""
AI Analysis Service - AI-powered case analysis service for the Legal AI System

This service handles AI analysis operations including:
- Case document analysis using Claude API
- Analysis result storage and retrieval
- Conversation logging for audit trails
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import logging

from .claude_client import ClaudeClient
from .document_extractor import DocumentExtractor


logger = logging.getLogger(__name__)


class AIAnalysisService:
    """Service for AI-powered case analysis operations."""
    
    def __init__(self):
        """Initialize the AI Analysis Service."""
        self.claude_client = ClaudeClient()
        self.document_extractor = DocumentExtractor()
        self.backend_dir = Path(__file__).parent.parent.parent
        self.ai_data_dir = self.backend_dir / "data" / "ai" / "cases"
    
    def analyze_case(self, case_id: str) -> Dict[str, Any]:
        """
        Perform AI analysis on a case and its documents.
        
        Args:
            case_id: The ID of the case to analyze
            
        Returns:
            Dict containing the analysis results
            
        Raises:
            ValueError: If case not found or no documents available
            Exception: If analysis fails
        """
        try:
            logger.info(f"Starting AI analysis for case {case_id}")
            
            # Load case data
            case_data = self._load_case_data(case_id)
            if not case_data:
                raise ValueError(f"Case {case_id} not found")
            
            # Extract text from all case documents
            document_texts = self._extract_case_documents(case_id, case_data.get('documents', []))
            if not document_texts:
                raise ValueError(f"No documents found for case {case_id}")
            
            # Prepare analysis prompt
            analysis_prompt = self._create_analysis_prompt(case_data, document_texts)
            
            # Send to Claude API for analysis
            logger.info(f"Sending analysis request to Claude API for case {case_id}")
            analysis_response = self.claude_client.analyze_case(analysis_prompt)
            
            # Parse and validate response
            analysis_result = self._parse_analysis_response(case_id, analysis_response)
            
            # Store analysis results
            self._store_analysis_result(case_id, analysis_result)
            
            # Log conversation
            self._log_conversation(case_id, analysis_prompt, analysis_response, "case_analysis")
            
            logger.info(f"AI analysis completed successfully for case {case_id}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing case {case_id}: {str(e)}")
            # Log failed conversation
            self._log_conversation(case_id, analysis_prompt if 'analysis_prompt' in locals() else "", 
                                 f"Error: {str(e)}", "case_analysis", success=False)
            raise
    
    def get_case_analysis(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve existing analysis data for a case.
        
        Args:
            case_id: The ID of the case
            
        Returns:
            Dict containing analysis data or None if not found
        """
        try:
            analysis_file = self.ai_data_dir / case_id / "case_analysis.json"
            
            if not analysis_file.exists():
                return None
            
            with open(analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error retrieving analysis for case {case_id}: {str(e)}")
            return None
    
    def get_conversation_log(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve conversation log for a case.
        
        Args:
            case_id: The ID of the case
            
        Returns:
            List of conversation objects
        """
        try:
            conversations_file = self.ai_data_dir / case_id / "conversations.json"
            
            if not conversations_file.exists():
                return []
            
            with open(conversations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('conversations', [])
                
        except Exception as e:
            logger.error(f"Error retrieving conversation log for case {case_id}: {str(e)}")
            return []
    
    def _load_case_data(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Load case data from the cases index."""
        try:
            cases_index_path = self.backend_dir / "data" / "cases" / "cases_index.json"
            
            if not cases_index_path.exists():
                return None
            
            with open(cases_index_path, 'r', encoding='utf-8') as f:
                cases_data = json.load(f)
                
                # Handle both array format and object with 'cases' key
                cases = cases_data if isinstance(cases_data, list) else cases_data.get('cases', [])
                
                return next((c for c in cases if c.get('id') == case_id), None)
                
        except Exception as e:
            logger.error(f"Error loading case data for {case_id}: {str(e)}")
            return None
    
    def _extract_case_documents(self, case_id: str, document_ids: List[str]) -> List[Dict[str, str]]:
        """Extract text from all case documents."""
        document_texts = []
        
        for doc_id in document_ids:
            try:
                text_content = self.document_extractor.extract_text(case_id, doc_id)
                if text_content:
                    document_texts.append({
                        'document_id': doc_id,
                        'content': text_content
                    })
            except Exception as e:
                logger.warning(f"Failed to extract text from document {doc_id}: {str(e)}")
                continue
        
        return document_texts
    
    def _create_analysis_prompt(self, case_data: Dict[str, Any], document_texts: List[Dict[str, str]]) -> str:
        """Create structured prompt for Claude API analysis."""
        
        # Combine all document texts
        combined_text = "\n\n".join([
            f"Document {doc['document_id']}:\n{doc['content']}" 
            for doc in document_texts
        ])
        
        prompt = f"""
Please analyze the following legal case and extract structured information. 

Case Information:
- Case ID: {case_data.get('id')}
- Title: {case_data.get('title')}
- Case Type: {case_data.get('case_type')}
- Client: {case_data.get('client_name')}
- Summary: {case_data.get('summary')}

Documents to analyze:
{combined_text}

Please provide a JSON response with the following structure:
{{
    "caseId": "{case_data.get('id')}",
    "timestamp": "{datetime.now(timezone.utc).isoformat()}",
    "claimReference": "extracted claim reference number if found",
    "claimantName": "name of the claimant",
    "incidentDate": "date of incident in YYYY-MM-DD format if found",
    "claimAmount": "monetary amount claimed as number if found",
    "injuryStatus": "description of injury or damages",
    "thirdPartyInvolvement": true/false,
    "keyFacts": ["list", "of", "key", "facts", "extracted"],
    "timelineEvents": [
        {{
            "date": "YYYY-MM-DD",
            "description": "event description",
            "importance": "high/medium/low"
        }}
    ],
    "playbookRelevance": [
        {{
            "playbookId": "{case_data.get('playbook_id')}",
            "relevantCriteria": ["criteria", "that", "apply"],
            "suggestedActions": ["suggested", "actions"],
            "conflictFlags": ["any", "conflicts", "identified"]
        }}
    ],
    "confidence": 0.85
}}

Focus on extracting factual information from the documents. If information is not available, use null for optional fields.
"""
        
        return prompt
    
    def _parse_analysis_response(self, case_id: str, response: str) -> Dict[str, Any]:
        """Parse and validate the Claude API response."""
        try:
            # Parse JSON response
            analysis_data = json.loads(response)
            
            # Add metadata
            analysis_data['caseId'] = case_id
            analysis_data['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Validate required fields
            required_fields = ['caseId', 'timestamp', 'keyFacts']
            for field in required_fields:
                if field not in analysis_data:
                    analysis_data[field] = [] if field == 'keyFacts' else None
            
            return analysis_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude API response as JSON: {str(e)}")
            # Return a basic structure with error information
            return {
                'caseId': case_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'error': 'Failed to parse AI response',
                'rawResponse': response,
                'keyFacts': [],
                'confidence': 0.0
            }
    
    def _store_analysis_result(self, case_id: str, analysis_result: Dict[str, Any]) -> None:
        """Store analysis results to file system."""
        try:
            # Create directory if it doesn't exist
            case_dir = self.ai_data_dir / case_id
            case_dir.mkdir(parents=True, exist_ok=True)
            
            # Store analysis result
            analysis_file = case_dir / "case_analysis.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Analysis result stored for case {case_id}")
            
        except Exception as e:
            logger.error(f"Error storing analysis result for case {case_id}: {str(e)}")
            raise
    
    def _log_conversation(self, case_id: str, prompt: str, response: str, 
                         analysis_type: str, success: bool = True) -> None:
        """Log AI conversation for audit trail."""
        try:
            # Create directory if it doesn't exist
            case_dir = self.ai_data_dir / case_id
            case_dir.mkdir(parents=True, exist_ok=True)
            
            # Load existing conversations
            conversations_file = case_dir / "conversations.json"
            conversations_data = {'conversations': []}
            
            if conversations_file.exists():
                with open(conversations_file, 'r', encoding='utf-8') as f:
                    conversations_data = json.load(f)
            
            # Add new conversation
            conversation = {
                'id': f"{case_id}_{len(conversations_data['conversations']) + 1}",
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'analysis_type': analysis_type,
                'prompt': prompt,
                'response': response,
                'metadata': {
                    'apiVersion': 'claude-3',
                    'processingTime': 0  # Will be updated by Claude client
                }
            }
            
            conversations_data['conversations'].append(conversation)
            
            # Store updated conversations
            with open(conversations_file, 'w', encoding='utf-8') as f:
                json.dump(conversations_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Conversation logged for case {case_id}")
            
        except Exception as e:
            logger.error(f"Error logging conversation for case {case_id}: {str(e)}")
            # Don't raise here as this is logging functionality