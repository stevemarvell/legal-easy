#!/usr/bin/env python3
"""
Script to initialize the legal document corpus and generate vector embeddings.
Run this script to set up the RAG system for legal research.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.legal_corpus_service import LegalCorpusService


def main():
    """Initialize the legal corpus and generate embeddings"""
    print("Initializing Legal Document Corpus for RAG System")
    print("=" * 50)
    
    try:
        # Initialize the corpus service
        corpus_service = LegalCorpusService()
        
        # Check if corpus directory exists
        if not corpus_service.corpus_path.exists():
            print(f"Error: Legal corpus directory not found at {corpus_service.corpus_path}")
            print("Please ensure the legal corpus files are in place.")
            return 1
        
        # Initialize the corpus
        document_count = corpus_service.initialize_corpus()
        
        print("\n" + "=" * 50)
        print(f"✅ Successfully initialized legal corpus with {document_count} document chunks")
        print(f"📁 Corpus data saved to: {corpus_service.embeddings_path}")
        print("\nThe RAG system is now ready for legal research queries!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error initializing legal corpus: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)