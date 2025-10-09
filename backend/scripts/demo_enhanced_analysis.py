#!/usr/bin/env python3
"""
Enhanced Document Analysis Demonstration Script

This script demonstrates the new advanced features of the Document Analysis Algorithm v2.1.0
including risk assessment, compliance analysis, semantic understanding, and enhanced confidence scoring.

Usage:
    python scripts/demo_enhanced_analysis.py
"""

import sys
import os
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.document_service import DocumentService
from app.services.ai_analysis_service import AIAnalysisService


def print_separator(title: str):
    """Print a formatted section separator"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print a formatted subsection separator"""
    print(f"\n--- {title} ---")


def format_confidence_score(score: float) -> str:
    """Format confidence score with color coding"""
    percentage = f"{score:.1%}"
    if score >= 0.9:
        return f"🟢 {percentage} (Excellent)"
    elif score >= 0.75:
        return f"🟡 {percentage} (Good)"
    elif score >= 0.5:
        return f"🟠 {percentage} (Fair)"
    else:
        return f"🔴 {percentage} (Poor)"


def format_risk_level(risk_level: str) -> str:
    """Format risk level with appropriate emoji"""
    risk_map = {
        'low': '🟢 LOW RISK',
        'medium': '🟡 MEDIUM RISK',
        'high': '🔴 HIGH RISK'
    }
    return risk_map.get(risk_level, f'❓ {risk_level.upper()}')


def format_compliance_status(status: str) -> str:
    """Format compliance status with appropriate emoji"""
    status_map = {
        'compliant': '✅ COMPLIANT',
        'partially_compliant': '⚠️ PARTIALLY COMPLIANT',
        'non_compliant': '❌ NON-COMPLIANT',
        'unknown': '❓ UNKNOWN'
    }
    return status_map.get(status, f'❓ {status.upper()}')


