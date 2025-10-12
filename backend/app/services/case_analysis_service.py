#!/usr/bin/env python3
"""
Case Analysis Service - Integrated analysis linking cases, research corpus, and playbooks

This service provides comprehensive case analysis by:
1. Analyzing case documents and extracting key information
2. Finding relevant legal research and precedents
3. Applying appropriate legal playbooks and strategies
4. Generating strategic recommendations and risk assessments
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .data_service import DataService
from .ai_service import AIService


class CaseAnalysisService:
    """Service for comprehensive case analysis integrating documents, research, and playbooks."""
    
    @staticmethod
    def analyze_case_details(case_id: str) -> Dict[str, Any]:
        """
        Analyze case details from the case description to extract key legal elements,
        timeline, parties, issues, and strategic insights.
        """
        try:
            # Load case data
            cases = DataService.load_cases()
            case = next((c for c in cases if c.get('id') == case_id), None)
            
            if not case:
                return {"error": f"Case {case_id} not found"}
            
            description = case.get('description', '')
            if not description:
                return {"error": f"No description available for case {case_id}"}
            
            # Extract key elements from case description
            analysis = {
                "case_id": case_id,
                "case_title": case.get('title', ''),
                "case_type": case.get('case_type', ''),
                "analysis_timestamp": datetime.now().isoformat(),
                "legal_elements": CaseAnalysisService._extract_legal_elements(description),
                "timeline_analysis": CaseAnalysisService._extract_timeline(description),
                "parties_analysis": CaseAnalysisService._analyze_parties(description, case.get('key_parties', [])),
                "issues_analysis": CaseAnalysisService._identify_legal_issues(description, case.get('case_type', '')),
                "evidence_analysis": CaseAnalysisService._analyze_evidence(description),
                "risk_assessment": CaseAnalysisService._assess_risks(description, case.get('case_type', '')),
                "strategic_insights": CaseAnalysisService._generate_strategic_insights(description, case.get('case_type', '')),
                "case_strength": CaseAnalysisService._assess_case_strength(description, case.get('case_type', ''))
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze case details: {str(e)}"}

    @staticmethod
    def analyze_case_comprehensive(case_id: str, force_regenerate: bool = False) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a case by integrating:
        - Case documents analysis
        - Relevant research corpus
        - Applicable playbook strategies
        
        Args:
            case_id: The ID of the case to analyze
            force_regenerate: If True, regenerate analysis even if cached version exists
        """
        try:
            # Check if we have cached analysis and don't need to regenerate
            if not force_regenerate:
                cached_analysis = CaseAnalysisService._load_cached_analysis(case_id)
                if cached_analysis:
                    return cached_analysis
            
            # Load case information
            case = DataService.load_case_by_id(case_id)
            if not case:
                return {"error": "Case not found"}
            
            # Analyze case documents
            document_analysis = CaseAnalysisService._analyze_case_documents(case_id)
            
            # Find relevant research
            research_analysis = CaseAnalysisService._find_relevant_research(case, document_analysis)
            
            # Apply playbook strategies
            playbook_analysis = CaseAnalysisService._apply_playbook_strategies(case, document_analysis)
            
            # Generate strategic recommendations
            strategic_recommendations = CaseAnalysisService._generate_strategic_recommendations(
                case, document_analysis, research_analysis, playbook_analysis
            )
            
            # Calculate overall case assessment
            case_assessment = CaseAnalysisService._calculate_case_assessment(
                document_analysis, research_analysis, playbook_analysis
            )
            
            analysis_result = {
                "case_id": case_id,
                "case_info": case,
                "analysis_timestamp": datetime.now().isoformat(),
                "document_analysis": document_analysis,
                "research_analysis": research_analysis,
                "playbook_analysis": playbook_analysis,
                "strategic_recommendations": strategic_recommendations,
                "case_assessment": case_assessment
            }
            
            # Save the analysis for future use
            CaseAnalysisService._save_case_analysis(case_id, analysis_result)
            
            return analysis_result
            
        except Exception as e:
            print(f"Error in comprehensive case analysis: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _analyze_case_documents(case_id: str) -> Dict[str, Any]:
        """Analyze all documents in a case and extract key information."""
        try:
            documents = DataService.load_case_documents(case_id)
            if not documents:
                return {"documents": [], "summary": "No documents found"}
            
            document_analyses = []
            all_key_dates = []
            all_parties = []
            all_clauses = []
            all_risks = []
            document_types = []
            
            for doc in documents:
                doc_id = doc.get('id')
                if not doc_id:
                    continue
                
                # Get document analysis
                analysis = DataService.load_document_analysis(doc_id)
                if analysis:
                    document_analyses.append({
                        "document_id": doc_id,
                        "document_name": doc.get('name', ''),
                        "document_type": doc.get('type', ''),
                        "analysis": analysis
                    })
                    
                    # Aggregate key information
                    if analysis.get('key_dates'):
                        all_key_dates.extend(analysis['key_dates'])
                    if analysis.get('parties_involved'):
                        all_parties.extend(analysis['parties_involved'])
                    if analysis.get('key_clauses'):
                        all_clauses.extend(analysis['key_clauses'])
                    if analysis.get('potential_issues'):
                        all_risks.extend(analysis['potential_issues'])
                    if analysis.get('document_type'):
                        document_types.append(analysis['document_type'])
            
            # Deduplicate and clean up aggregated data
            unique_dates = list(set(all_key_dates))
            unique_parties = list(set(all_parties))
            unique_clauses = list(set(all_clauses))
            unique_risks = list(set(all_risks)) if all_risks else []
            
            # Extract key themes and patterns
            themes = CaseAnalysisService._extract_case_themes(document_analyses)
            timeline = CaseAnalysisService._build_case_timeline(unique_dates, document_analyses)
            
            return {
                "documents": document_analyses,
                "summary": {
                    "total_documents": len(document_analyses),
                    "document_types": list(set(document_types)),
                    "key_dates": sorted(unique_dates),
                    "parties_involved": unique_parties,
                    "key_clauses": unique_clauses[:10],  # Top 10 clauses
                    "potential_risks": unique_risks,
                    "themes": themes,
                    "timeline": timeline
                }
            }
            
        except Exception as e:
            print(f"Error analyzing case documents: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _find_relevant_research(case: Dict[str, Any], document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Find relevant research corpus items based on case type and document analysis."""
        try:
            case_type = case.get('case_type', '')
            
            # Search research corpus based on case type
            research_items = DataService.search_corpus(case_type.lower())
            
            # Also search based on key themes from document analysis
            themes = document_analysis.get('summary', {}).get('themes', [])
            for theme in themes:
                theme_results = DataService.search_corpus(theme)
                research_items.extend(theme_results)
            
            # Deduplicate research items
            seen_ids = set()
            unique_research = []
            for item in research_items:
                if item.get('id') not in seen_ids:
                    unique_research.append(item)
                    seen_ids.add(item.get('id'))
            
            # Score relevance of research items
            scored_research = CaseAnalysisService._score_research_relevance(
                unique_research, case, document_analysis
            )
            
            # Get top relevant items
            top_research = sorted(scored_research, key=lambda x: x.get('relevance_score', 0), reverse=True)[:10]
            
            # Categorize research by type
            categorized_research = CaseAnalysisService._categorize_research(top_research)
            
            return {
                "total_found": len(unique_research),
                "top_relevant": top_research,
                "categorized": categorized_research,
                "search_terms": [case_type.lower()] + themes
            }
            
        except Exception as e:
            print(f"Error finding relevant research: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _apply_playbook_strategies(case: Dict[str, Any], document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply relevant playbook strategies based on case type and analysis."""
        try:
            playbook_id = case.get('playbook_id')
            if not playbook_id:
                return {"error": "No playbook assigned to case"}
            
            # Load the playbook
            playbook = DataService.load_playbook_by_id(playbook_id)
            if not playbook:
                return {"error": f"Playbook {playbook_id} not found"}
            
            # Apply playbook rules
            applicable_rules = CaseAnalysisService._evaluate_playbook_rules(
                playbook, case, document_analysis
            )
            
            # Navigate decision tree
            decision_path = CaseAnalysisService._navigate_decision_tree(
                playbook, case, document_analysis
            )
            
            # Calculate monetary assessment
            monetary_assessment = CaseAnalysisService._calculate_monetary_assessment(
                playbook, decision_path, document_analysis
            )
            
            # Get escalation path
            escalation_path = playbook.get('escalation_paths', [])
            
            return {
                "playbook_id": playbook_id,
                "playbook_name": playbook.get('name', ''),
                "applicable_rules": applicable_rules,
                "decision_path": decision_path,
                "monetary_assessment": monetary_assessment,
                "escalation_path": escalation_path,
                "key_statutes": playbook.get('key_statutes', []),
                "success_factors": playbook.get('success_factors', [])
            }
            
        except Exception as e:
            print(f"Error applying playbook strategies: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _generate_strategic_recommendations(
        case: Dict[str, Any], 
        document_analysis: Dict[str, Any], 
        research_analysis: Dict[str, Any], 
        playbook_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate strategic recommendations based on all analysis components."""
        try:
            recommendations = []
            
            # Document-based recommendations
            doc_summary = document_analysis.get('summary', {})
            risks = doc_summary.get('potential_risks', [])
            
            if risks:
                recommendations.append({
                    "category": "Risk Management",
                    "priority": "High",
                    "recommendation": f"Address identified risks: {', '.join(risks[:3])}",
                    "basis": "Document analysis revealed potential issues"
                })
            
            # Research-based recommendations
            top_research = research_analysis.get('top_relevant', [])
            if top_research:
                precedents = [r for r in top_research if r.get('category') == 'precedents']
                if precedents:
                    recommendations.append({
                        "category": "Legal Precedents",
                        "priority": "Medium",
                        "recommendation": f"Review relevant precedents: {precedents[0].get('name', 'N/A')}",
                        "basis": "Similar cases found in research corpus"
                    })
            
            # Playbook-based recommendations
            decision_path = playbook_analysis.get('decision_path', {})
            if decision_path.get('recommended_actions'):
                for action in decision_path['recommended_actions'][:2]:
                    recommendations.append({
                        "category": "Strategic Action",
                        "priority": "High",
                        "recommendation": action,
                        "basis": "Playbook decision tree analysis"
                    })
            
            # Timeline-based recommendations
            timeline = doc_summary.get('timeline', [])
            if timeline:
                upcoming_dates = [t for t in timeline if t.get('date') and t['date'] > datetime.now().strftime('%Y-%m-%d')]
                if upcoming_dates:
                    recommendations.append({
                        "category": "Timeline Management",
                        "priority": "High",
                        "recommendation": f"Monitor upcoming deadline: {upcoming_dates[0].get('description', 'N/A')}",
                        "basis": "Critical dates identified in case timeline"
                    })
            
            # Strength assessment
            strength_assessment = CaseAnalysisService._assess_case_strength(
                document_analysis, research_analysis, playbook_analysis
            )
            
            return {
                "recommendations": recommendations,
                "strength_assessment": strength_assessment,
                "next_steps": CaseAnalysisService._determine_next_steps(playbook_analysis, recommendations),
                "risk_factors": CaseAnalysisService._identify_risk_factors(document_analysis, playbook_analysis)
            }
            
        except Exception as e:
            print(f"Error generating strategic recommendations: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _calculate_case_assessment(
        document_analysis: Dict[str, Any], 
        research_analysis: Dict[str, Any], 
        playbook_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall case assessment score and confidence."""
        try:
            # Document analysis score (0-1)
            doc_score = 0.0
            doc_summary = document_analysis.get('summary', {})
            if doc_summary.get('key_dates'):
                doc_score += 0.2
            if doc_summary.get('parties_involved'):
                doc_score += 0.2
            if doc_summary.get('key_clauses'):
                doc_score += 0.3
            if not doc_summary.get('potential_risks'):
                doc_score += 0.3
            
            # Research support score (0-1)
            research_score = 0.0
            top_research = research_analysis.get('top_relevant', [])
            if top_research:
                research_score = min(len(top_research) / 10, 1.0)
            
            # Playbook alignment score (0-1)
            playbook_score = 0.0
            decision_path = playbook_analysis.get('decision_path', {})
            if decision_path.get('result'):
                if 'strong' in decision_path['result'].lower():
                    playbook_score = 0.9
                elif 'moderate' in decision_path['result'].lower():
                    playbook_score = 0.6
                else:
                    playbook_score = 0.3
            
            # Overall assessment (weighted average)
            overall_score = (doc_score * 0.4 + research_score * 0.3 + playbook_score * 0.3)
            
            # Determine assessment level
            if overall_score >= 0.8:
                assessment_level = "Strong"
                confidence = "High"
            elif overall_score >= 0.6:
                assessment_level = "Moderate"
                confidence = "Medium"
            else:
                assessment_level = "Weak"
                confidence = "Low"
            
            return {
                "overall_score": round(overall_score, 2),
                "assessment_level": assessment_level,
                "confidence": confidence,
                "component_scores": {
                    "document_analysis": round(doc_score, 2),
                    "research_support": round(research_score, 2),
                    "playbook_alignment": round(playbook_score, 2)
                }
            }
            
        except Exception as e:
            print(f"Error calculating case assessment: {e}")
            return {"error": str(e)}
    
    # Helper methods
    
    @staticmethod
    def _extract_case_themes(document_analyses: List[Dict[str, Any]]) -> List[str]:
        """Extract key themes from document analyses."""
        themes = []
        
        for doc_analysis in document_analyses:
            analysis = doc_analysis.get('analysis', {})
            
            # Extract themes from document type
            doc_type = analysis.get('document_type', '')
            if doc_type and doc_type not in themes:
                themes.append(doc_type.lower())
            
            # Extract themes from key clauses
            clauses = analysis.get('key_clauses', [])
            for clause in clauses:
                if isinstance(clause, str):
                    # Extract key legal terms
                    legal_terms = re.findall(r'\b(?:termination|confidentiality|employment|contract|breach|liability|damages|notice|compensation|benefits)\b', clause.lower())
                    themes.extend([term for term in legal_terms if term not in themes])
        
        return themes[:10]  # Return top 10 themes
    
    @staticmethod
    def _build_case_timeline(dates: List[str], document_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build a timeline of key events from case documents."""
        timeline = []
        
        for date in sorted(dates):
            # Find documents that reference this date
            related_docs = []
            for doc_analysis in document_analyses:
                analysis = doc_analysis.get('analysis', {})
                if date in analysis.get('key_dates', []):
                    related_docs.append(doc_analysis.get('document_name', ''))
            
            timeline.append({
                "date": date,
                "description": f"Key date referenced in: {', '.join(related_docs)}",
                "related_documents": related_docs
            })
        
        return timeline
    
    @staticmethod
    def _score_research_relevance(
        research_items: List[Dict[str, Any]], 
        case: Dict[str, Any], 
        document_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Score research items for relevance to the case."""
        case_type = case.get('case_type', '').lower()
        themes = document_analysis.get('summary', {}).get('themes', [])
        
        for item in research_items:
            score = 0.0
            
            # Score based on case type match
            title = item.get('title', '').lower()
            description = item.get('description', '').lower()
            research_areas = item.get('research_areas', [])
            
            if case_type in title:
                score += 0.4
            if case_type in description:
                score += 0.3
            
            # Score based on research areas
            for area in research_areas:
                if case_type in area.lower():
                    score += 0.3
            
            # Score based on theme matches
            for theme in themes:
                if theme in title:
                    score += 0.2
                if theme in description:
                    score += 0.1
                for area in research_areas:
                    if theme in area.lower():
                        score += 0.1
            
            item['relevance_score'] = min(score, 1.0)
        
        return research_items
    
    @staticmethod
    def _categorize_research(research_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize research items by type."""
        categories = {
            "precedents": [],
            "statutes": [],
            "contracts": [],
            "clauses": []
        }
        
        for item in research_items:
            category = item.get('category', 'unknown')
            if category in categories:
                categories[category].append(item)
        
        return categories
    
    @staticmethod
    def _evaluate_playbook_rules(
        playbook: Dict[str, Any], 
        case: Dict[str, Any], 
        document_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Evaluate which playbook rules apply to the case."""
        applicable_rules = []
        rules = playbook.get('rules', [])
        
        # This is a simplified rule evaluation - in practice, this would be more sophisticated
        for rule in rules:
            # Check if rule conditions might apply based on case type and document analysis
            condition = rule.get('condition', '')
            weight = rule.get('weight', 0.0)
            
            # Simple keyword matching for demonstration
            doc_summary = document_analysis.get('summary', {})
            themes = doc_summary.get('themes', [])
            risks = doc_summary.get('potential_risks', [])
            
            applies = False
            if any(theme in condition for theme in themes):
                applies = True
            elif any(risk in condition for risk in risks):
                applies = True
            
            if applies:
                applicable_rules.append({
                    "rule_id": rule.get('id'),
                    "condition": condition,
                    "action": rule.get('action'),
                    "weight": weight,
                    "description": rule.get('description'),
                    "legal_basis": rule.get('legal_basis'),
                    "evidence_required": rule.get('evidence_required', [])
                })
        
        return sorted(applicable_rules, key=lambda x: x.get('weight', 0), reverse=True)
    
    @staticmethod
    def _navigate_decision_tree(
        playbook: Dict[str, Any], 
        case: Dict[str, Any], 
        document_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Navigate the playbook decision tree based on case facts."""
        decision_tree = playbook.get('decision_tree', {})
        if not decision_tree:
            return {}
        
        # This is a simplified navigation - in practice, this would involve more complex logic
        # For now, we'll assume a moderate case assessment
        nodes = decision_tree.get('nodes', {})
        moderate_assessment = nodes.get('moderate_case_assessment', {})
        
        return moderate_assessment
    
    @staticmethod
    def _calculate_monetary_assessment(
        playbook: Dict[str, Any], 
        decision_path: Dict[str, Any], 
        document_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate monetary assessment based on playbook and case analysis."""
        monetary_ranges = playbook.get('monetary_ranges', {})
        assessment_range = decision_path.get('monetary_range', 'medium')
        
        if assessment_range in monetary_ranges:
            range_info = monetary_ranges[assessment_range]
            return {
                "range": range_info.get('range', [0, 0]),
                "description": range_info.get('description', ''),
                "factors": range_info.get('factors', [])
            }
        
        return {"range": [0, 0], "description": "Unable to assess", "factors": []}
    
    @staticmethod
    def _assess_case_strength(
        document_analysis: Dict[str, Any], 
        research_analysis: Dict[str, Any], 
        playbook_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess overall case strength."""
        strengths = []
        weaknesses = []
        
        # Document-based assessment
        doc_summary = document_analysis.get('summary', {})
        if doc_summary.get('key_dates'):
            strengths.append("Clear timeline established")
        if doc_summary.get('key_clauses'):
            strengths.append("Key contractual provisions identified")
        if doc_summary.get('potential_risks'):
            weaknesses.append("Potential risks identified in documents")
        
        # Research support
        if research_analysis.get('top_relevant'):
            strengths.append("Supporting legal precedents available")
        
        # Playbook assessment
        decision_path = playbook_analysis.get('decision_path', {})
        if 'strong' in decision_path.get('result', '').lower():
            strengths.append("Strong case according to playbook analysis")
        elif 'weak' in decision_path.get('result', '').lower():
            weaknesses.append("Weak case according to playbook analysis")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "overall": "Strong" if len(strengths) > len(weaknesses) else "Moderate" if len(strengths) == len(weaknesses) else "Weak"
        }
    
    @staticmethod
    def _determine_next_steps(
        playbook_analysis: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ) -> List[str]:
        """Determine immediate next steps."""
        next_steps = []
        
        # From playbook
        decision_path = playbook_analysis.get('decision_path', {})
        if decision_path.get('recommended_actions'):
            next_steps.extend(decision_path['recommended_actions'][:2])
        
        # From high-priority recommendations
        high_priority_recs = [r for r in recommendations if r.get('priority') == 'High']
        for rec in high_priority_recs[:2]:
            next_steps.append(rec.get('recommendation', ''))
        
        return next_steps[:5]  # Top 5 next steps
    
    @staticmethod
    def _identify_risk_factors(
        document_analysis: Dict[str, Any], 
        playbook_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify key risk factors."""
        risks = []
        
        # From document analysis
        doc_risks = document_analysis.get('summary', {}).get('potential_risks', [])
        risks.extend(doc_risks)
        
        # From playbook analysis
        applicable_rules = playbook_analysis.get('applicable_rules', [])
        for rule in applicable_rules:
            if 'risk' in rule.get('description', '').lower():
                risks.append(rule.get('description', ''))
        
        return list(set(risks))[:5]  # Top 5 unique risks
    
    @staticmethod
    def has_cached_analysis(case_id: str) -> bool:
        """Check if cached analysis exists for a case."""
        try:
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_analysis" / "case_analysis.json"
            
            if not analysis_path.exists():
                return False
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                all_analyses = json.load(f)
            
            return case_id in all_analyses
            
        except Exception as e:
            print(f"Error checking cached analysis: {e}")
            return False
    
    @staticmethod
    def _load_cached_analysis(case_id: str) -> Optional[Dict[str, Any]]:
        """Load cached case analysis if it exists and is recent."""
        try:
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_analysis" / "case_analysis.json"
            
            if not analysis_path.exists():
                return None
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                all_analyses = json.load(f)
            
            if case_id not in all_analyses:
                return None
            
            cached_analysis = all_analyses[case_id]
            
            # Check if analysis is recent (less than 24 hours old)
            analysis_time = datetime.fromisoformat(cached_analysis.get('analysis_timestamp', ''))
            if (datetime.now() - analysis_time).total_seconds() > 86400:  # 24 hours
                return None
            
            return cached_analysis
            
        except Exception as e:
            print(f"Error loading cached analysis: {e}")
            return None
    
    @staticmethod
    def _save_case_analysis(case_id: str, analysis: Dict[str, Any]) -> None:
        """Save case analysis results to storage."""
        try:
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_analysis" / "case_analysis.json"
            
            # Ensure directory exists
            analysis_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing analyses
            all_analyses = {}
            if analysis_path.exists():
                with open(analysis_path, 'r', encoding='utf-8') as f:
                    all_analyses = json.load(f)
            
            # Add or update analysis
            all_analyses[case_id] = analysis
            
            # Save back to file
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(all_analyses, f, indent=2, ensure_ascii=False)
                
            print(f"Saved case analysis for case {case_id}")
                
        except Exception as e:
            print(f"Error saving case analysis: {e}")
            # Don't raise the error - analysis generation should still work even if saving fails
    
    @staticmethod
    def regenerate_all_case_analyses() -> Dict[str, Any]:
        """Regenerate analysis for all cases in the system."""
        try:
            cases = DataService.load_cases()
            total_cases = len(cases)
            analyzed_cases = 0
            failed_cases = 0
            confidence_scores = []
            
            for case in cases:
                try:
                    case_id = case.get('id')
                    if case_id:
                        # Force regenerate analysis
                        analysis = CaseAnalysisService.analyze_case_comprehensive(case_id, force_regenerate=True)
                        
                        if "error" not in analysis:
                            analyzed_cases += 1
                            # Extract confidence score if available
                            case_assessment = analysis.get("case_assessment", {})
                            if "overall_score" in case_assessment:
                                confidence_scores.append(case_assessment["overall_score"])
                        else:
                            failed_cases += 1
                            print(f"Failed to analyze case {case_id}: {analysis['error']}")
                    else:
                        failed_cases += 1
                        print(f"Case missing ID: {case}")
                        
                except Exception as e:
                    failed_cases += 1
                    print(f"Error analyzing case {case.get('id', 'unknown')}: {str(e)}")
            
            # Calculate average confidence
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            return {
                "total_cases": total_cases,
                "analyzed_cases": analyzed_cases,
                "failed_cases": failed_cases,
                "average_confidence": round(average_confidence, 3)
            }
            
        except Exception as e:
            print(f"Error regenerating all case analyses: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_analysis_statistics() -> Dict[str, Any]:
        """Get statistics about case analyses."""
        try:
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_analysis" / "case_analysis.json"
            
            if not analysis_path.exists():
                return {
                    "total_analyses": 0,
                    "recent_analyses": 0,
                    "average_confidence": 0.0
                }
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                all_analyses = json.load(f)
            
            total_analyses = len(all_analyses)
            recent_analyses = 0
            confidence_scores = []
            
            # Count recent analyses (last 7 days) and collect confidence scores
            from datetime import timedelta
            seven_days_ago = datetime.now() - timedelta(days=7)
            
            for analysis in all_analyses.values():
                # Check if analysis is recent
                try:
                    analysis_time = datetime.fromisoformat(analysis.get('analysis_timestamp', ''))
                    if analysis_time >= seven_days_ago:
                        recent_analyses += 1
                except:
                    pass
                
                # Collect confidence scores
                case_assessment = analysis.get('case_assessment', {})
                if 'overall_score' in case_assessment:
                    confidence_scores.append(case_assessment['overall_score'])
            
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            return {
                "total_analyses": total_analyses,
                "recent_analyses": recent_analyses,
                "average_confidence": round(average_confidence, 3)
            }
            
        except Exception as e:
            print(f"Error getting analysis statistics: {e}")
            return {"error": str(e)}

    @staticmethod
    def _extract_legal_elements(description: str) -> Dict[str, Any]:
        """Extract key legal elements from case description"""
        elements = {
            "contracts": [],
            "statutes": [],
            "regulations": [],
            "legal_concepts": [],
            "monetary_amounts": [],
            "dates": [],
            "locations": []
        }
        
        # Extract contracts and agreements
        contract_patterns = [
            r'([A-Z][a-zA-Z\s]+Agreement)',
            r'([A-Z][a-zA-Z\s]+Contract)',
            r'employment agreement',
            r'licence agreement',
            r'consulting agreement'
        ]
        
        for pattern in contract_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            elements["contracts"].extend([match.strip() for match in matches if match.strip()])
        
        # Extract statutes and acts
        statute_patterns = [
            r'([A-Z][a-zA-Z\s]+Act \d{4})',
            r'([A-Z][a-zA-Z\s]+Regulations \d{4})',
            r'(Public Interest Disclosure Act)',
            r'(Employment Rights Act)',
            r'(Health and Safety at Work Act)'
        ]
        
        for pattern in statute_patterns:
            matches = re.findall(pattern, description)
            elements["statutes"].extend([match.strip() for match in matches if match.strip()])
        
        # Extract monetary amounts
        money_patterns = [
            r'£([\d,]+(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*)\s*(?:pounds?|GBP)',
        ]
        
        for pattern in money_patterns:
            matches = re.findall(pattern, description)
            elements["monetary_amounts"].extend([f"£{match}" if not match.startswith('£') else match for match in matches])
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'([A-Z][a-z]+\s+\d{4})'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, description)
            elements["dates"].extend([match.strip() for match in matches if match.strip()])
        
        # Remove duplicates
        for key in elements:
            elements[key] = list(set(elements[key]))
        
        return elements

    @staticmethod
    def _extract_timeline(description: str) -> Dict[str, Any]:
        """Extract and analyze timeline from case description"""
        timeline_events = []
        
        # Pattern to find date-based events
        event_patterns = [
            r'On (\d{1,2}\s+[A-Z][a-z]+\s+\d{4}),?\s*([^.]+\.)',
            r'(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})[,:]?\s*([^.]+\.)',
            r'Exactly (\d+\s+days?\s+later),?\s*on\s*(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})[,:]?\s*([^.]+\.)'
        ]
        
        for pattern in event_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if len(match) == 2:  # date, event
                    timeline_events.append({
                        "date": match[0].strip(),
                        "event": match[1].strip(),
                        "type": "key_event"
                    })
                elif len(match) == 3:  # relative time, date, event
                    timeline_events.append({
                        "date": match[1].strip(),
                        "event": match[2].strip(),
                        "relative_timing": match[0].strip(),
                        "type": "consequential_event"
                    })
        
        return {
            "events": timeline_events[:10],  # Limit to top 10 events
            "total_events_found": len(timeline_events),
            "timeline_span": CaseAnalysisService._calculate_timeline_span(timeline_events)
        }

    @staticmethod
    def _calculate_timeline_span(events: List[Dict]) -> str:
        """Calculate the span of the timeline"""
        if not events:
            return "No timeline data"
        
        dates = []
        for event in events:
            date_str = event.get('date', '')
            try:
                # Try to parse common date formats
                for fmt in ['%d %B %Y', '%B %Y', '%Y-%m-%d']:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        dates.append(date_obj)
                        break
                    except ValueError:
                        continue
            except:
                continue
        
        if len(dates) >= 2:
            span = max(dates) - min(dates)
            return f"{span.days} days ({span.days // 30} months)"
        
        return "Timeline span could not be calculated"

    @staticmethod
    def _analyze_parties(description: str, key_parties: List[str]) -> Dict[str, Any]:
        """Analyze parties involved in the case"""
        parties_analysis = {
            "primary_parties": key_parties,
            "additional_parties": [],
            "party_roles": {},
            "relationships": []
        }
        
        # Extract additional parties mentioned in description
        party_patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*\([^)]+\)',
            r'(Mr\.\s+[A-Z][a-z]+)',
            r'(Ms\.\s+[A-Z][a-z]+)',
            r'(Dr\.\s+[A-Z][a-z]+)'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, description)
            parties_analysis["additional_parties"].extend([match.strip() for match in matches])
        
        # Identify party roles
        role_patterns = [
            (r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*\(([^)]+)\)', 'role_in_parentheses'),
            (r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+(HR Director|CTO|CEO|Legal Counsel)', 'title_after_name'),
        ]
        
        for pattern, role_type in role_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if len(match) == 2:
                    parties_analysis["party_roles"][match[0]] = match[1]
        
        return parties_analysis

    @staticmethod
    def _identify_legal_issues(description: str, case_type: str) -> Dict[str, Any]:
        """Identify legal issues from the case description"""
        issues = {
            "primary_issues": [],
            "secondary_issues": [],
            "legal_theories": [],
            "potential_defenses": []
        }
        
        # Common legal issue patterns
        issue_patterns = {
            "employment": [
                r'(wrongful\s+(?:dismissal|termination))',
                r'(unfair\s+dismissal)',
                r'(victimisation)',
                r'(whistleblowing)',
                r'(age\s+discrimination)',
                r'(retaliation)',
                r'(breach\s+of\s+contract)'
            ],
            "contract": [
                r'(breach\s+of\s+(?:contract|agreement))',
                r'(licence\s+violation)',
                r'(intellectual\s+property\s+infringement)',
                r'(trade\s+secrets?\s+violation)',
                r'(non-compete\s+violation)'
            ]
        }
        
        case_type_lower = case_type.lower()
        relevant_patterns = []
        
        if 'employment' in case_type_lower:
            relevant_patterns.extend(issue_patterns.get('employment', []))
        if 'contract' in case_type_lower or 'intellectual' in case_type_lower:
            relevant_patterns.extend(issue_patterns.get('contract', []))
        
        for pattern in relevant_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            issues["primary_issues"].extend([match.strip() for match in matches])
        
        # Remove duplicates
        issues["primary_issues"] = list(set(issues["primary_issues"]))
        
        return issues

    @staticmethod
    def _analyze_evidence(description: str) -> Dict[str, Any]:
        """Analyze evidence mentioned in the case"""
        evidence = {
            "documentary_evidence": [],
            "witness_evidence": [],
            "expert_evidence": [],
            "physical_evidence": []
        }
        
        # Documentary evidence patterns
        doc_patterns = [
            r'(employment\s+(?:contract|agreement))',
            r'(termination\s+email)',
            r'(safety\s+report)',
            r'(server\s+logs)',
            r'(email\s+communications)',
            r'(performance\s+review)',
            r'(licence\s+agreement)'
        ]
        
        for pattern in doc_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            evidence["documentary_evidence"].extend([match.strip() for match in matches])
        
        # Witness evidence
        witness_patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+).*(?:reported|testified|stated|witnessed)',
            r'colleagues.*(?:reported|heard|witnessed)'
        ]
        
        for pattern in witness_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            evidence["witness_evidence"].extend([match.strip() for match in matches])
        
        return evidence

    @staticmethod
    def _assess_risks(description: str, case_type: str) -> Dict[str, Any]:
        """Assess risks based on case details"""
        risks = {
            "high_risk_factors": [],
            "medium_risk_factors": [],
            "low_risk_factors": [],
            "overall_risk_level": "medium"
        }
        
        # Risk indicators
        high_risk_indicators = [
            r'criminal\s+liability',
            r'regulatory\s+(?:fines?|penalties)',
            r'HSE\s+enforcement',
            r'£\d{2,}[,\d]*\s*(?:fine|penalty|damages)'
        ]
        
        medium_risk_indicators = [
            r'breach\s+of\s+contract',
            r'unfair\s+dismissal',
            r'discrimination',
            r'reputational\s+harm'
        ]
        
        for pattern in high_risk_indicators:
            if re.search(pattern, description, re.IGNORECASE):
                risks["high_risk_factors"].append(pattern.replace('\\s+', ' ').replace('\\d+', 'amount'))
        
        for pattern in medium_risk_indicators:
            if re.search(pattern, description, re.IGNORECASE):
                risks["medium_risk_factors"].append(pattern.replace('\\s+', ' '))
        
        # Determine overall risk level
        if risks["high_risk_factors"]:
            risks["overall_risk_level"] = "high"
        elif len(risks["medium_risk_factors"]) > 2:
            risks["overall_risk_level"] = "medium-high"
        elif risks["medium_risk_factors"]:
            risks["overall_risk_level"] = "medium"
        else:
            risks["overall_risk_level"] = "low"
        
        return risks

    @staticmethod
    def _generate_strategic_insights(description: str, case_type: str) -> Dict[str, Any]:
        """Generate strategic insights based on case analysis"""
        insights = {
            "key_strengths": [],
            "potential_weaknesses": [],
            "recommended_actions": [],
            "settlement_considerations": []
        }
        
        # Analyze for strengths
        strength_indicators = [
            (r'comprehensive\s+(?:report|documentation)', "Strong documentation"),
            (r'clear\s+(?:timeline|evidence)', "Clear evidence trail"),
            (r'regulatory\s+(?:breach|violation)', "Regulatory support"),
            (r'written\s+(?:contract|agreement)', "Written contractual terms")
        ]
        
        for pattern, strength in strength_indicators:
            if re.search(pattern, description, re.IGNORECASE):
                insights["key_strengths"].append(strength)
        
        # Analyze for weaknesses
        weakness_indicators = [
            (r'ambiguous\s+(?:terms|language)', "Ambiguous contract terms"),
            (r'good[- ]faith\s+interpretation', "Defendant claims good faith"),
            (r'coincidental\s+timing', "Timing may be disputed"),
            (r'limited\s+(?:evidence|documentation)', "Limited evidence")
        ]
        
        for pattern, weakness in weakness_indicators:
            if re.search(pattern, description, re.IGNORECASE):
                insights["potential_weaknesses"].append(weakness)
        
        # Generate recommendations based on case type
        if 'employment' in case_type.lower():
            insights["recommended_actions"] = [
                "File ACAS early conciliation",
                "Gather witness statements",
                "Document timeline of events",
                "Preserve all relevant communications"
            ]
        elif 'contract' in case_type.lower():
            insights["recommended_actions"] = [
                "Review contract terms thoroughly",
                "Gather technical evidence",
                "Assess damages calculation",
                "Consider alternative dispute resolution"
            ]
        
        return insights

    @staticmethod
    def _assess_case_strength(description: str, case_type: str) -> Dict[str, Any]:
        """Assess overall case strength"""
        strength_factors = {
            "evidence_strength": 0,
            "legal_precedent": 0,
            "timeline_clarity": 0,
            "documentation_quality": 0
        }
        
        # Evidence strength indicators
        evidence_indicators = [
            r'comprehensive\s+(?:report|analysis)',
            r'detailed\s+(?:documentation|records)',
            r'witness\s+(?:statements|testimony)',
            r'expert\s+(?:analysis|testimony)'
        ]
        
        evidence_score = sum(1 for pattern in evidence_indicators if re.search(pattern, description, re.IGNORECASE))
        strength_factors["evidence_strength"] = min(evidence_score * 25, 100)
        
        # Timeline clarity
        timeline_indicators = [
            r'on\s+\d{1,2}\s+[A-Z][a-z]+\s+\d{4}',
            r'exactly\s+\d+\s+days',
            r'at\s+\d{1,2}:\d{2}\s+[AP]M'
        ]
        
        timeline_score = sum(1 for pattern in timeline_indicators if re.search(pattern, description, re.IGNORECASE))
        strength_factors["timeline_clarity"] = min(timeline_score * 20, 100)
        
        # Calculate overall strength
        overall_score = sum(strength_factors.values()) / len(strength_factors)
        
        if overall_score >= 75:
            strength_level = "Strong"
        elif overall_score >= 50:
            strength_level = "Moderate"
        else:
            strength_level = "Weak"
        
        return {
            "overall_score": round(overall_score, 1),
            "strength_level": strength_level,
            "factor_scores": strength_factors,
            "confidence_level": min(overall_score / 100, 0.95)
        }