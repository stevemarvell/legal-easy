#!/usr/bin/env python3
from app.services.ai_service import AIService
import json

# Test loading analysis directly
print("Testing AIService.load_existing_analysis...")

try:
    analysis = AIService.load_existing_analysis("doc-001")
    if analysis:
        print("Analysis found!")
        print(f"Document ID: {analysis.get('document_id')}")
        print(f"Key dates: {analysis.get('key_dates')}")
        print(f"Overall confidence: {analysis.get('overall_confidence')}")
    else:
        print("No analysis found")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Check if file exists
from pathlib import Path
analysis_path = Path("data/ai/case_documents/case_documents_analysis.json")
print(f"\nAnalysis file exists: {analysis_path.exists()}")
print(f"Analysis file path: {analysis_path.absolute()}")

if analysis_path.exists():
    with open(analysis_path, 'r') as f:
        data = json.load(f)
    print(f"File contains {len(data)} documents")
    if "doc-001" in data:
        print("doc-001 analysis exists in file")
        print(f"Key dates in file: {data['doc-001'].get('key_dates')}")
    else:
        print("doc-001 not found in analysis file")