#!/usr/bin/env python3
"""
Script to initialize the legal document corpus using simple vector embeddings.
This is a fallback when sentence-transformers is not available.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.simple_vector_service import SimpleVectorService


def main():
    """Initialize the legal corpus with simple vector embeddings"""
    print("Initializing Legal Document Corpus with Simple Vector Embeddings")
    print("=" * 60)
    
    try:
        # Initialize the vector service
        vector_service = SimpleVectorService()
        
        # Check if corpus directory exists
        if not vector_service.corpus_path.exists():
            print(f"Error: Legal corpus directory not found at {vector_service.corpus_path}")
            print("Please ensure the legal corpus files are in place.")
            return 1
        
        # Initialize the vector database
        document_count = vector_service.initialize_vector_database()
        
        print("\n" + "=" * 60)
        print(f"✅ Successfully initialized vector database with {document_count} document chunks")
        print(f"📁 Embeddings saved to: {vector_service.embeddings_path}")
        print("\nThe simple RAG system is now ready for legal research queries!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error initializing vector database: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)