#!/usr/bin/env python3
"""
Script to run AI document analysis on all documents in the system.
This will analyze documents and generate real AI-powered insights.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.document_service import DocumentService
from app.services.ai_analysis_service import AIAnalysisService


def run_document_analysis():
    """Run AI analysis on all documents"""
    print("Starting AI Document Analysis")
    print("=" * 50)
    
    try:
        # Initialize services
        document_service = DocumentService()
        ai_service = AIAnalysisService()
        
        # Load all documents
        documents = document_service._load_documents()
        print(f"Found {len(documents)} documents to analyze")
        
        if len(documents) == 0:
            print("No documents found to analyze")
            return 0
        
        # Check if AI service is implemented
        if not hasattr(ai_service, 'analyze_document') or ai_service.analyze_document.__code__.co_code == b'd\x00S\x00':
            print("❌ AI Analysis Service not implemented yet")
            print("This would require:")
            print("  - OpenAI API integration")
            print("  - Document text extraction")
            print("  - AI prompt engineering")
            print("  - Analysis result processing")
            return 1
        
        # If implemented, run analysis
        analyses = []
        for i, document in enumerate(documents):
            print(f"Analyzing document {i+1}/{len(documents)}: {document.name}")
            
            try:
                analysis = ai_service.analyze_document(document)
                analyses.append(analysis)
                print(f"  ✅ Analysis complete")
            except Exception as e:
                print(f"  ❌ Analysis failed: {str(e)}")
        
        # Save results
        if analyses:
            output_file = Path("app/data/ai_document_analysis.json")
            analysis_data = {
                "generated_at": datetime.now().isoformat(),
                "total_documents": len(documents),
                "successful_analyses": len(analyses),
                "document_analyses": [analysis.dict() for analysis in analyses]
            }
            
            with open(output_file, 'w') as f:
                json.dump(analysis_data, f, indent=2)
            
            print(f"\n✅ Analysis complete!")
            print(f"📁 Results saved to: {output_file}")
            print(f"📊 Successfully analyzed {len(analyses)}/{len(documents)} documents")
        
        return len(analyses)
        
    except Exception as e:
        print(f"❌ Error during document analysis: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    result = run_document_analysis()
    if result > 0:
        print(f"\n🎉 Document analysis completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💡 Document analysis not available yet - implement AI service first")
        sys.exit(1)