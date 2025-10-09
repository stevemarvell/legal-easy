from app.models.document import Document, DocumentAnalysis, KeyInformation
from app.models.case import Case
from app.models.playbook import CaseAssessment
from app.services.document_analyzer import DocumentAnalyzer


class AIAnalysisService:
    """Service for AI-powered document and case analysis"""
    
    def __init__(self):
        self.document_analyzer = DocumentAnalyzer()
    
    def analyze_document(self, document: Document) -> DocumentAnalysis:
        """Analyze a document using AI"""
        return self.document_analyzer.analyze_document(document)
    
    def generate_case_assessment(self, case: Case) -> CaseAssessment:
        """Generate AI-powered case assessment"""
        # Implementation will be added in later tasks
        pass
    
    def extract_key_information(self, text: str) -> KeyInformation:
        """Extract key information from text"""
        return self.document_analyzer.extract_key_information(text)