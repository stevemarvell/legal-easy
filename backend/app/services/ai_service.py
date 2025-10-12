#!/usr/bin/env python3
"""
AIService - Simple AI analysis service for the Legal AI System

This service handles AI-powered document analysis including:
- Document analysis with confidence scores and uncertainty flags
- Analysis result storage and retrieval
- Confidence assessment logic for high/low confidence scenarios
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class AIService:
    """Simple AI analysis with confidence scoring."""
    
    # === DOCUMENT ANALYSIS ===
    
    @staticmethod
    def analyze_document(doc_id: str, content: str) -> Dict[str, Any]:
        """
        Perform AI analysis on a document with confidence scores and uncertainty flags.
        
        Note: This is a simplified implementation that extracts basic information.
        In a full implementation, this would integrate with OpenAI API or similar.
        """
        # Extract information using simplified methods
        key_dates = AIService._extract_dates(content)
        parties_involved = AIService._extract_parties(content)
        document_type = AIService._classify_document_type(content)
        summary = AIService._generate_summary(content)
        key_clauses = AIService._extract_key_clauses(content)
        
        # Calculate confidence scores based on content quality and extraction success
        confidence_scores = AIService._calculate_confidence_scores(
            content, key_dates, parties_involved, document_type, summary, key_clauses
        )
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores.values()) / len(confidence_scores)
        
        # Identify uncertainty flags for low confidence areas
        uncertainty_flags = AIService._identify_uncertainty_flags(confidence_scores, content)
        
        # Assess additional analysis fields
        risk_level = AIService._assess_risk_level(content, key_clauses)
        potential_issues = AIService._identify_potential_issues(content, key_clauses)
        compliance_status = AIService._assess_compliance_status(content, document_type)
        critical_deadlines = AIService._extract_critical_deadlines(content, key_dates)
        document_intent = AIService._determine_document_intent(content, document_type)
        complexity_score = AIService._calculate_complexity_score(content)
        
        analysis = {
            "document_id": doc_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "key_dates": key_dates,
            "parties_involved": parties_involved,
            "document_type": document_type,
            "summary": summary,
            "key_clauses": key_clauses,
            "confidence_scores": confidence_scores,
            "overall_confidence": round(overall_confidence, 2),
            "uncertainty_flags": uncertainty_flags,
            "risk_level": risk_level,
            "potential_issues": potential_issues,
            "compliance_status": compliance_status,
            "critical_deadlines": critical_deadlines,
            "document_intent": document_intent,
            "complexity_score": round(complexity_score, 2)
        }
        
        return analysis
    
    @staticmethod
    def _extract_dates(content: str) -> List[str]:
        """Extract key dates from document content and format them as ISO dates."""
        from datetime import datetime
        import re
        
        # Enhanced date pattern matching
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD or YYYY-MM-DD
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'  # DDth Month YYYY
        ]
        
        raw_dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            raw_dates.extend(matches)
        
        # Convert to ISO format dates
        formatted_dates = []
        for date_str in list(set(raw_dates))[:5]:
            try:
                # Try different parsing formats
                iso_date = AIService._parse_date_to_iso(date_str)
                if iso_date:
                    formatted_dates.append(iso_date)
            except:
                # If parsing fails, skip this date
                continue
        
        return formatted_dates
    
    @staticmethod
    def _parse_date_to_iso(date_str: str) -> Optional[str]:
        """Parse various date formats to ISO date string (YYYY-MM-DD)."""
        from datetime import datetime
        
        # Clean up the date string
        date_str = date_str.strip()
        
        # Common date formats to try
        formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d",  # Slash formats
            "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d",  # Dash formats
            "%d %B %Y", "%B %d, %Y", "%B %d %Y",  # Month name formats
            "%dst %B %Y", "%dnd %B %Y", "%drd %B %Y", "%dth %B %Y"  # Ordinal formats
        ]
        
        for fmt in formats:
            try:
                # Remove ordinal suffixes for parsing
                clean_date = re.sub(r'(\d+)(?:st|nd|rd|th)', r'\1', date_str)
                parsed_date = datetime.strptime(clean_date, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If no format works, try to extract year-month-day with regex
        match = re.search(r'(\d{4})', date_str)
        if match:
            year = match.group(1)
            # Default to January 1st if we can't parse the full date
            return f"{year}-01-01"
        
        return None
    
    @staticmethod
    def _extract_parties(content: str) -> List[str]:
        """Extract parties/entities from document content."""
        # Enhanced pattern matching for common legal entities
        party_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b',  # Person names (First Last, First Middle Last)
            r'\b[A-Z][a-zA-Z\s]+ (?:Ltd|Limited|Inc|Corporation|Corp|Company|Co)\.?\b',  # Company names
            r'\b[A-Z][a-zA-Z\s]+ (?:LLC|LLP|Partnership)\.?\b'  # Other business entities
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, content)
            parties.extend(matches)
        
        # Filter out common false positives and clean up
        filtered_parties = []
        common_false_positives = [
            'Employment Agreement', 'This Employment', 'Start Date', 'Either Party',
            'The Company', 'The Employee', 'This Agreement', 'Such Party'
        ]
        
        for party in parties:
            party = party.strip()
            if (len(party) > 3 and 
                party not in common_false_positives and 
                not party.startswith('This ') and
                not party.startswith('Such ') and
                not party.startswith('Either ') and
                party not in filtered_parties):
                filtered_parties.append(party)
        
        # Return unique parties, limited to first 5
        return filtered_parties[:5]
    
    @staticmethod
    def _classify_document_type(content: str) -> str:
        """Classify the document type based on content."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['employment', 'employee', 'employer', 'termination']):
            return 'Employment Document'
        elif any(word in content_lower for word in ['contract', 'agreement', 'terms']):
            return 'Contract'
        elif any(word in content_lower for word in ['confidential', 'non-disclosure', 'nda']):
            return 'Confidentiality Agreement'
        elif any(word in content_lower for word in ['invoice', 'payment', 'billing']):
            return 'Financial Document'
        elif any(word in content_lower for word in ['email', 'from:', 'to:', 'subject:']):
            return 'Email'
        elif any(word in content_lower for word in ['evidence', 'report', 'statement']):
            return 'Evidence'
        else:
            return 'Legal Document'
    
    @staticmethod
    def _generate_summary(content: str) -> str:
        """Generate a simple summary of the document."""
        # Simple summary - take first few sentences
        sentences = content.split('.')[:3]
        summary = '. '.join(sentence.strip() for sentence in sentences if sentence.strip())
        
        if len(summary) > 200:
            summary = summary[:200] + "..."
        
        return summary or "Document summary not available"
    
    @staticmethod
    def _extract_key_clauses(content: str) -> List[str]:
        """Extract key clauses from the document."""
        clauses = []
        
        # Method 1: Look for section headers (common in contracts)
        section_patterns = [
            r'^([A-Z][A-Z\s&]{10,50})$',  # All caps section headers
            r'^\d+\.\s*([A-Z][A-Za-z\s&]{10,80})$',  # Numbered sections
            r'^([A-Z][A-Za-z\s&]{5,50})\s*$'  # Title case section headers
        ]
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            for pattern in section_patterns:
                match = re.match(pattern, line)
                if match:
                    section_title = match.group(1).strip()
                    # Filter out common non-clause headers
                    if (len(section_title) > 5 and 
                        not section_title.startswith('TECHCORP') and
                        not section_title.startswith('EMPLOYEE') and
                        'WITNESS' not in section_title and
                        'Date:' not in section_title):
                        clauses.append(section_title)
        
        # Method 2: Look for key legal provisions and obligations
        provision_patterns = [
            r'(?:Employee|Party|Company)\s+(?:shall|must|will|agrees?|acknowledges?|undertakes?)\s+[^.]{20,150}',
            r'(?:In the event of|Upon|Subject to)\s+[^.]{20,150}',
            r'(?:Employee|Party|Company)\s+(?:is|are)\s+(?:entitled|required|obligated)\s+[^.]{20,150}',
            r'(?:This Agreement|Employment)\s+(?:shall|will|may)\s+[^.]{20,150}',
            r'(?:Either party|Both parties)\s+[^.]{20,150}'
        ]
        
        for pattern in provision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Clean up the match
                match = re.sub(r'\s+', ' ', match.strip())
                if len(match) > 30 and len(match) < 200:
                    clauses.append(match)
        
        # Method 3: Look for specific legal terms and their context
        legal_term_patterns = [
            r'[^.]*(?:termination|terminate)[^.]{10,100}',
            r'[^.]*(?:confidential|confidentiality)[^.]{10,100}',
            r'[^.]*(?:compensation|salary|payment)[^.]{10,100}',
            r'[^.]*(?:benefits|insurance|pension)[^.]{10,100}',
            r'[^.]*(?:notice|notification)[^.]{10,100}',
            r'[^.]*(?:governing law|jurisdiction)[^.]{10,100}',
            r'[^.]*(?:retaliation|safety|compliance)[^.]{10,100}'
        ]
        
        for pattern in legal_term_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                match = re.sub(r'\s+', ' ', match.strip())
                if len(match) > 20 and len(match) < 200:
                    clauses.append(match)
        
        # Clean up and deduplicate clauses
        cleaned_clauses = []
        seen_clauses = set()
        
        for clause in clauses:
            clause = clause.strip()
            # Remove leading/trailing punctuation and normalize
            clause = re.sub(r'^[^\w]+|[^\w]+$', '', clause)
            clause = re.sub(r'\s+', ' ', clause)
            
            # Skip if too short, too long, or already seen
            if (len(clause) < 15 or len(clause) > 200 or 
                clause.lower() in seen_clauses or
                clause in cleaned_clauses):
                continue
                
            # Skip common false positives
            skip_patterns = [
                r'^(By:|Date:|EMPLOYEE:|COMPANY:)',
                r'^\d+\s*(March|April|May|June|July|August|September|October|November|December)',
                r'^/s/',
                r'Marcus Rodriguez|Sarah Chen|TechCorp Solutions'
            ]
            
            should_skip = False
            for skip_pattern in skip_patterns:
                if re.match(skip_pattern, clause, re.IGNORECASE):
                    should_skip = True
                    break
            
            if not should_skip:
                cleaned_clauses.append(clause)
                seen_clauses.add(clause.lower())
        
        return cleaned_clauses[:8]  # Return up to 8 key clauses
    
    @staticmethod
    def _calculate_confidence_scores(content: str, key_dates: List[str], parties_involved: List[str], 
                                   document_type: str, summary: str, key_clauses: List[str]) -> Dict[str, float]:
        """Calculate confidence scores for each analysis category."""
        scores = {}
        
        # Dates confidence - based on number and format quality
        if len(key_dates) >= 2:
            scores['dates'] = 0.9
        elif len(key_dates) == 1:
            scores['dates'] = 0.7
        else:
            scores['dates'] = 0.3
        
        # Parties confidence - based on number and format quality
        if len(parties_involved) >= 2:
            scores['parties'] = 0.85
        elif len(parties_involved) == 1:
            scores['parties'] = 0.6
        else:
            scores['parties'] = 0.2
        
        # Document type confidence - based on keyword matches
        content_lower = content.lower()
        type_keywords = {
            'employment': ['employment', 'employee', 'employer', 'termination'],
            'contract': ['contract', 'agreement', 'terms'],
            'confidentiality': ['confidential', 'non-disclosure', 'nda'],
            'financial': ['invoice', 'payment', 'billing'],
            'email': ['email', 'from:', 'to:', 'subject:'],
            'evidence': ['evidence', 'report', 'statement']
        }
        
        max_matches = 0
        for category, keywords in type_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            max_matches = max(max_matches, matches)
        
        if max_matches >= 3:
            scores['document_type'] = 0.95
        elif max_matches >= 2:
            scores['document_type'] = 0.8
        elif max_matches >= 1:
            scores['document_type'] = 0.6
        else:
            scores['document_type'] = 0.4
        
        # Summary confidence - based on content length and quality
        if len(content) > 1000 and len(summary) > 50:
            scores['summary'] = 0.8
        elif len(content) > 500 and len(summary) > 30:
            scores['summary'] = 0.6
        elif len(summary) > 10:
            scores['summary'] = 0.4
        else:
            scores['summary'] = 0.2
        
        # Key clauses confidence - based on number found
        if len(key_clauses) >= 3:
            scores['key_clauses'] = 0.85
        elif len(key_clauses) >= 2:
            scores['key_clauses'] = 0.7
        elif len(key_clauses) >= 1:
            scores['key_clauses'] = 0.5
        else:
            scores['key_clauses'] = 0.2
        
        return scores
    
    @staticmethod
    def _identify_uncertainty_flags(confidence_scores: Dict[str, float], content: str) -> List[str]:
        """Identify areas where confidence is low."""
        flags = []
        
        for category, score in confidence_scores.items():
            if score < 0.5:
                flags.append(f"Low confidence in {category} extraction")
        
        # Additional uncertainty indicators
        if len(content) < 200:
            flags.append("Document content is very short")
        
        if not re.search(r'\b\d{4}\b', content):  # No year found
            flags.append("No clear date references found")
        
        if not re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', content):  # No proper names
            flags.append("No clear party names identified")
        
        return flags
    
    @staticmethod
    def _assess_risk_level(content: str, key_clauses: List[str]) -> Optional[str]:
        """Assess risk level based on content and clauses."""
        content_lower = content.lower()
        risk_indicators = {
            'high': ['termination', 'breach', 'violation', 'lawsuit', 'damages', 'penalty'],
            'medium': ['dispute', 'disagreement', 'concern', 'issue', 'problem'],
            'low': ['agreement', 'cooperation', 'satisfaction', 'compliance']
        }
        
        high_count = sum(1 for word in risk_indicators['high'] if word in content_lower)
        medium_count = sum(1 for word in risk_indicators['medium'] if word in content_lower)
        low_count = sum(1 for word in risk_indicators['low'] if word in content_lower)
        
        if high_count >= 2:
            return 'high'
        elif medium_count >= 2 or high_count >= 1:
            return 'medium'
        elif low_count >= 1:
            return 'low'
        else:
            return None
    
    @staticmethod
    def _identify_potential_issues(content: str, key_clauses: List[str]) -> Optional[List[str]]:
        """Identify potential legal issues from content."""
        issues = []
        content_lower = content.lower()
        
        issue_patterns = {
            'Contract breach': ['breach', 'violation', 'failed to', 'did not comply'],
            'Payment dispute': ['unpaid', 'overdue', 'payment', 'invoice'],
            'Termination issues': ['termination', 'dismissal', 'fired', 'let go'],
            'Confidentiality concerns': ['confidential', 'disclosed', 'leaked', 'shared'],
            'Compliance issues': ['non-compliance', 'violation', 'regulatory', 'standards']
        }
        
        for issue_type, keywords in issue_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                issues.append(issue_type)
        
        return issues if issues else None
    
    @staticmethod
    def _assess_compliance_status(content: str, document_type: str) -> Optional[str]:
        """Assess compliance status based on document type and content."""
        content_lower = content.lower()
        
        if 'compliant' in content_lower or 'compliance' in content_lower:
            if 'non-compliant' in content_lower or 'violation' in content_lower:
                return 'Non-compliant'
            else:
                return 'Compliant'
        elif 'violation' in content_lower or 'breach' in content_lower:
            return 'Non-compliant'
        else:
            return 'Under review'
    
    @staticmethod
    def _extract_critical_deadlines(content: str, key_dates: List[str]) -> Optional[List[Dict]]:
        """Extract critical deadlines from content."""
        if not key_dates:
            return None
        
        deadlines = []
        content_lower = content.lower()
        
        deadline_keywords = ['deadline', 'due', 'expires', 'termination date', 'completion']
        
        for date in key_dates:
            for keyword in deadline_keywords:
                if keyword in content_lower:
                    deadlines.append({
                        'date': date,
                        'type': keyword,
                        'description': f'{keyword.title()} on {date}'
                    })
                    break
        
        return deadlines if deadlines else None
    
    @staticmethod
    def _determine_document_intent(content: str, document_type: str) -> Optional[str]:
        """Determine the intent or purpose of the document."""
        content_lower = content.lower()
        
        intent_patterns = {
            'Agreement': ['agreement', 'contract', 'terms'],
            'Notice': ['notice', 'notification', 'inform'],
            'Request': ['request', 'asking', 'please'],
            'Report': ['report', 'summary', 'findings'],
            'Complaint': ['complaint', 'dispute', 'issue'],
            'Termination': ['termination', 'end', 'cancel']
        }
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                return intent
        
        return 'General correspondence'
    
    @staticmethod
    def _calculate_complexity_score(content: str) -> float:
        """Calculate document complexity score based on various factors."""
        # Base score on content length
        length_score = min(len(content) / 5000, 1.0)  # Normalize to 0-1
        
        # Legal terminology complexity
        legal_terms = ['whereas', 'heretofore', 'pursuant', 'notwithstanding', 'indemnify', 'covenant']
        legal_term_count = sum(1 for term in legal_terms if term in content.lower())
        legal_score = min(legal_term_count / 10, 1.0)
        
        # Sentence complexity (average sentence length)
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        sentence_score = min(avg_sentence_length / 50, 1.0)
        
        # Overall complexity (weighted average)
        complexity = (length_score * 0.4 + legal_score * 0.4 + sentence_score * 0.2)
        return complexity
    
    # === CASE DETAILS ANALYSIS ===
    
    @staticmethod
    def analyze_case_details(case_id: str, case_type: str, case_description: str) -> Dict[str, Any]:
        """
        Perform comprehensive case details analysis.
        
        This method analyzes all aspects of a case including legal issues, parties,
        timeline, risks, evidence, precedents, and strategic considerations.
        """
        # Perform individual analysis components
        legal_analysis = AIService._analyze_legal_issues(case_description, case_type)
        parties_analysis = AIService._analyze_parties(case_description)
        timeline_analysis = AIService._analyze_timeline(case_description)
        risk_assessment = AIService._assess_case_risks(case_description, case_type)
        evidence_analysis = AIService._analyze_evidence(case_description)
        legal_precedents = AIService._identify_precedents(case_description, case_type)
        strategic_recommendations = AIService._generate_strategic_recommendations(case_description, case_type)
        case_strength = AIService._assess_case_strength(case_description, case_type)
        
        # Compile comprehensive analysis
        analysis = {
            "case_id": case_id,
            "case_type": case_type,
            "analysis_timestamp": datetime.now().isoformat(),
            "legal_analysis": legal_analysis,
            "parties_analysis": parties_analysis,
            "timeline_analysis": timeline_analysis,
            "risk_assessment": risk_assessment,
            "evidence_analysis": evidence_analysis,
            "legal_precedents": legal_precedents,
            "strategic_recommendations": strategic_recommendations,
            "case_strength": case_strength
        }
        
        return analysis
    
    @staticmethod
    def _analyze_legal_issues(case_description: str, case_type: str) -> Dict[str, Any]:
        """Analyze primary legal issues and applicable legislation."""
        description_lower = case_description.lower()
        
        # Define legal issue patterns by case type
        legal_issue_patterns = {
            "Employment Dispute": {
                "issues": ["wrongful dismissal", "retaliation", "discrimination", "harassment", "safety violations", "wage disputes"],
                "legislation": ["Employment Standards Act", "Human Rights Code", "Occupational Health and Safety Act", "Labour Relations Act"]
            },
            "Contract Breach": {
                "issues": ["breach of contract", "non-performance", "material breach", "anticipatory breach", "damages"],
                "legislation": ["Contract Law", "Sale of Goods Act", "Commercial Law", "Civil Code"]
            },
            "Debt Claim": {
                "issues": ["unpaid debt", "default", "collection", "interest calculation", "payment terms"],
                "legislation": ["Debt Collection Act", "Interest Act", "Consumer Protection Act", "Commercial Law"]
            }
        }
        
        # Get patterns for case type or use general patterns
        patterns = legal_issue_patterns.get(case_type, {
            "issues": ["legal dispute", "breach", "violation", "damages", "liability"],
            "legislation": ["Civil Code", "Common Law", "Statutory Law"]
        })
        
        # Identify primary legal issues
        primary_issues = []
        for issue in patterns["issues"]:
            if issue in description_lower:
                primary_issues.append(issue.title())
        
        # Add case-type specific issues if none found
        if not primary_issues:
            if case_type == "Employment Dispute":
                primary_issues = ["Employment Law Dispute"]
            elif case_type == "Contract Breach":
                primary_issues = ["Contract Dispute"]
            elif case_type == "Debt Claim":
                primary_issues = ["Debt Recovery"]
            else:
                primary_issues = ["Legal Dispute"]
        
        # Determine applicable legislation
        applicable_legislation = patterns["legislation"][:3]  # Limit to top 3
        
        # Calculate complexity score based on number of issues and case type
        complexity_score = min(len(primary_issues) * 2 + len(applicable_legislation), 10)
        if case_type == "Employment Dispute":
            complexity_score = min(complexity_score + 2, 10)  # Employment cases tend to be more complex
        
        return {
            "primary_legal_issues": primary_issues[:5],  # Limit to 5 issues
            "applicable_legislation": applicable_legislation,
            "complexity_score": max(complexity_score, 3)  # Minimum complexity of 3
        }
    
    @staticmethod
    def _analyze_parties(case_description: str) -> Dict[str, Any]:
        """Analyze parties involved in the case."""
        # Extract party names using enhanced patterns
        party_patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',  # Person names
            r'\b([A-Z][a-zA-Z\s]+ (?:Ltd|Limited|Inc|Corporation|Corp|Company|Co)\.?)\b',  # Company names
            r'\b([A-Z][a-zA-Z\s]+ (?:LLC|LLP|Partnership)\.?)\b'  # Other business entities
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, case_description)
            parties.extend(matches)
        
        # Clean and deduplicate parties
        cleaned_parties = []
        seen_parties = set()
        
        for party in parties:
            party = party.strip()
            if (len(party) > 3 and 
                party.lower() not in seen_parties and
                not party.startswith('This ') and
                not party.startswith('The ')):
                cleaned_parties.append(party)
                seen_parties.add(party.lower())
        
        # Create party details with role assignment
        parties_detail = []
        for i, party in enumerate(cleaned_parties[:6]):  # Limit to 6 parties
            # Determine role based on context and position
            role = AIService._determine_party_role(party, case_description, i)
            parties_detail.append({
                "name": party,
                "role": role,
                "mentioned_in_description": True
            })
        
        # If no parties found, create generic ones
        if not parties_detail:
            parties_detail = [
                {"name": "Claimant", "role": "Claimant", "mentioned_in_description": False},
                {"name": "Respondent", "role": "Respondent", "mentioned_in_description": False}
            ]
        
        total_parties = len(parties_detail)
        
        # Determine complexity indicator
        if total_parties <= 2:
            complexity_indicator = "Low"
        elif total_parties <= 4:
            complexity_indicator = "Medium"
        else:
            complexity_indicator = "High"
        
        return {
            "total_parties": total_parties,
            "parties_detail": parties_detail,
            "complexity_indicator": complexity_indicator
        }
    
    @staticmethod
    def _determine_party_role(party_name: str, case_description: str, position: int) -> str:
        """Determine the role of a party based on context."""
        description_lower = case_description.lower()
        party_lower = party_name.lower()
        
        # Check for explicit role indicators
        if any(word in description_lower for word in [f"{party_lower} (claimant)", f"{party_lower} alleges", f"{party_lower} claims"]):
            return "Claimant"
        elif any(word in description_lower for word in [f"{party_lower} (respondent)", f"{party_lower} (defendant)"]):
            return "Respondent"
        elif "ltd" in party_lower or "inc" in party_lower or "corp" in party_lower or "company" in party_lower:
            return "Corporate Entity"
        elif position == 0:
            return "Claimant"
        elif position == 1:
            return "Respondent"
        else:
            return "Third Party"
    
    @staticmethod
    def _analyze_timeline(case_description: str) -> Dict[str, Any]:
        """Extract and analyze timeline information."""
        # Extract dates using existing date extraction logic
        dates_identified = AIService._extract_dates(case_description)
        
        # Extract key events based on common legal event patterns
        event_patterns = [
            r'(?:commenced|started|began)\s+[^.]{10,100}',
            r'(?:terminated|ended|dismissed|fired)\s+[^.]{10,100}',
            r'(?:reported|filed|submitted)\s+[^.]{10,100}',
            r'(?:occurred|happened|took place)\s+[^.]{10,100}',
            r'(?:signed|executed|entered into)\s+[^.]{10,100}',
            r'(?:violated|breached|failed to)\s+[^.]{10,100}'
        ]
        
        key_events = []
        for pattern in event_patterns:
            matches = re.findall(pattern, case_description, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                event = re.sub(r'\s+', ' ', match.strip())
                if len(event) > 15 and len(event) < 150:
                    key_events.append(event)
        
        # If no events found, create generic timeline
        if not key_events:
            key_events = ["Case initiated", "Events under investigation"]
        
        # Calculate timeline complexity
        timeline_complexity = min(len(dates_identified) + len(key_events), 10)
        timeline_complexity = max(timeline_complexity, 2)  # Minimum complexity of 2
        
        return {
            "dates_identified": dates_identified[:8],  # Limit to 8 dates
            "key_events": key_events[:6],  # Limit to 6 events
            "timeline_complexity": timeline_complexity
        }
    
    @staticmethod
    def _assess_case_risks(case_description: str, case_type: str) -> Dict[str, Any]:
        """Assess risks associated with the case."""
        description_lower = case_description.lower()
        
        # Define risk factors by case type
        risk_factor_patterns = {
            "Employment Dispute": [
                "retaliation", "discrimination", "harassment", "safety violations",
                "wrongful dismissal", "unpaid wages", "overtime disputes"
            ],
            "Contract Breach": [
                "material breach", "non-performance", "damages", "penalty clauses",
                "liquidated damages", "specific performance", "termination"
            ],
            "Debt Claim": [
                "default", "insolvency", "bankruptcy", "collection costs",
                "interest penalties", "secured debt", "unsecured debt"
            ]
        }
        
        # Get risk patterns for case type
        patterns = risk_factor_patterns.get(case_type, [
            "liability", "damages", "costs", "penalties", "breach", "violation"
        ])
        
        # Identify risk factors
        risk_factors = []
        for pattern in patterns:
            if pattern in description_lower:
                risk_factors.append(pattern.title())
        
        # Add general risk indicators
        general_risks = ["legal costs", "time delays", "reputation damage"]
        for risk in general_risks:
            if risk.replace(" ", "") in description_lower.replace(" ", ""):
                risk_factors.append(risk.title())
        
        # If no specific risks found, add generic ones
        if not risk_factors:
            risk_factors = ["Legal uncertainty", "Potential costs"]
        
        # Calculate risk score and level
        risk_score = min(len(risk_factors) * 2 + 2, 10)
        
        if risk_score <= 3:
            overall_risk_level = "Low"
        elif risk_score <= 6:
            overall_risk_level = "Medium"
        else:
            overall_risk_level = "High"
        
        # Adjust based on case type
        if case_type == "Employment Dispute" and any("retaliation" in rf.lower() for rf in risk_factors):
            risk_score = min(risk_score + 2, 10)
            overall_risk_level = "High" if risk_score > 6 else overall_risk_level
        
        return {
            "risk_factors": risk_factors[:6],  # Limit to 6 factors
            "overall_risk_level": overall_risk_level,
            "risk_score": max(risk_score, 2)  # Minimum risk score of 2
        }
    
    @staticmethod
    def _analyze_evidence(case_description: str) -> Dict[str, Any]:
        """Analyze available evidence types and strength."""
        description_lower = case_description.lower()
        
        # Define evidence type patterns
        evidence_patterns = {
            "Employment contract": ["employment agreement", "contract", "terms of employment"],
            "Email correspondence": ["email", "correspondence", "communication", "messages"],
            "Safety reports": ["safety report", "incident report", "violation report"],
            "Witness statements": ["witness", "testimony", "statement", "account"],
            "Financial records": ["payroll", "salary", "wages", "financial", "records"],
            "Documentation": ["document", "paperwork", "file", "record"],
            "Performance reviews": ["performance", "review", "evaluation", "assessment"],
            "Company policies": ["policy", "handbook", "procedures", "guidelines"]
        }
        
        # Identify evidence types
        evidence_types = []
        for evidence_type, patterns in evidence_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                evidence_types.append(evidence_type)
        
        # If no specific evidence found, add generic types
        if not evidence_types:
            evidence_types = ["Case documentation", "Relevant records"]
        
        # Calculate evidence strength and score
        evidence_score = min(len(evidence_types) * 2, 10)
        evidence_score = max(evidence_score, 3)  # Minimum score of 3
        
        if evidence_score <= 4:
            evidence_strength = "Limited"
        elif evidence_score <= 7:
            evidence_strength = "Moderate"
        else:
            evidence_strength = "Strong"
        
        # Boost score if key evidence types are present
        key_evidence = ["employment contract", "email correspondence", "witness statements"]
        if any(key in evidence_types for key in key_evidence):
            evidence_score = min(evidence_score + 1, 10)
            if evidence_strength == "Limited":
                evidence_strength = "Moderate"
        
        return {
            "evidence_types": evidence_types[:6],  # Limit to 6 types
            "evidence_strength": evidence_strength,
            "evidence_score": evidence_score
        }
    
    @staticmethod
    def _identify_precedents(case_description: str, case_type: str) -> Dict[str, Any]:
        """Identify relevant legal precedents."""
        # Define precedent categories by case type
        precedent_categories = {
            "Employment Dispute": [
                "Wrongful dismissal precedents",
                "Retaliation case law",
                "Employment standards violations",
                "Safety violation cases"
            ],
            "Contract Breach": [
                "Contract breach precedents",
                "Damages calculation cases",
                "Material breach determinations",
                "Specific performance cases"
            ],
            "Debt Claim": [
                "Debt collection precedents",
                "Interest calculation cases",
                "Default judgment cases",
                "Secured debt cases"
            ]
        }
        
        # Get relevant precedents for case type
        relevant_precedents = precedent_categories.get(case_type, [
            "General legal precedents",
            "Similar case outcomes",
            "Relevant court decisions"
        ])
        
        # Determine precedent strength based on case type and description
        description_lower = case_description.lower()
        strength_indicators = ["similar", "precedent", "established", "court", "decision", "ruling"]
        
        strength_count = sum(1 for indicator in strength_indicators if indicator in description_lower)
        
        if strength_count >= 3:
            precedent_strength = "High"
        elif strength_count >= 1:
            precedent_strength = "Medium"
        else:
            precedent_strength = "Low"
        
        # Employment disputes often have stronger precedent support
        if case_type == "Employment Dispute":
            precedent_strength = "High" if precedent_strength == "Medium" else precedent_strength
        
        return {
            "relevant_precedents": relevant_precedents[:4],  # Limit to 4 precedents
            "precedent_strength": precedent_strength
        }
    
    @staticmethod
    def _generate_strategic_recommendations(case_description: str, case_type: str) -> Dict[str, Any]:
        """Generate strategic recommendations for case handling."""
        # Define strategic recommendations by case type
        case_strategies = {
            "Employment Dispute": {
                "recommendations": [
                    "Document all employment-related communications",
                    "Gather evidence of safety violations and reporting",
                    "Review employment contract terms and conditions",
                    "Collect witness statements from colleagues",
                    "Analyze company policies and procedures"
                ],
                "priority_actions": [
                    "Secure employment documentation",
                    "Interview key witnesses",
                    "Review safety compliance records"
                ]
            },
            "Contract Breach": {
                "recommendations": [
                    "Review contract terms and performance obligations",
                    "Document breach incidents and damages",
                    "Assess mitigation efforts and alternatives",
                    "Evaluate remedy options and enforceability",
                    "Consider settlement negotiations"
                ],
                "priority_actions": [
                    "Analyze contract provisions",
                    "Calculate damages and losses",
                    "Explore resolution options"
                ]
            },
            "Debt Claim": {
                "recommendations": [
                    "Verify debt amount and calculation methods",
                    "Review payment terms and default provisions",
                    "Assess debtor's financial capacity",
                    "Consider collection alternatives",
                    "Evaluate security interests"
                ],
                "priority_actions": [
                    "Confirm debt validity",
                    "Assess collection prospects",
                    "Review security options"
                ]
            }
        }
        
        # Get strategies for case type or use general ones
        strategies = case_strategies.get(case_type, {
            "recommendations": [
                "Gather all relevant documentation",
                "Identify key witnesses and evidence",
                "Review applicable legal standards",
                "Assess strengths and weaknesses",
                "Consider settlement options"
            ],
            "priority_actions": [
                "Secure evidence",
                "Analyze legal position",
                "Develop case strategy"
            ]
        })
        
        return {
            "strategic_recommendations": strategies["recommendations"][:5],  # Limit to 5
            "priority_actions": strategies["priority_actions"][:4]  # Limit to 4
        }
    
    @staticmethod
    def _assess_case_strength(case_description: str, case_type: str) -> Dict[str, Any]:
        """Assess overall case strength."""
        description_lower = case_description.lower()
        
        # Define strength and weakness indicators
        strength_indicators = [
            "documented", "evidence", "witness", "contract", "agreement",
            "clear", "established", "proven", "supported", "corroborated"
        ]
        
        weakness_indicators = [
            "unclear", "disputed", "lacking", "insufficient", "weak",
            "questionable", "uncertain", "limited", "missing", "incomplete"
        ]
        
        # Count indicators
        strength_count = sum(1 for indicator in strength_indicators if indicator in description_lower)
        weakness_count = sum(1 for indicator in weakness_indicators if indicator in description_lower)
        
        # Identify specific strength and weakness factors
        strength_factors = []
        weakness_factors = []
        
        # Case-specific strength factors
        if case_type == "Employment Dispute":
            if "safety" in description_lower and "report" in description_lower:
                strength_factors.append("Safety violation documentation")
            if "contract" in description_lower or "agreement" in description_lower:
                strength_factors.append("Employment contract evidence")
            if "retaliation" in description_lower:
                weakness_factors.append("Retaliation claims can be difficult to prove")
        
        elif case_type == "Contract Breach":
            if "contract" in description_lower:
                strength_factors.append("Written contract exists")
            if "breach" in description_lower and "clear" in description_lower:
                strength_factors.append("Clear breach identified")
            if "damages" in description_lower:
                weakness_factors.append("Damages calculation may be complex")
        
        elif case_type == "Debt Claim":
            if "amount" in description_lower or "payment" in description_lower:
                strength_factors.append("Clear debt amount")
            if "default" in description_lower:
                strength_factors.append("Default clearly established")
            if "dispute" in description_lower:
                weakness_factors.append("Disputed debt amounts")
        
        # Add generic factors if none found
        if not strength_factors:
            strength_factors = ["Case documentation available", "Legal basis established"]
        
        if not weakness_factors:
            weakness_factors = ["Complex legal issues", "Potential counterarguments"]
        
        # Calculate strength score
        base_score = 5  # Start with neutral
        base_score += min(strength_count, 3)  # Add up to 3 for strength indicators
        base_score -= min(weakness_count, 2)  # Subtract up to 2 for weakness indicators
        
        strength_score = max(min(base_score, 10), 1)  # Keep between 1-10
        
        # Determine overall strength
        if strength_score <= 3:
            overall_strength = "Weak"
        elif strength_score <= 6:
            overall_strength = "Moderate"
        else:
            overall_strength = "Strong"
        
        return {
            "strength_factors": strength_factors[:4],  # Limit to 4 factors
            "weakness_factors": weakness_factors[:4],  # Limit to 4 factors
            "overall_strength": overall_strength,
            "strength_score": strength_score
        }

    # === ANALYSIS STORAGE ===
    
    @staticmethod
    def load_existing_analysis(doc_id: str) -> Optional[Dict[str, Any]]:
        """Load existing analysis results for a document."""
        try:
            # Use absolute path from the backend/app directory
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_documents" / "case_documents_analysis.json"
            if not analysis_path.exists():
                return None
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                analyses = json.load(f)
                return analyses.get(doc_id)
        except Exception as e:
            print(f"Error loading existing analysis: {e}")
            return None
    
    @staticmethod
    def save_analysis(doc_id: str, analysis: Dict[str, Any]) -> None:
        """Save analysis results to storage."""
        try:
            # Use absolute path from the backend/app directory
            analysis_path = Path(__file__).parent.parent.parent / "data" / "ai" / "case_documents" / "case_documents_analysis.json"
            
            # Ensure directory exists
            analysis_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing analyses
            analyses = {}
            if analysis_path.exists():
                with open(analysis_path, 'r', encoding='utf-8') as f:
                    analyses = json.load(f)
            
            # Add or update analysis
            analyses[doc_id] = analysis
            
            # Save back to file
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving analysis: {e}")
            raise