def analyze_document_enhanced(doc_service, ai_service, document):
    """Perform enhanced analysis on a document and display results"""
    
    print_separator(f"ENHANCED ANALYSIS: {document.name}")
    
    # Basic document info
    print(f"📄 Document ID: {document.id}")
    print(f"📁 Case ID: {document.case_id}")
    print(f"📋 Original Type: {document.type}")
    print(f"📏 Size: {document.size:,} bytes")
    print(f"📅 Upload Date: {document.upload_date.strftime('%Y-%m-%d %H:%M')}")
    
    # Perform enhanced analysis
    print("\n🔍 Performing enhanced AI analysis...")
    start_time = datetime.now()
    analysis = ai_service.analyze_document(document)
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    print(f"⚡ Analysis completed in {processing_time:.2f} seconds")
    
    # Core Analysis Results
    print_subsection("CORE ANALYSIS RESULTS")
    print(f"📋 Document Type: {analysis.document_type}")
    print(f"👥 Parties Found: {len(analysis.parties_involved)}")
    for i, party in enumerate(analysis.parties_involved[:5], 1):
        print(f"   {i}. {party}")
    if len(analysis.parties_involved) > 5:
        print(f"   ... and {len(analysis.parties_involved) - 5} more")
    
    print(f"📅 Key Dates: {len(analysis.key_dates)}")
    for i, date in enumerate(analysis.key_dates[:3], 1):
        print(f"   {i}. {date}")
    if len(analysis.key_dates) > 3:
        print(f"   ... and {len(analysis.key_dates) - 3} more")
    
    # Enhanced Features
    print_subsection("ENHANCED ANALYSIS FEATURES")
    
    # Risk Assessment
    print(f"⚠️  Risk Level: {format_risk_level(analysis.risk_level)}")
    if analysis.potential_issues:
        print(f"🚨 Potential Issues ({len(analysis.potential_issues)}):")
        for i, issue in enumerate(analysis.potential_issues[:3], 1):
            print(f"   {i}. {issue}")
        if len(analysis.potential_issues) > 3:
            print(f"   ... and {len(analysis.potential_issues) - 3} more")
    else:
        print("✅ No significant issues identified")
    
    # Compliance Analysis
    print(f"📋 Compliance Status: {format_compliance_status(analysis.compliance_status)}")
    
    # Semantic Analysis
    print(f"🎯 Document Intent: {analysis.document_intent or 'Unknown'}")
    print(f"🧠 Complexity Score: {analysis.complexity_score:.2f}/1.0")
    
    # Critical Deadlines
    if analysis.critical_deadlines:
        print(f"⏰ Critical Deadlines ({len(analysis.critical_deadlines)}):")
        for i, deadline in enumerate(analysis.critical_deadlines[:3], 1):
            deadline_type = deadline.get('type', 'unknown')
            period = deadline.get('period', deadline.get('text', 'N/A'))
            print(f"   {i}. {deadline_type.title()}: {period}")
    else:
        print("⏰ No critical deadlines identified")
    
    # Confidence Scores
    print_subsection("CONFIDENCE SCORES")
    for category, score in analysis.confidence_scores.items():
        formatted_category = category.replace('_', ' ').title()
        print(f"{formatted_category}: {format_confidence_score(score)}")
    
    # Document Summary
    print_subsection("AI-GENERATED SUMMARY")
    print(f"📝 {analysis.summary}")
    
    # Key Clauses
    if analysis.key_clauses:
        print_subsection("KEY CLAUSES IDENTIFIED")
        for i, clause in enumerate(analysis.key_clauses[:5], 1):
            print(f"{i}. {clause}")
        if len(analysis.key_clauses) > 5:
            print(f"... and {len(analysis.key_clauses) - 5} more clauses")
    
    # Metadata
    print_subsection("ANALYSIS METADATA")
    print(f"🔧 Analysis Version: {analysis.analysis_version}")
    print(f"⏱️  Analysis Timestamp: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return analysis


def main():
    """Main demonstration function"""
    
    print_separator("ENHANCED DOCUMENT ANALYSIS ALGORITHM v2.1.0 DEMONSTRATION")
    print("This demonstration showcases the advanced features of the enhanced analysis algorithm:")
    print("• Risk Assessment Engine")
    print("• Compliance Analysis Engine") 
    print("• Semantic Analysis Engine")
    print("• Enhanced Confidence Scoring")
    print("• Temporal Analysis Engine")
    
    # Initialize services
    print("\n🚀 Initializing analysis services...")
    doc_service = DocumentService()
    ai_service = AIAnalysisService()
    
    # Load available documents
    print("📚 Loading available documents...")
    documents = doc_service._load_documents()
    print(f"✅ Loaded {len(documents)} documents")
    
    # Select interesting documents for demonstration
    demo_documents = [
        ("Employment Contract", lambda d: 'employment' in d.name.lower() and 'contract' in d.name.lower()),
        ("Safety Report", lambda d: 'safety' in d.name.lower()),
        ("Consulting Agreement", lambda d: 'consulting' in d.name.lower()),
        ("Non-Compete Agreement", lambda d: 'non-compete' in d.name.lower()),
        ("Email Communication", lambda d: 'email' in d.name.lower())
    ]
    
    analyses = []
    
    for doc_type, filter_func in demo_documents:
        matching_docs = [doc for doc in documents if filter_func(doc)]
        if matching_docs:
            document = matching_docs[0]  # Take the first matching document
            try:
                analysis = analyze_document_enhanced(doc_service, ai_service, document)
                analyses.append((doc_type, analysis))
            except Exception as e:
                print(f"❌ Error analyzing {document.name}: {str(e)}")
        else:
            print(f"⚠️  No {doc_type} found in document collection")
    
    # Summary comparison
    if analyses:
        print_separator("ANALYSIS COMPARISON SUMMARY")
        print(f"{'Document Type':<25} {'Risk':<15} {'Compliance':<20} {'Complexity':<12} {'Confidence':<12}")
        print("-" * 90)
        
        for doc_type, analysis in analyses:
            risk = analysis.risk_level or 'unknown'
            compliance = analysis.compliance_status or 'unknown'
            complexity = f"{analysis.complexity_score:.2f}" if analysis.complexity_score else 'N/A'
            avg_confidence = sum(analysis.confidence_scores.values()) / len(analysis.confidence_scores)
            confidence = f"{avg_confidence:.1%}"
            
            print(f"{doc_type:<25} {risk:<15} {compliance:<20} {complexity:<12} {confidence:<12}")
    
    print_separator("DEMONSTRATION COMPLETE")
    print("✅ Enhanced Document Analysis Algorithm v2.1.0 demonstration completed successfully!")
    print("\n📊 Key Improvements Demonstrated:")
    print("• Realistic confidence scores based on document quality")
    print("• Comprehensive risk assessment with actionable insights")
    print("• Multi-domain compliance analysis")
    print("• Advanced semantic understanding and intent recognition")
    print("• Temporal analysis for time-sensitive elements")
    print("\n🚀 The algorithm is now ready for production use with enhanced capabilities!")


if __name__ == "__main__":
    main()