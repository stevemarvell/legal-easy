#!/usr/bin/env python3
"""
PlaybookService - Simple playbook service for the Legal AI System

This service handles playbook-related operations including:
- Playbook matching for case type matching
- Comprehensive case analysis using playbooks
- Fallback to general analysis when no playbook matches
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PlaybookService:
    """Simple playbook matching and case analysis."""
    
    # === PLAYBOOK MATCHING ===
    
    @staticmethod
    def match_playbook(case_type: str) -> Optional[Dict[str, Any]]:
        """Match playbook for case type matching."""
        try:
            playbooks_index_path = Path("data/playbooks/playbooks_index.json")
            if not playbooks_index_path.exists():
                return None
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                playbooks_data = json.load(f)
                # Handle both array format and object with 'playbooks' key
                if isinstance(playbooks_data, list):
                    playbooks = playbooks_data
                else:
                    playbooks = playbooks_data.get('playbooks', [])
            
            # Find matching playbook by case type
            for playbook in playbooks:
                if playbook.get('case_type') == case_type:
                    return playbook
            
            return None
        except Exception as e:
            print(f"Error matching playbook: {e}")
            return None
    
    # === COMPREHENSIVE CASE ANALYSIS ===
    
    @staticmethod
    def analyze_case_with_playbook(case_id: str) -> Dict[str, Any]:
        """Analyze case with playbook for comprehensive case analysis."""
        try:
            # Load case data
            from .data_service import ResearchService
            cases = ResearchService.load_cases()
            case = None
            for c in cases:
                if c.get('id') == case_id:
                    case = c
                    break
            
            if not case:
                return PlaybookService._generate_fallback_analysis(case_id, "Case not found")
            
            case_type = case.get('case_type')
            if not case_type:
                return PlaybookService._generate_fallback_analysis(case_id, "No case type specified")
            
            # Try to match playbook
            playbook = PlaybookService.match_playbook(case_type)
            if not playbook:
                return PlaybookService._generate_fallback_analysis(case_id, f"No playbook found for case type: {case_type}")
            
            # Apply playbook rules to generate comprehensive analysis
            playbook_result = PlaybookService._apply_playbook_rules(case, playbook)
            
            # Generate comprehensive case analysis
            analysis = {
                "case_id": case_id,
                "case_strength_assessment": {
                    "overall_strength": playbook_result.get('case_strength', 'Unknown'),
                    "confidence_level": playbook_result.get('confidence_level', 0.5),
                    "key_strengths": playbook_result.get('key_strengths', []),
                    "potential_weaknesses": playbook_result.get('potential_weaknesses', []),
                    "supporting_evidence": playbook_result.get('supporting_evidence', [])
                },
                "strategic_recommendations": PlaybookService._generate_strategic_recommendations(playbook_result),
                "relevant_precedents": PlaybookService._get_relevant_precedents(case_type),
                "applied_playbook": {
                    "id": playbook.get('id'),
                    "name": playbook.get('name'),
                    "case_type": playbook.get('case_type')
                },
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing case with playbook: {e}")
            return PlaybookService._generate_fallback_analysis(case_id, f"Analysis error: {str(e)}")
    
    @staticmethod
    def _apply_playbook_rules(case: Dict[str, Any], playbook: Dict[str, Any]) -> Dict[str, Any]:
        """Apply playbook rules to a case and return detailed results."""
        case_id = case.get('id', '')
        playbook_id = playbook.get('id', '')
        
        # Get playbook rules
        rules = playbook.get('rules', [])
        if not rules:
            return {
                "case_id": case_id,
                "playbook_id": playbook_id,
                "applied_rules": [],
                "recommendations": [],
                "case_strength": "Weak",
                "confidence_level": 0.2,
                "key_strengths": [],
                "potential_weaknesses": ["No applicable rules found"],
                "supporting_evidence": [],
                "reasoning": "No rules available in playbook"
            }
        
        # Evaluate each rule against the case
        applied_rules = []
        recommendations = []
        key_strengths = []
        potential_weaknesses = []
        supporting_evidence = []
        total_weight = 0.0
        
        for rule in rules:
            if PlaybookService._evaluate_rule_condition(case, rule):
                applied_rules.append(rule.get('id', ''))
                
                # Add rule's action as recommendation
                action = rule.get('action')
                if action and action not in recommendations:
                    recommendations.append(action)
                
                # Add to strengths if high weight rule
                weight = rule.get('weight', 0.5)
                if weight >= 0.8:
                    key_strengths.append(rule.get('description', 'Strong legal position'))
                
                # Add evidence requirements as supporting evidence
                evidence = rule.get('evidence_required', [])
                supporting_evidence.extend(evidence)
                
                total_weight += weight
            else:
                # Add to potential weaknesses if important rule not met
                weight = rule.get('weight', 0.5)
                if weight >= 0.7:
                    potential_weaknesses.append(f"Does not meet: {rule.get('description', 'Important criteria')}")
        
        # Calculate case strength and confidence
        case_strength, confidence_level = PlaybookService._calculate_case_strength_and_confidence(
            total_weight, len(applied_rules), len(rules)
        )
        
        # Generate reasoning
        reasoning = PlaybookService._generate_reasoning(applied_rules, case_strength, len(rules))
        
        return {
            "case_id": case_id,
            "playbook_id": playbook_id,
            "applied_rules": applied_rules,
            "recommendations": recommendations,
            "case_strength": case_strength,
            "confidence_level": confidence_level,
            "key_strengths": list(set(key_strengths)),
            "potential_weaknesses": list(set(potential_weaknesses)),
            "supporting_evidence": list(set(supporting_evidence)),
            "reasoning": reasoning,
            "total_weight": total_weight,
            "rules_applied_count": len(applied_rules),
            "total_rules_count": len(rules)
        }
    
    @staticmethod
    def _evaluate_rule_condition(case: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Evaluate if a rule condition applies to a case."""
        condition = rule.get('condition', '').lower()
        case_summary = case.get('summary', '').lower()
        case_type = case.get('case_type', '').lower()
        
        # Simple keyword matching for common conditions
        condition_keywords = {
            'termination_within_protected_period': ['termination', 'dismissal', 'fired', 'protected'],
            'age_over_40_and_replaced_by_younger': ['age', 'discrimination', 'younger', 'replaced'],
            'documented_performance_issues': ['performance', 'issues', 'documented', 'problems'],
            'hostile_work_environment_pattern': ['hostile', 'harassment', 'bullying', 'environment'],
            'whistleblower_activity': ['whistleblower', 'reporting', 'violations', 'safety'],
            'pregnancy_or_family_leave_involved': ['pregnancy', 'maternity', 'family', 'leave'],
            'disability_accommodation_denied': ['disability', 'accommodation', 'denied', 'adjustments'],
            'clear_contract_terms_violated': ['breach', 'violation', 'failed to', 'did not'],
            'ambiguous_contract_language': ['ambiguous', 'unclear', 'disputed', 'interpretation'],
            'non_compete_violation': ['non-compete', 'competition', 'competitor', 'restraint'],
            'damages_easily_calculable': ['damages', 'loss', 'financial', 'calculable'],
            'ongoing_harm_occurring': ['ongoing', 'continuing', 'harm', 'damage'],
            'force_majeure_claimed': ['force majeure', 'impossible', 'unforeseen', 'circumstances'],
            'statute_of_frauds_issue': ['writing', 'written', 'signed', 'agreement'],
            'clear_debt_documentation': ['debt', 'invoice', 'payment', 'owed'],
            'debtor_disputes_amount': ['dispute', 'disagree', 'contest', 'challenge'],
            'debtor_claims_defective_services': ['defective', 'poor quality', 'unsatisfactory', 'substandard'],
            'debt_over_statute_limitations': ['old debt', 'statute', 'limitations', 'time-barred'],
            'debtor_has_assets': ['assets', 'property', 'income', 'resources'],
            'consumer_debt_uk_applies': ['consumer', 'personal', 'individual', 'household'],
            'debtor_filed_bankruptcy': ['bankruptcy', 'insolvency', 'administration', 'liquidation'],
            'personal_guarantee_exists': ['guarantee', 'guarantor', 'personal liability', 'surety'],
            'clear_liability_established': ['liability', 'fault', 'negligence', 'responsible'],
            'comparative_negligence_issue': ['comparative', 'contributory', 'shared fault', 'partial blame'],
            'serious_permanent_injury': ['serious', 'permanent', 'disability', 'life-changing'],
            'insurance_coverage_adequate': ['insurance', 'coverage', 'policy', 'insured']
        }
        
        # Check if condition keywords appear in case summary
        if condition in condition_keywords:
            keywords = condition_keywords[condition]
            return any(keyword in case_summary for keyword in keywords)
        
        # Fallback: simple substring matching
        return condition in case_summary or condition in case_type
    
    @staticmethod
    def _calculate_case_strength_and_confidence(total_weight: float, rules_count: int, total_rules: int) -> tuple:
        """Calculate case strength and confidence level based on applied rules and weights."""
        if rules_count == 0:
            return "Weak", 0.2
        
        # Normalize weight by number of rules applied
        average_weight = total_weight / rules_count if rules_count > 0 else 0
        
        # Calculate coverage (percentage of rules that applied)
        coverage = rules_count / total_rules if total_rules > 0 else 0
        
        # Determine case strength
        if average_weight >= 0.8 and coverage >= 0.5:
            case_strength = "Strong"
            confidence = min(0.9, 0.7 + (coverage * 0.2))
        elif average_weight >= 0.6 and coverage >= 0.3:
            case_strength = "Moderate"
            confidence = min(0.7, 0.5 + (coverage * 0.2))
        else:
            case_strength = "Weak"
            confidence = min(0.5, 0.2 + (coverage * 0.3))
        
        return case_strength, round(confidence, 2)
    
    @staticmethod
    def _generate_reasoning(applied_rules: List[str], case_strength: str, total_rules: int) -> str:
        """Generate reasoning text for the case assessment."""
        rules_count = len(applied_rules)
        
        if rules_count == 0:
            return "No applicable rules found. Case assessment is inconclusive based on available playbook rules."
        
        strength_desc = {
            "Strong": "strong prospects for success",
            "Moderate": "moderate prospects with reasonable chance of success", 
            "Weak": "limited prospects requiring careful consideration"
        }
        
        return (f"Case shows {strength_desc.get(case_strength, 'uncertain prospects')} "
                f"based on {rules_count} applicable rule{'s' if rules_count != 1 else ''} "
                f"out of {total_rules} total rules in the playbook. "
                f"The analysis indicates this is a {case_strength.lower()} case with "
                f"{'significant' if case_strength == 'Strong' else 'some' if case_strength == 'Moderate' else 'limited'} "
                f"supporting factors.")
    
    @staticmethod
    def _generate_strategic_recommendations(playbook_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations from playbook results."""
        recommendations = []
        case_strength = playbook_result.get('case_strength', 'Weak')
        applied_rules = playbook_result.get('applied_rules', [])
        
        # Base recommendations on case strength
        if case_strength == "Strong":
            recommendations.extend([
                {
                    "id": "pursue_full_damages",
                    "title": "Pursue Full Compensatory Damages",
                    "description": "Strong case merits pursuing maximum available damages",
                    "priority": "High",
                    "rationale": "High likelihood of success supports aggressive approach",
                    "supporting_precedents": ["Strong legal position", "Clear rule violations"]
                },
                {
                    "id": "consider_injunctive_relief",
                    "title": "Consider Injunctive Relief",
                    "description": "Seek court orders to prevent ongoing harm",
                    "priority": "Medium",
                    "rationale": "Strong case position supports equitable remedies",
                    "supporting_precedents": ["Ongoing harm prevention", "Court intervention justified"]
                }
            ])
        elif case_strength == "Moderate":
            recommendations.extend([
                {
                    "id": "negotiate_settlement",
                    "title": "Negotiate Favorable Settlement",
                    "description": "Reasonable prospects support settlement negotiations",
                    "priority": "High",
                    "rationale": "Moderate case strength suggests settlement may be optimal",
                    "supporting_precedents": ["Risk mitigation", "Cost-effective resolution"]
                },
                {
                    "id": "gather_additional_evidence",
                    "title": "Strengthen Evidence Base",
                    "description": "Collect additional supporting documentation and testimony",
                    "priority": "Medium",
                    "rationale": "Additional evidence could strengthen case position",
                    "supporting_precedents": ["Evidence strengthening", "Case improvement potential"]
                }
            ])
        else:  # Weak
            recommendations.extend([
                {
                    "id": "assess_settlement_options",
                    "title": "Explore Settlement Options",
                    "description": "Consider early settlement to minimize risks and costs",
                    "priority": "High",
                    "rationale": "Limited prospects suggest settlement may be preferable to litigation",
                    "supporting_precedents": ["Risk management", "Cost containment"]
                },
                {
                    "id": "advise_client_risks",
                    "title": "Advise Client of Litigation Risks",
                    "description": "Ensure client understands potential adverse outcomes",
                    "priority": "High",
                    "rationale": "Professional duty to inform client of case weaknesses",
                    "supporting_precedents": ["Client counseling", "Risk disclosure"]
                }
            ])
        
        # Add rule-specific recommendations
        for rule_id in applied_rules:
            if 'termination' in rule_id.lower():
                recommendations.append({
                    "id": "document_termination_circumstances",
                    "title": "Document Termination Circumstances",
                    "description": "Gather comprehensive documentation of termination events",
                    "priority": "Medium",
                    "rationale": "Termination cases require detailed factual record",
                    "supporting_precedents": ["Employment law requirements", "Factual documentation"]
                })
            elif 'breach' in rule_id.lower():
                recommendations.append({
                    "id": "analyze_contract_terms",
                    "title": "Analyze Contract Terms and Performance",
                    "description": "Detailed review of contract obligations and performance",
                    "priority": "Medium",
                    "rationale": "Contract breach cases require thorough contract analysis",
                    "supporting_precedents": ["Contract interpretation", "Performance standards"]
                })
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    @staticmethod
    def _get_relevant_precedents(case_type: str) -> List[Dict[str, Any]]:
        """Get relevant legal precedents based on case type."""
        # This would typically query the legal corpus, but for now return mock data
        precedents = []
        
        if "Employment" in case_type:
            precedents.extend([
                {
                    "id": "employment_precedent_1",
                    "title": "Employment Rights Act 1996 - Unfair Dismissal",
                    "category": "statutes",
                    "relevance": "Primary legislation governing employment termination",
                    "key_principle": "Employees have right not to be unfairly dismissed"
                },
                {
                    "id": "employment_precedent_2", 
                    "title": "Equality Act 2010 - Discrimination Protection",
                    "category": "statutes",
                    "relevance": "Protection against workplace discrimination",
                    "key_principle": "Prohibition of discrimination based on protected characteristics"
                }
            ])
        elif "Contract" in case_type:
            precedents.extend([
                {
                    "id": "contract_precedent_1",
                    "title": "Sale of Goods Act 1979 - Contract Performance",
                    "category": "statutes", 
                    "relevance": "Fundamental contract law principles",
                    "key_principle": "Contracts must be performed according to their terms"
                },
                {
                    "id": "contract_precedent_2",
                    "title": "Unfair Contract Terms Act 1977 - Term Validity",
                    "category": "statutes",
                    "relevance": "Regulation of unfair contract terms",
                    "key_principle": "Certain contract terms may be unenforceable if unfair"
                }
            ])
        elif "Intellectual Property" in case_type:
            precedents.extend([
                {
                    "id": "ip_precedent_1",
                    "title": "Copyright, Designs and Patents Act 1988",
                    "category": "statutes",
                    "relevance": "Intellectual property protection framework",
                    "key_principle": "Protection of creative works and inventions"
                }
            ])
        
        return precedents
    
    @staticmethod
    def _generate_fallback_analysis(case_id: str, reason: str) -> Dict[str, Any]:
        """Generate fallback analysis when no playbook matches."""
        return {
            "case_id": case_id,
            "case_strength_assessment": {
                "overall_strength": "Unknown",
                "confidence_level": 0.1,
                "key_strengths": [],
                "potential_weaknesses": [reason],
                "supporting_evidence": []
            },
            "strategic_recommendations": [
                {
                    "id": "general_legal_review",
                    "title": "Conduct General Legal Review",
                    "description": "Perform comprehensive legal analysis without specialized playbook",
                    "priority": "High",
                    "rationale": "No specific playbook available for this case type",
                    "supporting_precedents": ["General legal principles"]
                },
                {
                    "id": "consult_specialist",
                    "title": "Consult Subject Matter Expert",
                    "description": "Seek advice from specialist in relevant area of law",
                    "priority": "Medium",
                    "rationale": "Specialized expertise may be required",
                    "supporting_precedents": ["Professional consultation"]
                }
            ],
            "relevant_precedents": [],
            "applied_playbook": None,
            "analysis_timestamp": datetime.now().isoformat(),
            "fallback_reason": reason
        }
