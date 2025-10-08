import json
import os
from typing import List, Optional, Dict, Any
from app.models.playbook import Playbook, PlaybookResult, PlaybookRule, CaseAssessment
from app.models.case import Case


class PlaybookEngine:
    """Engine for applying case-specific playbooks"""
    
    def __init__(self):
        """Initialize the playbook engine with demo data"""
        self._playbooks: Dict[str, Playbook] = {}
        self._load_demo_playbooks()
    
    def _load_demo_playbooks(self) -> None:
        """Load demo playbooks from JSON file"""
        try:
            playbooks_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'demo_playbooks.json')
            with open(playbooks_file, 'r', encoding='utf-8') as f:
                playbooks_data = json.load(f)
            
            for playbook_data in playbooks_data:
                # Convert rules data to PlaybookRule objects
                rules = [
                    PlaybookRule(
                        id=rule['id'],
                        condition=rule['condition'],
                        action=rule['action'],
                        weight=rule['weight'],
                        description=rule['description']
                    )
                    for rule in playbook_data['rules']
                ]
                
                # Convert monetary ranges to MonetaryRange objects
                from app.models.playbook import MonetaryRange
                monetary_ranges = {}
                for key, range_data in playbook_data['monetary_ranges'].items():
                    monetary_ranges[key] = MonetaryRange(
                        range=range_data['range'],
                        description=range_data['description'],
                        factors=range_data['factors']
                    )
                
                # Create Playbook object
                playbook = Playbook(
                    id=playbook_data['id'],
                    case_type=playbook_data['case_type'],
                    name=playbook_data['name'],
                    rules=rules,
                    decision_tree=playbook_data['decision_tree'],
                    monetary_ranges=monetary_ranges,
                    escalation_paths=[step['action'] for step in playbook_data['escalation_paths']]
                )
                
                self._playbooks[playbook_data['case_type']] = playbook
                
        except FileNotFoundError:
            print("Warning: Demo playbooks file not found")
        except Exception as e:
            print(f"Error loading demo playbooks: {e}")
    
    def get_playbook_by_case_type(self, case_type: str) -> Optional[Playbook]:
        """Get playbook for specific case type"""
        return self._playbooks.get(case_type)
    
    def get_all_playbooks(self) -> List[Playbook]:
        """Get all available playbooks"""
        return list(self._playbooks.values())
    
    def apply_playbook_rules(self, case: Case, playbook: Playbook) -> PlaybookResult:
        """Apply playbook rules to a case and generate assessment"""
        applied_rules = []
        recommendations = []
        total_weight = 0.0
        
        # Simulate rule application based on case data
        # In a real implementation, this would analyze case facts against rule conditions
        for rule in playbook.rules:
            # For demo purposes, apply rules based on simple heuristics
            if self._should_apply_rule(case, rule):
                applied_rules.append(rule.id)
                recommendations.append(rule.action)
                total_weight += rule.weight
        
        # Determine case strength based on applied rules and weights
        case_strength = self._calculate_case_strength(total_weight, len(applied_rules))
        
        # Generate reasoning
        reasoning = self._generate_reasoning(case, applied_rules, case_strength)
        
        return PlaybookResult(
            case_id=case.id,
            playbook_id=playbook.id,
            applied_rules=applied_rules,
            recommendations=recommendations,
            case_strength=case_strength,
            reasoning=reasoning
        )
    
    def generate_case_assessment(self, case: Case) -> Optional[CaseAssessment]:
        """Generate complete case assessment using appropriate playbook"""
        playbook = self.get_playbook_by_case_type(case.case_type)
        if not playbook:
            return None
        
        playbook_result = self.apply_playbook_rules(case, playbook)
        
        # Extract key issues based on case type
        key_issues = self._extract_key_issues(case, playbook)
        
        # Get monetary assessment based on case strength
        monetary_assessment = self._get_monetary_assessment(playbook, playbook_result.case_strength)
        
        return CaseAssessment(
            case_id=case.id,
            playbook_used=playbook.name,
            case_strength=playbook_result.case_strength,
            key_issues=key_issues,
            recommended_actions=playbook_result.recommendations,
            monetary_assessment=monetary_assessment,
            applied_rules=playbook_result.applied_rules,
            reasoning=playbook_result.reasoning
        )
    
    def evaluate_case_strength(self, case: Case, rules: List[PlaybookRule]) -> str:
        """Evaluate case strength based on applied rules"""
        if not rules:
            return "Weak"
        
        total_weight = sum(rule.weight for rule in rules)
        avg_weight = total_weight / len(rules)
        
        if avg_weight >= 0.8:
            return "Strong"
        elif avg_weight >= 0.6:
            return "Moderate"
        else:
            return "Weak"
    
    def _should_apply_rule(self, case: Case, rule: PlaybookRule) -> bool:
        """Determine if a rule should be applied to a case (simplified logic for demo)"""
        # This is simplified demo logic. In a real system, this would parse
        # rule conditions and evaluate them against case facts
        
        case_type_lower = case.case_type.lower()
        condition_lower = rule.condition.lower()
        
        # Employment dispute rules
        if case_type_lower == "employment dispute":
            if "termination" in condition_lower and "termination" in case.summary.lower():
                return True
            if "age" in condition_lower and "age" in case.summary.lower():
                return True
            if "retaliation" in condition_lower and "retaliation" in case.summary.lower():
                return True
            if "harassment" in condition_lower and "harassment" in case.summary.lower():
                return True
        
        # Contract breach rules
        elif case_type_lower == "contract breach":
            if "contract" in condition_lower and "contract" in case.summary.lower():
                return True
            if "breach" in condition_lower and "breach" in case.summary.lower():
                return True
            if "non_compete" in condition_lower and "non-compete" in case.summary.lower():
                return True
        
        # Debt claim rules
        elif case_type_lower == "debt claim":
            if "debt" in condition_lower and ("debt" in case.summary.lower() or "payment" in case.summary.lower()):
                return True
            if "documentation" in condition_lower:
                return True  # Assume we have documentation for demo cases
        
        # Default: apply rule with 30% probability for demo variety
        import random
        return random.random() < 0.3
    
    def _calculate_case_strength(self, total_weight: float, rule_count: int) -> str:
        """Calculate case strength based on applied rules and weights"""
        if rule_count == 0:
            return "Weak"
        
        avg_weight = total_weight / rule_count
        
        if avg_weight >= 0.8 and rule_count >= 3:
            return "Strong"
        elif avg_weight >= 0.6 and rule_count >= 2:
            return "Moderate"
        else:
            return "Weak"
    
    def _generate_reasoning(self, case: Case, applied_rules: List[str], case_strength: str) -> str:
        """Generate reasoning explanation for the assessment"""
        rule_count = len(applied_rules)
        
        if case_strength == "Strong":
            return f"Case shows strong prospects based on {rule_count} applicable rules. " \
                   f"Key factors support the client's position in this {case.case_type.lower()} matter."
        elif case_strength == "Moderate":
            return f"Case has moderate prospects with {rule_count} applicable rules. " \
                   f"Some factors favor the client, but there may be challenges to address."
        else:
            return f"Case presents challenges with limited supporting factors. " \
                   f"Consider alternative approaches or settlement options."
    
    def _extract_key_issues(self, case: Case, playbook: Playbook) -> List[str]:
        """Extract key issues based on case type and summary"""
        issues = []
        case_summary_lower = case.summary.lower()
        
        if case.case_type == "Employment Dispute":
            if "termination" in case_summary_lower:
                issues.append("Wrongful termination claim")
            if "discrimination" in case_summary_lower:
                issues.append("Discrimination allegations")
            if "retaliation" in case_summary_lower:
                issues.append("Retaliation for protected activity")
            if "harassment" in case_summary_lower:
                issues.append("Workplace harassment")
        
        elif case.case_type == "Contract Breach":
            if "breach" in case_summary_lower:
                issues.append("Material breach of contract")
            if "license" in case_summary_lower:
                issues.append("License agreement violations")
            if "non-compete" in case_summary_lower:
                issues.append("Non-compete agreement enforcement")
        
        elif case.case_type == "Debt Claim":
            if "payment" in case_summary_lower or "debt" in case_summary_lower:
                issues.append("Outstanding payment obligations")
            if "services" in case_summary_lower:
                issues.append("Service delivery disputes")
        
        # Default issues if none detected
        if not issues:
            issues.append(f"General {case.case_type.lower()} matter")
        
        return issues
    
    def _get_monetary_assessment(self, playbook: Playbook, case_strength: str) -> Optional[tuple]:
        """Get monetary assessment range based on case strength"""
        strength_to_range = {
            "Strong": "high",
            "Moderate": "medium", 
            "Weak": "low"
        }
        
        range_key = strength_to_range.get(case_strength, "low")
        monetary_range = playbook.monetary_ranges.get(range_key)
        
        if monetary_range and monetary_range.range:
            return tuple(monetary_range.range)
        
        return None