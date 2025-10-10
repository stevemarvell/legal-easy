#!/usr/bin/env python3
"""
PlaybookService - Simplified playbook service for the Legal AI System

This service handles all playbook-related operations including:
- Loading and managing playbooks
- Applying playbook rules to cases
- Generating case assessments
- Playbook rule evaluation and scoring
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PlaybookService:
    """Simplified playbook service for case assessment and rule application."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.playbooks_path = self.data_root / "playbooks"
        
        # Ensure playbooks directory exists
        self.playbooks_path.mkdir(parents=True, exist_ok=True)
    
    # === PLAYBOOK MANAGEMENT ===
    
    def get_all_playbooks(self) -> List[Dict[str, Any]]:
        """Get all available playbooks."""
        try:
            playbooks_index_path = self.playbooks_path / "playbooks_index.json"
            if not playbooks_index_path.exists():
                return []
            
            with open(playbooks_index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('playbooks', [])
        except Exception as e:
            print(f"Error loading playbooks: {e}")
            return []
    
    def get_playbook_by_case_type(self, case_type: str) -> Optional[Dict[str, Any]]:
        """Get playbook for a specific case type."""
        playbooks = self.get_all_playbooks()
        for playbook in playbooks:
            if playbook.get('case_type') == case_type:
                return playbook
        return None
    
    def get_playbook_by_id(self, playbook_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific playbook by ID."""
        playbooks = self.get_all_playbooks()
        for playbook in playbooks:
            if playbook.get('id') == playbook_id:
                return playbook
        return None
    
    # === CASE ASSESSMENT ===
    
    def generate_case_assessment(self, case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate AI-powered case assessment using appropriate playbook."""
        case_type = case.get('case_type')
        if not case_type:
            return None
        
        playbook = self.get_playbook_by_case_type(case_type)
        if not playbook:
            return None
        
        # Apply playbook rules to generate assessment
        playbook_result = self.apply_playbook_rules(case, playbook)
        
        # Convert to case assessment format
        assessment = {
            "case_id": case.get('id'),
            "playbook_used": playbook.get('name', 'Unknown Playbook'),
            "case_strength": playbook_result.get('case_strength', 'Unknown'),
            "key_issues": self._extract_key_issues(case, playbook_result),
            "recommended_actions": playbook_result.get('recommendations', []),
            "monetary_assessment": self._calculate_monetary_assessment(playbook, playbook_result),
            "applied_rules": playbook_result.get('applied_rules', []),
            "reasoning": playbook_result.get('reasoning', 'No reasoning available')
        }
        
        return assessment
    
    def apply_playbook_rules(self, case: Dict[str, Any], playbook: Dict[str, Any]) -> Dict[str, Any]:
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
                "case_strength": "Unknown",
                "reasoning": "No rules available in playbook"
            }
        
        # Evaluate each rule against the case
        applied_rules = []
        recommendations = []
        total_weight = 0.0
        
        for rule in rules:
            if self._evaluate_rule_condition(case, rule):
                applied_rules.append(rule.get('id', ''))
                
                # Add rule's action as recommendation
                action = rule.get('action')
                if action and action not in recommendations:
                    recommendations.append(action)
                
                # Add rule weight to total
                weight = rule.get('weight', 0.5)
                total_weight += weight
        
        # Calculate case strength based on applied rules
        case_strength = self._calculate_case_strength(total_weight, len(applied_rules))
        
        # Generate reasoning
        reasoning = self._generate_reasoning(applied_rules, case_strength, len(rules))
        
        return {
            "case_id": case_id,
            "playbook_id": playbook_id,
            "applied_rules": applied_rules,
            "recommendations": recommendations,
            "case_strength": case_strength,
            "reasoning": reasoning,
            "total_weight": total_weight,
            "rules_applied_count": len(applied_rules),
            "total_rules_count": len(rules)
        }
    
    def _evaluate_rule_condition(self, case: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """
        Evaluate if a rule condition applies to a case.
        
        This is a simplified implementation. In production, this would use
        more sophisticated rule evaluation logic.
        """
        condition = rule.get('condition', '').lower()
        case_summary = case.get('summary', '').lower()
        case_type = case.get('case_type', '').lower()
        
        # Simple keyword matching for common conditions
        condition_keywords = {
            'termination_within_protected_period': ['termination', 'dismissal', 'fired', 'protected'],
            'harassment_documented': ['harassment', 'bullying', 'discrimination', 'documented'],
            'contract_breach': ['breach', 'violation', 'failed to', 'did not'],
            'safety_violation': ['safety', 'health', 'violation', 'dangerous'],
            'confidentiality_breach': ['confidential', 'disclosure', 'leaked', 'shared'],
            'intellectual_property_dispute': ['intellectual property', 'copyright', 'patent', 'trademark'],
            'payment_dispute': ['payment', 'invoice', 'unpaid', 'overdue'],
            'liability_claim': ['liability', 'damages', 'compensation', 'injury']
        }
        
        # Check if condition keywords appear in case summary
        if condition in condition_keywords:
            keywords = condition_keywords[condition]
            return any(keyword in case_summary for keyword in keywords)
        
        # Fallback: simple substring matching
        return condition in case_summary or condition in case_type
    
    def _calculate_case_strength(self, total_weight: float, rules_count: int) -> str:
        """Calculate case strength based on applied rules and weights."""
        if rules_count == 0:
            return "Weak"
        
        # Normalize weight by number of rules
        average_weight = total_weight / rules_count if rules_count > 0 else 0
        
        if average_weight >= 0.8:
            return "Strong"
        elif average_weight >= 0.6:
            return "Moderate"
        else:
            return "Weak"
    
    def _generate_reasoning(self, applied_rules: List[str], case_strength: str, total_rules: int) -> str:
        """Generate reasoning text for the case assessment."""
        rules_count = len(applied_rules)
        
        if rules_count == 0:
            return f"No applicable rules found. Case assessment is inconclusive based on available playbook rules."
        
        strength_desc = {
            "Strong": "strong prospects",
            "Moderate": "moderate prospects", 
            "Weak": "limited prospects"
        }
        
        return (f"Case shows {strength_desc.get(case_strength, 'uncertain prospects')} "
                f"based on {rules_count} applicable rule{'s' if rules_count != 1 else ''} "
                f"out of {total_rules} total rules. "
                f"Key factors support the client's position in this {case_strength.lower()} case matter.")
    
    def _extract_key_issues(self, case: Dict[str, Any], playbook_result: Dict[str, Any]) -> List[str]:
        """Extract key legal issues from case and playbook results."""
        issues = []
        
        # Extract from case type
        case_type = case.get('case_type', '')
        if 'Employment' in case_type:
            issues.append('Employment law matter')
        if 'Contract' in case_type:
            issues.append('Contract dispute')
        
        # Extract from applied rules (simplified)
        applied_rules = playbook_result.get('applied_rules', [])
        for rule_id in applied_rules:
            if 'termination' in rule_id.lower():
                issues.append('Wrongful termination claim')
            elif 'harassment' in rule_id.lower():
                issues.append('Workplace harassment')
            elif 'breach' in rule_id.lower():
                issues.append('Contract breach')
            elif 'discrimination' in rule_id.lower():
                issues.append('Discrimination claim')
        
        # Add generic issue if none found
        if not issues:
            issues.append('Legal dispute requiring assessment')
        
        return issues[:5]  # Limit to 5 key issues
    
    def _calculate_monetary_assessment(self, playbook: Dict[str, Any], playbook_result: Dict[str, Any]) -> List[int]:
        """Calculate monetary assessment range based on case strength."""
        case_strength = playbook_result.get('case_strength', 'Weak')
        
        # Get monetary ranges from playbook
        monetary_ranges = playbook.get('monetary_ranges', {})
        
        # Default ranges if not specified in playbook
        default_ranges = {
            "Strong": [100000, 500000],
            "Moderate": [50000, 200000],
            "Weak": [10000, 75000]
        }
        
        # Use playbook ranges if available, otherwise use defaults
        if case_strength.lower() in monetary_ranges:
            range_data = monetary_ranges[case_strength.lower()]
            if isinstance(range_data, dict) and 'range' in range_data:
                return range_data['range']
        
        return default_ranges.get(case_strength, [10000, 50000])
    
    # === PLAYBOOK STATISTICS ===
    
    def get_playbook_statistics(self) -> Dict[str, Any]:
        """Get statistics about all playbooks."""
        playbooks = self.get_all_playbooks()
        
        stats = {
            "total_playbooks": len(playbooks),
            "case_types": [],
            "total_rules": 0,
            "playbook_details": []
        }
        
        for playbook in playbooks:
            case_type = playbook.get('case_type')
            if case_type:
                stats["case_types"].append(case_type)
            
            rules = playbook.get('rules', [])
            stats["total_rules"] += len(rules)
            
            stats["playbook_details"].append({
                "id": playbook.get('id'),
                "name": playbook.get('name'),
                "case_type": case_type,
                "rules_count": len(rules)
            })
        
        return stats
    
    # === UTILITY METHODS ===
    
    def validate_playbook(self, playbook: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a playbook structure and content."""
        validation_result = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check required fields
        required_fields = ['id', 'name', 'case_type']
        for field in required_fields:
            if not playbook.get(field):
                validation_result["valid"] = False
                validation_result["issues"].append(f"Missing required field: {field}")
        
        # Check rules structure
        rules = playbook.get('rules', [])
        if not rules:
            validation_result["warnings"].append("Playbook has no rules defined")
        else:
            for i, rule in enumerate(rules):
                if not rule.get('id'):
                    validation_result["issues"].append(f"Rule {i} missing ID")
                    validation_result["valid"] = False
                
                if not rule.get('condition'):
                    validation_result["issues"].append(f"Rule {rule.get('id', i)} missing condition")
                    validation_result["valid"] = False
                
                if not rule.get('action'):
                    validation_result["issues"].append(f"Rule {rule.get('id', i)} missing action")
                    validation_result["valid"] = False
        
        return validation_result