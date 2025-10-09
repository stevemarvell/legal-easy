from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime
import os
from pathlib import Path
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService

router = APIRouter(prefix="/admin", tags=["admin"])

class SystemStatus:
    """System status checker for admin interface"""
    
    def __init__(self):
        self.document_service = DocumentService()
        self.rag_service = RAGService()
    
    def check_backend_health(self) -> Dict[str, Any]:
        """Check backend API health"""
        try:
            # Basic API health
            return {
                "status": "green",
                "message": "Backend API is running",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "api_version": "1.0.0",
                    "python_version": "3.x",
                    "fastapi_status": "operational"
                }
            }
        except Exception as e:
            return {
                "status": "red",
                "message": f"Backend health check failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "details": {"error": str(e)}
            }
    
    def check_document_service(self) -> Dict[str, Any]:
        """Check document service status"""
        try:
            # Test document loading
            documents = self.document_service._load_documents()
            
            # Check if AI analysis is working by testing the service
            try:
                from app.services.ai_analysis_service import AIAnalysisService
                from app.services.analysis_storage_service import AnalysisStorageService
                
                ai_service = AIAnalysisService()
                storage_service = AnalysisStorageService()
                
                # Get live analysis statistics
                storage_stats = storage_service.get_storage_stats()
                live_analyses_count = storage_stats.get("total_analyses", 0)
                
                analysis_status = f"AI analysis operational ({live_analyses_count} live analyses stored)"
                status_color = "green"
            except Exception as e:
                analysis_status = f"AI analysis service error: {str(e)}"
                status_color = "amber"
                live_analyses_count = 0
            
            return {
                "status": status_color,
                "message": f"Document service operational - {len(documents)} documents",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "documents_count": len(documents),
                    "live_analyses_count": live_analyses_count if 'live_analyses_count' in locals() else 0,
                    "documents_file_exists": os.path.exists(self.document_service._documents_file),
                    "ai_analysis_implemented": True,
                    "ai_analysis_status": analysis_status,
                    "analysis_endpoint": "/api/documents/{id}/analyze",
                    "analysis_interface": "/analysis",
                    "storage_stats": storage_stats if 'storage_stats' in locals() else {}
                }
            }
        except Exception as e:
            return {
                "status": "red",
                "message": f"Document service error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "details": {"error": str(e)}
            }
    
    def check_rag_service(self) -> Dict[str, Any]:
        """Check RAG service status"""
        try:
            # Test RAG search functionality
            test_results = self.rag_service.search_legal_corpus("test query", top_k=1)
            corpus_stats = self.rag_service.get_corpus_statistics()
            
            if len(test_results) > 0:
                status = "green"
                message = "RAG service operational"
            else:
                status = "amber"
                message = "RAG service running but no search results"
            
            return {
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "test_results_count": len(test_results),
                    "corpus_total_documents": corpus_stats.get("total_documents", 0),
                    "corpus_categories": corpus_stats.get("categories", {}),
                    "search_functional": len(test_results) > 0
                }
            }
        except Exception as e:
            return {
                "status": "red",
                "message": f"RAG service error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "details": {"error": str(e)}
            }
    
    def check_legal_corpus(self) -> Dict[str, Any]:
        """Check legal corpus status"""
        try:
            corpus_path = Path("app/data/legal_corpus")
            demo_corpus_path = Path("app/data/demo_legal_corpus.json")
            embeddings_path = Path("app/data/embeddings")
            
            corpus_exists = corpus_path.exists()
            demo_corpus_exists = demo_corpus_path.exists()
            embeddings_exist = embeddings_path.exists()
            
            # Count documents in corpus
            doc_count = 0
            if corpus_exists:
                for category_dir in corpus_path.iterdir():
                    if category_dir.is_dir():
                        doc_count += len(list(category_dir.glob("*.txt")))
            
            # Check demo corpus
            demo_doc_count = 0
            if demo_corpus_exists:
                import json
                with open(demo_corpus_path, 'r') as f:
                    demo_corpus = json.load(f)
                    demo_doc_count = len(demo_corpus)
            
            # Determine status
            if doc_count > 50:
                status = "green"
                message = f"Full legal corpus available - {doc_count} documents"
            elif demo_doc_count > 0:
                status = "amber"
                message = f"Using demo corpus - {demo_doc_count} documents"
            else:
                status = "red"
                message = "No legal corpus available"
            
            return {
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "full_corpus_exists": corpus_exists,
                    "full_corpus_doc_count": doc_count,
                    "demo_corpus_exists": demo_corpus_exists,
                    "demo_corpus_doc_count": demo_doc_count,
                    "embeddings_exist": embeddings_exist,
                    "corpus_path": str(corpus_path),
                    "embeddings_path": str(embeddings_path)
                }
            }
        except Exception as e:
            return {
                "status": "red",
                "message": f"Legal corpus check failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "details": {"error": str(e)}
            }
    
    def check_case_assessment(self) -> Dict[str, Any]:
        """Check case assessment functionality"""
        try:
            # This will be implemented in Phase 1
            return {
                "status": "red",
                "message": "Case assessment not implemented",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "implementation_status": "pending",
                    "phase": "Phase 1 - Not Started"
                }
            }
        except Exception as e:
            return {
                "status": "red",
                "message": f"Case assessment check failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "details": {"error": str(e)}
            }
    
    def get_demo_data_summary(self) -> Dict[str, Any]:
        """Get comprehensive demo data summary"""
        try:
            import json
            from pathlib import Path
            
            summary = {
                "cases": {},
                "documents": {},
                "document_analyses": {},
                "legal_corpus": {},
                "playbooks": {}
            }
            
            # Cases summary
            try:
                cases_file = Path("app/data/demo_cases.json")
                if cases_file.exists():
                    with open(cases_file, 'r') as f:
                        cases_data = json.load(f)
                        cases = cases_data.get("cases", [])
                        summary["cases"] = {
                            "total_cases": len(cases),
                            "by_status": {},
                            "by_type": {},
                            "case_types": list(set(case.get("case_type", "Unknown") for case in cases))
                        }
                        
                        # Count by status
                        for case in cases:
                            status = case.get("status", "Unknown")
                            summary["cases"]["by_status"][status] = summary["cases"]["by_status"].get(status, 0) + 1
                        
                        # Count by type
                        for case in cases:
                            case_type = case.get("case_type", "Unknown")
                            summary["cases"]["by_type"][case_type] = summary["cases"]["by_type"].get(case_type, 0) + 1
            except Exception as e:
                summary["cases"]["error"] = str(e)
            
            # Documents summary
            try:
                docs_file = Path("app/data/demo_documents.json")
                if docs_file.exists():
                    with open(docs_file, 'r') as f:
                        docs_data = json.load(f)
                        documents = docs_data.get("documents", [])
                        
                        # Get actual live analysis count
                        try:
                            from app.services.analysis_storage_service import AnalysisStorageService
                            storage_service = AnalysisStorageService()
                            storage_stats = storage_service.get_storage_stats()
                            analyzed_count = storage_stats.get("total_analyses", 0)
                        except Exception:
                            # Fallback to demo data flag
                            analyzed_count = sum(1 for doc in documents if doc.get("analysis_completed", False))
                        
                        summary["documents"] = {
                            "total_documents": len(documents),
                            "by_type": {},
                            "by_case": {},
                            "analyzed_count": analyzed_count,
                            "analysis_status": "AI analysis implemented and available"
                        }
                        
                        # Count by type
                        for doc in documents:
                            doc_type = doc.get("type", "Unknown")
                            summary["documents"]["by_type"][doc_type] = summary["documents"]["by_type"].get(doc_type, 0) + 1
                        
                        # Count by case
                        for doc in documents:
                            case_id = doc.get("case_id", "Unknown")
                            summary["documents"]["by_case"][case_id] = summary["documents"]["by_case"].get(case_id, 0) + 1
            except Exception as e:
                summary["documents"]["error"] = str(e)
            
            # Document analyses summary - AI analysis is now implemented
            summary["document_analyses"] = {
                "total_analyses": 0,
                "status": "AI document analysis implemented - live analysis only",
                "demo_data_available": False,
                "real_analysis_available": True
            }
            
            # Legal corpus summary
            try:
                corpus_path = Path("app/data/legal_corpus")
                demo_corpus_file = Path("app/data/demo_legal_corpus.json")
                
                summary["legal_corpus"] = {
                    "full_corpus": {"exists": False, "documents": 0, "categories": {}},
                    "demo_corpus": {"exists": False, "documents": 0, "categories": {}}
                }
                
                # Check full corpus
                if corpus_path.exists():
                    summary["legal_corpus"]["full_corpus"]["exists"] = True
                    doc_count = 0
                    categories = {}
                    
                    for category_dir in corpus_path.iterdir():
                        if category_dir.is_dir():
                            category_docs = len(list(category_dir.glob("*.txt")))
                            categories[category_dir.name] = category_docs
                            doc_count += category_docs
                    
                    summary["legal_corpus"]["full_corpus"]["documents"] = doc_count
                    summary["legal_corpus"]["full_corpus"]["categories"] = categories
                
                # Check demo corpus
                if demo_corpus_file.exists():
                    with open(demo_corpus_file, 'r') as f:
                        demo_corpus = json.load(f)
                        summary["legal_corpus"]["demo_corpus"]["exists"] = True
                        summary["legal_corpus"]["demo_corpus"]["documents"] = len(demo_corpus)
                        
                        categories = {}
                        for doc in demo_corpus:
                            category = doc.get("category_name", "Unknown")
                            categories[category] = categories.get(category, 0) + 1
                        summary["legal_corpus"]["demo_corpus"]["categories"] = categories
            except Exception as e:
                summary["legal_corpus"]["error"] = str(e)
            
            # Playbooks summary
            try:
                playbooks_file = Path("app/data/demo_playbooks.json")
                if playbooks_file.exists():
                    with open(playbooks_file, 'r') as f:
                        playbooks_data = json.load(f)
                        playbooks = playbooks_data.get("playbooks", [])
                        summary["playbooks"] = {
                            "total_playbooks": len(playbooks),
                            "by_case_type": {},
                            "total_rules": sum(len(playbook.get("rules", [])) for playbook in playbooks),
                            "case_types": list(set(playbook.get("case_type", "Unknown") for playbook in playbooks))
                        }
                        
                        # Count by case type
                        for playbook in playbooks:
                            case_type = playbook.get("case_type", "Unknown")
                            summary["playbooks"]["by_case_type"][case_type] = summary["playbooks"]["by_case_type"].get(case_type, 0) + 1
            except Exception as e:
                summary["playbooks"]["error"] = str(e)
            
            return summary
            
        except Exception as e:
            return {"error": f"Failed to generate demo data summary: {str(e)}"}

