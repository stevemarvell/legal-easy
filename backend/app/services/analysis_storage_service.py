import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from app.models.document import DocumentAnalysis


class AnalysisStorageService:
    """Service for storing and retrieving document analysis results"""
    
    def __init__(self):
        self.storage_dir = Path("app/data/al/case_documents")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.storage_file = self.storage_dir / "documents_analysis.json"
        self._ensure_storage_file()
    
    def _ensure_storage_file(self):
        """Ensure the storage file exists with proper structure"""
        if not self.storage_file.exists():
            initial_data = {
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_analyses": 0
                },
                "analyses": {}
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, default=str)
    
    def save_analysis(self, document_id: str, analysis: DocumentAnalysis) -> bool:
        """
        Save analysis results for a document
        
        Args:
            document_id: ID of the document
            analysis: DocumentAnalysis object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Load existing data
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert analysis to dict for JSON storage
            analysis_dict = {
                "document_id": analysis.document_id,
                "key_dates": [str(date) for date in analysis.key_dates],
                "parties_involved": analysis.parties_involved,
                "document_type": analysis.document_type,
                "summary": analysis.summary,
                "key_clauses": analysis.key_clauses,
                "confidence_scores": analysis.confidence_scores,
                "analyzed_at": datetime.now().isoformat(),
                "analysis_source": "live_ai_analysis"
            }
            
            # Update data
            data["analyses"][document_id] = analysis_dict
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            data["metadata"]["total_analyses"] = len(data["analyses"])
            
            # Save back to file
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"Failed to save analysis for document {document_id}: {str(e)}")
            return False
    
    def get_analysis(self, document_id: str) -> Optional[DocumentAnalysis]:
        """
        Retrieve analysis results for a document
        
        Args:
            document_id: ID of the document
            
        Returns:
            DocumentAnalysis object if found, None otherwise
        """
        try:
            if not self.storage_file.exists():
                return None
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if document_id not in data.get("analyses", {}):
                return None
            
            analysis_dict = data["analyses"][document_id]
            
            # Convert back to DocumentAnalysis object
            from datetime import date
            analysis = DocumentAnalysis(
                document_id=analysis_dict["document_id"],
                key_dates=[date.fromisoformat(d) for d in analysis_dict["key_dates"]],
                parties_involved=analysis_dict["parties_involved"],
                document_type=analysis_dict["document_type"],
                summary=analysis_dict["summary"],
                key_clauses=analysis_dict["key_clauses"],
                confidence_scores=analysis_dict["confidence_scores"]
            )
            
            return analysis
            
        except Exception as e:
            print(f"Failed to retrieve analysis for document {document_id}: {str(e)}")
            return None
    
    def has_analysis(self, document_id: str) -> bool:
        """Check if analysis exists for a document"""
        try:
            if not self.storage_file.exists():
                return False
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return document_id in data.get("analyses", {})
            
        except Exception:
            return False
    
    def get_all_analyses(self) -> Dict[str, DocumentAnalysis]:
        """Get all stored analyses"""
        try:
            if not self.storage_file.exists():
                return {}
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analyses = {}
            for doc_id, analysis_dict in data.get("analyses", {}).items():
                try:
                    from datetime import date
                    analysis = DocumentAnalysis(
                        document_id=analysis_dict["document_id"],
                        key_dates=[date.fromisoformat(d) for d in analysis_dict["key_dates"]],
                        parties_involved=analysis_dict["parties_involved"],
                        document_type=analysis_dict["document_type"],
                        summary=analysis_dict["summary"],
                        key_clauses=analysis_dict["key_clauses"],
                        confidence_scores=analysis_dict["confidence_scores"]
                    )
                    analyses[doc_id] = analysis
                except Exception as e:
                    print(f"Failed to parse analysis for document {doc_id}: {str(e)}")
                    continue
            
            return analyses
            
        except Exception as e:
            print(f"Failed to retrieve all analyses: {str(e)}")
            return {}
    
    def delete_analysis(self, document_id: str) -> bool:
        """Delete analysis for a document"""
        try:
            if not self.storage_file.exists():
                return False
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if document_id in data.get("analyses", {}):
                del data["analyses"][document_id]
                data["metadata"]["last_updated"] = datetime.now().isoformat()
                data["metadata"]["total_analyses"] = len(data["analyses"])
                
                with open(self.storage_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Failed to delete analysis for document {document_id}: {str(e)}")
            return False
    
    def clear_all_analyses(self) -> bool:
        """Clear all stored analyses"""
        try:
            data = {
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_analyses": 0
                },
                "analyses": {}
            }
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"Failed to clear all analyses: {str(e)}")
            return False
    
    def get_storage_stats(self) -> Dict:
        """Get statistics about stored analyses"""
        try:
            if not self.storage_file.exists():
                return {"total_analyses": 0, "storage_available": False}
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "total_analyses": len(data.get("analyses", {})),
                "storage_available": True,
                "last_updated": data.get("metadata", {}).get("last_updated"),
                "storage_file_size": os.path.getsize(self.storage_file)
            }
            
        except Exception as e:
            return {"total_analyses": 0, "storage_available": False, "error": str(e)}