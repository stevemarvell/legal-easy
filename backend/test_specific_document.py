#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.document_service import DocumentService
from app.services.ai_analysis_service import AIAnalysisService
import json

# Test specific documents
doc_service = DocumentService()
ai_service = AIAnalysisService()

documents = doc_service._load_documents()

print('=== TESTING SPECIFIC DOCUMENTS ===')

# Test the first few documents that users are likely to click on
test_docs = ['doc-001', 'doc-002', 'doc-003', 'doc-004', 'doc-005']

for doc_id in test_docs:
    doc = doc_service.get_document_by_id(doc_id)
    if doc:
        analysis = ai_service.analyze_document(doc)
        print(f'\n{doc_id}: {doc.name}')
        print('Confidence Scores:')
        for category, score in analysis.confidence_scores.items():
            print(f'  {category}: {score:.3f} ({score:.1%})')
        
        # Test JSON serialization
        analysis_dict = analysis.model_dump()
        print('JSON serialized scores:')
        for category, score in analysis_dict['confidence_scores'].items():
            print(f'  {category}: {score:.3f} ({score:.1%})')