system_status = SystemStatus()

@router.get("/health")
async def get_system_health():
    """Get comprehensive system health status"""
    
    health_checks = {
        "backend_api": system_status.check_backend_health(),
        "document_service": system_status.check_document_service(),
        "rag_service": system_status.check_rag_service(),
        "legal_corpus": system_status.check_legal_corpus(),
        "case_assessment": system_status.check_case_assessment()
    }
    
    # Calculate overall status
    statuses = [check["status"] for check in health_checks.values()]
    if "red" in statuses:
        overall_status = "red"
    elif "amber" in statuses:
        overall_status = "amber"
    else:
        overall_status = "green"
    
    return {
        "overall_status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "checks": health_checks,
        "summary": {
            "total_checks": len(health_checks),
            "green_count": statuses.count("green"),
            "amber_count": statuses.count("amber"),
            "red_count": statuses.count("red")
        }
    }

@router.post("/actions/initialize-corpus")
async def initialize_corpus():
    """Initialize the legal corpus and embeddings"""
    try:
        # This will trigger corpus initialization
        document_count = system_status.rag_service.initialize_vector_database()
        
        return {
            "success": True,
            "message": f"Corpus initialized with {document_count} documents",
            "timestamp": datetime.now().isoformat(),
            "document_count": document_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize corpus: {str(e)}")

@router.post("/actions/test-rag-search")
async def test_rag_search(query: str = "employment contract"):
    """Test RAG search functionality"""
    try:
        results = system_status.rag_service.search_legal_corpus(query, top_k=3)
        
        return {
            "success": True,
            "message": f"RAG search test completed - {len(results)} results",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results_count": len(results),
            "sample_results": [
                {
                    "content": r.content[:100] + "..." if len(r.content) > 100 else r.content,
                    "relevance_score": r.relevance_score,
                    "document_type": r.document_type
                }
                for r in results[:2]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG search test failed: {str(e)}")

# Bulk analysis removed - use the Analysis interface at /analysis for document analysis

@router.get("/demo-data-summary")
async def get_demo_data_summary():
    """Get comprehensive summary of all demo data"""
    try:
        summary = system_status.get_demo_data_summary()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get demo data summary: {str(e)}")

# Removed duplicate analyze-documents endpoint - use run-document-analysis instead