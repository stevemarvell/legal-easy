import re
import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from app.models.document import Document, DocumentAnalysis, KeyInformation


class DocumentAnalyzer:
    """
    Advanced AI-powered document analysis service for legal document processing.
    
    Features:
    - Multi-layered text analysis with semantic understanding
    - Risk assessment and compliance checking
    - Advanced confidence scoring based on document quality
    - Legal concept extraction with context awareness
    - Temporal analysis for contract lifecycle management
    """
    
    def __init__(self):
        """Initialize the document analyzer with enhanced legal patterns and analysis models"""
        # Enhanced legal keyword taxonomy
        self.legal_keywords = {
            'contract_terms': [
                'agreement', 'contract', 'terms', 'conditions', 'obligations',
                'liability', 'indemnity', 'warranty', 'breach', 'termination',
                'notice', 'payment', 'consideration', 'performance', 'covenant',
                'undertaking', 'representation', 'guarantee', 'assignment'
            ],
            'employment': [
                'employment', 'employee', 'employer', 'salary', 'wages',
                'benefits', 'vacation', 'termination', 'resignation', 'notice',
                'position', 'duties', 'responsibilities', 'performance',
                'probation', 'promotion', 'disciplinary', 'grievance'
            ],
            'legal_concepts': [
                'negligence', 'damages', 'liability', 'breach', 'violation',
                'compliance', 'regulation', 'statute', 'law', 'legal',
                'court', 'jurisdiction', 'dispute', 'claim', 'remedy',
                'precedent', 'jurisprudence', 'tort', 'fiduciary'
            ],
            'risk_indicators': [
                'penalty', 'fine', 'liquidated damages', 'consequential damages',
                'unlimited liability', 'personal guarantee', 'joint and several',
                'indemnification', 'hold harmless', 'waiver', 'release'
            ],
            'compliance_terms': [
                'gdpr', 'data protection', 'privacy', 'confidential', 'proprietary',
                'intellectual property', 'copyright', 'trademark', 'patent',
                'trade secret', 'non-disclosure', 'nda', 'confidentiality'
            ]
        }
        
        # Risk assessment patterns
        self.risk_patterns = {
            'high_risk': [
                r'\bunlimited\s+liability\b',
                r'\bpersonal\s+guarantee\b',
                r'\bjoint\s+and\s+several\b',
                r'\bconsequential\s+damages\b',
                r'\bpunitive\s+damages\b'
            ],
            'medium_risk': [
                r'\bliquidated\s+damages\b',
                r'\bpenalty\b',
                r'\bindemnif\w+\b',
                r'\bhold\s+harmless\b',
                r'\bwaiver\s+of\s+rights\b'
            ],
            'compliance_risk': [
                r'\bdata\s+breach\b',
                r'\bprivacy\s+violation\b',
                r'\bgdpr\s+compliance\b',
                r'\bintellectual\s+property\s+infringement\b'
            ]
        }
        
        # Temporal analysis patterns
        self.temporal_patterns = {
            'deadlines': [
                r'\b(?:within|by|before|no later than)\s+(\d+)\s+(days?|weeks?|months?|years?)\b',
                r'\b(?:deadline|due date|expiry|expiration)\b'
            ],
            'renewal_terms': [
                r'\b(?:renew|renewal|extend|extension)\b',
                r'\b(?:automatic\s+renewal|auto-renew)\b'
            ],
            'notice_periods': [
                r'\b(\d+)\s+(?:days?|weeks?|months?)\s+(?:notice|prior notice)\b'
            ]
        }
        
        # Date patterns for extraction
        self.date_patterns = [
            r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})\b',  # YYYY/MM/DD or YYYY-MM-DD
            r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b',
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b'
        ]
        
        # Amount patterns for financial extraction
        self.amount_patterns = [
            r'[\$£€]\s*[\d,]+(?:\.\d{2})?',  # Currency symbols
            r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars?|pounds?|euros?)\b'  # Written currency
        ]

    def analyze_document(self, document: Document) -> DocumentAnalysis:
        """
        Perform comprehensive AI analysis of a legal document with advanced features
        
        Args:
            document: Document object to analyze
            
        Returns:
            DocumentAnalysis: Complete analysis results with extracted information,
                            risk assessment, and compliance analysis
        """
        # Load full document content if available
        full_content = self._load_document_content(document)
        
        # Core information extraction
        key_dates = self._extract_dates(full_content)
        parties = self._extract_parties(full_content)
        document_type = self._classify_document_type(full_content, document.type)
        
        # Advanced analysis features
        risk_assessment = self._assess_document_risks(full_content, document_type)
        compliance_analysis = self._analyze_compliance(full_content, document_type)
        temporal_analysis = self._analyze_temporal_elements(full_content)
        semantic_analysis = self._perform_semantic_analysis(full_content, document_type)
        
        # Generate enhanced summary and clauses
        summary = self._generate_enhanced_summary(full_content, document_type, risk_assessment)
        key_clauses = self._extract_enhanced_clauses(full_content, document_type, semantic_analysis)
        
        # Calculate advanced confidence scores
        analysis_data = {
            'document_type': document_type,
            'key_clauses': key_clauses,
            'parties': parties,
            'dates': key_dates,
            'risk_assessment': risk_assessment,
            'compliance_analysis': compliance_analysis,
            'semantic_analysis': semantic_analysis
        }
        confidence_scores = self._calculate_confidence_scores(document, analysis_data)
        
        # Prepare critical deadlines from temporal analysis
        critical_deadlines = []
        for deadline in temporal_analysis.get('deadlines', []):
            critical_deadlines.append({
                'type': 'deadline',
                'text': deadline.get('text', ''),
                'context': deadline.get('context', '')
            })
        for notice in temporal_analysis.get('notice_periods', []):
            critical_deadlines.append({
                'type': 'notice_period',
                'period': notice.get('period', 'unspecified'),
                'context': notice.get('context', '')
            })
        
        return DocumentAnalysis(
            document_id=document.id,
            key_dates=key_dates,
            parties_involved=parties,
            document_type=document_type,
            summary=summary,
            key_clauses=key_clauses,
            confidence_scores=confidence_scores,
            risk_level=risk_assessment.get('overall_risk', 'medium'),
            potential_issues=risk_assessment.get('issues', []),
            compliance_status=compliance_analysis.get('status', 'unknown'),
            critical_deadlines=critical_deadlines[:5],  # Limit to top 5 deadlines
            document_intent=semantic_analysis.get('intent', 'unknown'),
            complexity_score=self._calculate_complexity_score(semantic_analysis, len(full_content.split())),
            analysis_timestamp=datetime.now(),
            analysis_version="2.1.0"
        )

    def extract_key_information(self, text: str) -> KeyInformation:
        """
        Extract key information from raw text
        
        Args:
            text: Raw text content to analyze
            
        Returns:
            KeyInformation: Extracted dates, parties, amounts, and legal concepts
        """
        dates = self._extract_dates(text)
        parties = self._extract_parties(text)
        amounts = self._extract_amounts(text)
        legal_concepts = self._extract_legal_concepts(text)
        confidence = self._calculate_extraction_confidence(text, dates, parties, amounts, legal_concepts)
        
        return KeyInformation(
            dates=dates,
            parties=parties,
            amounts=amounts,
            legal_concepts=legal_concepts,
            confidence=confidence
        )

    def _load_document_content(self, document: Document) -> str:
        """Load full document content from file if available, otherwise use preview"""
        try:
            # Check if document has full_content_path
            if document.full_content_path:
                # Try the path as-is first
                if os.path.exists(document.full_content_path):
                    with open(document.full_content_path, 'r', encoding='utf-8') as f:
                        return f.read()
                
                # Try removing 'backend/' prefix if it exists
                if document.full_content_path.startswith('backend/'):
                    corrected_path = document.full_content_path[8:]  # Remove 'backend/'
                    if os.path.exists(corrected_path):
                        with open(corrected_path, 'r', encoding='utf-8') as f:
                            return f.read()
            
            # Try to find content file based on document ID and case ID
            content_dir = os.path.join(os.path.dirname(__file__), "..", "data", "documents")
            case_dir = os.path.join(content_dir, document.case_id)
            
            if os.path.exists(case_dir):
                # Look for files that might match this document
                for filename in os.listdir(case_dir):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(case_dir, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Simple heuristic: if preview matches beginning of file, use it
                            if document.content_preview[:100].lower() in content[:200].lower():
                                return content
            
            # Fallback to content preview
            return document.content_preview
            
        except Exception:
            # Fallback to content preview if file loading fails
            return document.content_preview

    def _extract_dates(self, text: str) -> List[date]:
        """Extract dates from text using regex patterns"""
        dates = []
        
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        if groups[0].isdigit() and groups[1].isdigit() and groups[2].isdigit():
                            # Numeric date format
                            if len(groups[0]) == 4:  # YYYY-MM-DD format
                                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                            else:  # MM-DD-YYYY format
                                month, day, year = int(groups[0]), int(groups[1]), int(groups[2])
                        else:
                            # Month name format
                            month_names = {
                                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                                'september': 9, 'october': 10, 'november': 11, 'december': 12
                            }
                            if groups[1].lower() in month_names:  # Day Month Year
                                day, month, year = int(groups[0]), month_names[groups[1].lower()], int(groups[2])
                            else:  # Month Day Year
                                month, day, year = month_names[groups[0].lower()], int(groups[1]), int(groups[2])
                        
                        if 1 <= month <= 12 and 1 <= day <= 31 and 1900 <= year <= 2100:
                            extracted_date = date(year, month, day)
                            if extracted_date not in dates:
                                dates.append(extracted_date)
                except (ValueError, KeyError):
                    continue
        
        return sorted(dates)

    def _extract_parties(self, text: str) -> List[str]:
        """Extract party names from text using patterns and heuristics"""
        parties = []
        
        # Pattern for company names - more specific to avoid false matches
        company_patterns = [
            r'\b([A-Z][a-zA-Z\s&]{2,30}(?:Ltd|Inc|Corp|LLC|Limited|Corporation|Company|Co\.?))\b',
            r'\b([A-Z][a-zA-Z\s&]{2,30}(?:Solutions|Systems|Technologies|Services|Group|Associates))\b'
        ]
        
        # Enhanced person name patterns for different contexts
        person_patterns = [
            # Formal titles
            r'\b(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Professor)\s+([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\b',
            # Professional titles and signatures
            r'\b([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\s*(?:,\s*(?:General Counsel|Legal Counsel|CEO|Director|Manager|Esq\.?|QC|KC))\b',
            # Email signatures and formal contexts
            r'\b([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\s*\n(?:General Counsel|Legal Counsel|CEO|Director|Manager)',
            # Standard two-word names (more permissive for emails)
            r'\b([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\b'
        ]
        
        # Email-specific patterns for names in email headers
        email_header_patterns = [
            # From/To/CC patterns: "From: name@domain" or "name@domain"
            r'(?:From|To|CC):\s*([a-z]+\.?[a-z]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            # CC with multiple emails: "CC: email1, email2, email3"
            r'CC:.*?([a-z]+\.?[a-z]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            # Email addresses in general
            r'\b([a-z]+\.?[a-z]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        ]
        
        # Extract company names
        for pattern in company_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                party = match.group(1).strip()
                # Filter out common false positives
                if (len(party) > 5 and len(party) < 50 and 
                    party not in parties and
                    not party.startswith('EMPLOYMENT') and
                    not party.startswith('AGREEMENT') and
                    'between' not in party.lower()):
                    parties.append(party)
        
        # Extract person names with enhanced patterns
        for pattern in person_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                party = match.group(1).strip()
                # Enhanced filtering for email contexts and false positives
                if (len(party.split()) == 2 and 
                    party not in parties and
                    len(party) > 5 and len(party) < 40 and
                    not self._is_false_positive_party(party)):
                    parties.append(party)
        
        # Extract names from email addresses
        for pattern in email_header_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                email_name = match.group(1).replace('.', ' ').title()
                if (email_name not in parties and 
                    len(email_name.split()) >= 2 and
                    len(email_name) > 5 and len(email_name) < 30 and
                    not any(word in email_name.lower() for word in ['legal', 'licensing', 'info', 'admin', 'support'])):
                    parties.append(email_name)
        
        # Look for names in email signature blocks
        signature_pattern = r'\n([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\s*\n(?:General Counsel|Legal Counsel|CEO|Director|Manager)'
        signature_matches = re.finditer(signature_pattern, text)
        for match in signature_matches:
            party = match.group(1).strip()
            if party not in parties and len(party) > 5:
                parties.append(party)
        
        # Look for specific "between X and Y" patterns
        between_pattern = r'\bbetween\s+([A-Z][a-zA-Z\s&.]{2,40}?)\s+and\s+([A-Z][a-zA-Z\s&.]{2,40}?)(?:\s|\.|\,)'
        between_matches = re.finditer(between_pattern, text)
        for match in between_matches:
            for i in [1, 2]:
                party = match.group(i).strip()
                if (len(party) > 3 and len(party) < 50 and 
                    party not in parties and
                    not party.lower().endswith('the')):
                    parties.append(party)
        
        # Clean up and remove duplicates while preserving order
        unique_parties = []
        seen_names = set()
        
        for party in parties:
            # Clean up the party name
            cleaned_party = party.strip()
            
            # Skip if empty or too short
            if len(cleaned_party) < 3:
                continue
                
            # Skip malformed entries (like "Counsel CloudTech Systems Ltd")
            if cleaned_party.startswith(('Counsel', 'Legal Counsel', 'General Counsel')) and len(cleaned_party.split()) > 3:
                # Extract just the company name part
                words = cleaned_party.split()
                if 'Ltd' in words or 'Limited' in words or 'Inc' in words or 'Corp' in words:
                    # Find the company part
                    company_start = -1
                    for i, word in enumerate(words):
                        if word[0].isupper() and word not in ['Counsel', 'Legal', 'General']:
                            company_start = i
                            break
                    if company_start >= 0:
                        cleaned_party = ' '.join(words[company_start:])
            
            # Normalize for duplicate detection (case-insensitive)
            normalized = cleaned_party.lower()
            
            # Skip if we've already seen this name (or a very similar one)
            if normalized not in seen_names:
                # Check for partial matches (e.g., "CloudTech Systems" vs "CloudTech Systems Ltd")
                is_duplicate = False
                for seen in seen_names:
                    if (normalized in seen and len(normalized) > len(seen) * 0.7) or \
                       (seen in normalized and len(seen) > len(normalized) * 0.7):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_parties.append(cleaned_party)
                    seen_names.add(normalized)
        
        return unique_parties[:8]  # Limit to top 8 parties

    def _is_false_positive_party(self, party: str) -> bool:
        """Check if a potential party name is actually a false positive"""
        party_lower = party.lower()
        
        # Performance evaluation terms
        performance_terms = [
            'exceeds expectations', 'meets expectations', 'below expectations',
            'outstanding performance', 'satisfactory performance', 'needs improvement',
            'excellent performance', 'good performance', 'poor performance',
            'above average', 'below average', 'average performance'
        ]
        
        # Common document terms that aren't parties
        document_terms = [
            'dear sir', 'dear madam', 'yours faithfully', 'yours sincerely',
            'kind regards', 'best regards', 'thank you', 'subject line',
            'date received', 'date sent', 'from address', 'to address',
            'cc address', 'bcc address', 'email address', 'phone number',
            'fax number', 'postal code', 'zip code', 'street address',
            'po box', 'post office', 'united kingdom', 'united states',
            'new york', 'los angeles', 'san francisco', 'washington dc',
            'this employment', 'this agreement', 'this contract', 'this document',
            'senior safety', 'senior engineer', 'general counsel', 'legal counsel',
            'hr director', 'human resources', 'licence violation', 'license violation',
            'clarification date', 'effective date', 'execution date', 'signature date'
        ]
        
        # Legal/business terms that aren't parties
        business_terms = [
            'annual salary', 'monthly salary', 'hourly rate', 'base salary',
            'gross salary', 'net salary', 'total compensation', 'bonus payment',
            'pension scheme', 'health insurance', 'life insurance', 'dental insurance',
            'vision insurance', 'paid holiday', 'sick leave', 'maternity leave',
            'paternity leave', 'notice period', 'probation period', 'trial period',
            'contract terms', 'employment terms', 'service terms', 'license terms',
            'payment terms', 'delivery terms', 'warranty terms', 'liability terms',
            'confidentiality agreement', 'non disclosure', 'non compete', 'trade secrets',
            'intellectual property', 'copyright notice', 'trademark notice', 'patent rights',
            'governing law', 'dispute resolution', 'arbitration clause', 'jurisdiction clause',
            'force majeure', 'acts god', 'natural disasters', 'government action'
        ]
        
        # Time-related terms
        time_terms = [
            'business days', 'working days', 'calendar days', 'business hours',
            'working hours', 'office hours', 'standard hours', 'overtime hours',
            'part time', 'full time', 'temporary position', 'permanent position',
            'fixed term', 'indefinite term', 'renewable term', 'initial term'
        ]
        
        # Combine all false positive terms
        all_false_positives = performance_terms + document_terms + business_terms + time_terms
        
        # Check if the party matches any false positive term
        for false_positive in all_false_positives:
            if party_lower == false_positive or false_positive in party_lower:
                return True
        
        # Check for common patterns that aren't parties
        false_positive_patterns = [
            r'\b\d+\s+(days?|weeks?|months?|years?)\b',  # "30 days", "2 weeks"
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d+\b',  # "January 15"
            r'\b\d+\s+(january|february|march|april|may|june|july|august|september|october|november|december)\b',  # "15 January"
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+\w+\b',  # "Monday Morning"
            r'\b\w+\s+(morning|afternoon|evening|night)\b',  # "Good Morning"
            r'\b(good|best|kind|warm)\s+\w+\b',  # "Good Wishes", "Best Practices"
            r'\b\w+\s+(wishes|regards|greetings|salutations)\b',  # "Best Wishes"
            r'\b(this|that|these|those)\s+\w+\b',  # "This Agreement", "That Contract"
            r'\b\w+\s+(director|manager|counsel|engineer|analyst)\b',  # "HR Director", "Senior Engineer"
            r'\b\w+\s+(date|time|period|term)\b',  # "Effective Date", "Notice Period"
            r'\b\w+\s+(violation|notice|report|document)\b',  # "License Violation", "Safety Report"
        ]
        
        for pattern in false_positive_patterns:
            if re.search(pattern, party_lower):
                return True
        
        return False

    def _extract_amounts(self, text: str) -> List[str]:
        """Extract financial amounts from text"""
        amounts = []
        
        for pattern in self.amount_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                amount = match.group(0).strip()
                if amount not in amounts:
                    amounts.append(amount)
        
        return amounts[:10]  # Limit to top 10 amounts

    def _extract_legal_concepts(self, text: str) -> List[str]:
        """Extract legal concepts and terms from text"""
        concepts = []
        text_lower = text.lower()
        
        for category, keywords in self.legal_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and keyword not in concepts:
                    concepts.append(keyword)
        
        return concepts[:15]  # Limit to top 15 concepts

    def _classify_document_type(self, text: str, original_type: str) -> str:
        """Classify document type based on content analysis"""
        text_lower = text.lower()
        
        # Employment-related documents
        if any(word in text_lower for word in ['employment', 'employee', 'salary', 'position', 'job']):
            if 'agreement' in text_lower or 'contract' in text_lower:
                return 'Employment Contract'
            elif 'termination' in text_lower or 'dismissal' in text_lower:
                return 'Termination Notice'
            elif 'performance' in text_lower or 'review' in text_lower:
                return 'Performance Review'
        
        # Contract-related documents
        if any(word in text_lower for word in ['agreement', 'contract', 'terms', 'conditions']):
            if 'service' in text_lower:
                return 'Service Agreement'
            elif 'license' in text_lower or 'licence' in text_lower:
                return 'License Agreement'
            elif 'consulting' in text_lower:
                return 'Consulting Agreement'
            else:
                return 'Contract'
        
        # Communication documents
        if any(word in text_lower for word in ['from:', 'to:', 'subject:', 'email']):
            return 'Email Communication'
        
        # Legal documents
        if any(word in text_lower for word in ['notice', 'violation', 'breach', 'claim']):
            return 'Legal Notice'
        
        # Evidence documents
        if any(word in text_lower for word in ['report', 'log', 'record', 'evidence']):
            return 'Evidence Document'
        
        # Fallback to original type
        return original_type

    def _generate_summary(self, text: str, document_type: str) -> str:
        """Generate a summary of the document based on its type and content"""
        # Extract first few sentences for context
        sentences = re.split(r'[.!?]+', text)
        first_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        
        # Extract key information for summary
        parties = self._extract_parties(text)
        dates = self._extract_dates(text)
        amounts = self._extract_amounts(text)
        
        # Build summary based on document type
        if document_type == 'Employment Contract':
            summary = f"Employment agreement"
            if parties:
                summary += f" between {' and '.join(parties[:2])}"
            if dates:
                summary += f" effective from {dates[0]}"
            if amounts:
                summary += f" with compensation of {amounts[0]}"
        
        elif document_type == 'Service Agreement' or document_type == 'Consulting Agreement':
            summary = f"{document_type}"
            if parties:
                summary += f" between {' and '.join(parties[:2])}"
            if amounts:
                summary += f" for services valued at {amounts[0]}"
        
        elif document_type == 'Email Communication':
            summary = "Email communication"
            if parties:
                summary += f" involving {', '.join(parties[:3])}"
            if 'complaint' in text.lower():
                summary += " regarding complaints or concerns"
            elif 'termination' in text.lower():
                summary += " regarding employment termination"
        
        elif document_type == 'Legal Notice':
            summary = "Legal notice"
            if 'violation' in text.lower():
                summary += " regarding violations or breaches"
            if parties:
                summary += f" involving {', '.join(parties[:2])}"
        
        else:
            # Generic summary
            summary = f"{document_type}"
            if parties:
                summary += f" involving {', '.join(parties[:2])}"
        
        # Add context from first sentence if available
        if first_sentences:
            context = first_sentences[0][:100]
            if len(context) < len(first_sentences[0]):
                context += "..."
            summary += f". {context}"
        
        return summary

    def _extract_key_clauses(self, text: str, document_type: str) -> List[str]:
        """Extract key clauses and important sections from the document"""
        clauses = []
        text_lower = text.lower()
        
        # Employment contract clauses
        if 'employment' in document_type.lower():
            if 'notice' in text_lower:
                clauses.append("Notice period requirements for termination")
            if 'salary' in text_lower or 'compensation' in text_lower:
                clauses.append("Compensation and benefits provisions")
            if 'confidential' in text_lower:
                clauses.append("Confidentiality and non-disclosure obligations")
            if 'non-compete' in text_lower:
                clauses.append("Non-compete and restraint of trade clauses")
        
        # Contract clauses
        if 'contract' in document_type.lower() or 'agreement' in document_type.lower():
            if 'payment' in text_lower:
                clauses.append("Payment terms and conditions")
            if 'termination' in text_lower:
                clauses.append("Contract termination provisions")
            if 'liability' in text_lower:
                clauses.append("Liability and indemnification clauses")
            if 'intellectual property' in text_lower or 'ip' in text_lower:
                clauses.append("Intellectual property rights and ownership")
        
        # Legal notice clauses
        if 'notice' in document_type.lower():
            if 'violation' in text_lower or 'breach' in text_lower:
                clauses.append("Violation or breach allegations")
            if 'remedy' in text_lower or 'cure' in text_lower:
                clauses.append("Required remedial actions")
        
        # Evidence document clauses
        if 'evidence' in document_type.lower() or 'report' in document_type.lower():
            if 'safety' in text_lower:
                clauses.append("Safety violations and compliance issues")
            if 'performance' in text_lower:
                clauses.append("Performance metrics and evaluations")
        
        # Generic important clauses
        if 'force majeure' in text_lower:
            clauses.append("Force majeure provisions")
        if 'dispute' in text_lower:
            clauses.append("Dispute resolution mechanisms")
        if 'governing law' in text_lower:
            clauses.append("Governing law and jurisdiction clauses")
        
        return clauses[:8]  # Limit to top 8 clauses

    def _calculate_confidence_scores(self, document: Document, analysis_data: dict) -> Dict[str, float]:
        """Calculate confidence scores for different aspects of the analysis based on document quality"""
        scores = {}
        
        # Extract data from analysis_data
        text = self._load_document_content(document)
        text_lower = text.lower()
        word_count = len(text.split())
        parties = analysis_data.get('parties', [])
        dates = analysis_data.get('dates', [])
        clauses = analysis_data.get('key_clauses', [])
        
        # Document quality indicators
        has_formal_structure = bool(re.search(r'\b(?:agreement|contract|whereas|witnesseth)\b', text, re.IGNORECASE))
        has_signatures = bool(re.search(r'\b(?:signature|signed|executed|witness)\b', text, re.IGNORECASE))
        has_legal_language = bool(re.search(r'\b(?:hereby|whereas|therefore|notwithstanding)\b', text, re.IGNORECASE))
        
        # Party extraction confidence - based on actual extraction quality
        party_indicators = len(re.findall(r'\b(?:between|party|parties|client|contractor|company|employee)\b', text, re.IGNORECASE))
        base_party_confidence = 0.4
        if len(parties) >= 2:
            base_party_confidence += 0.3  # Found multiple parties
        if party_indicators >= 3:
            base_party_confidence += 0.2  # Strong party indicators
        if has_formal_structure:
            base_party_confidence += 0.1  # Formal document structure
        scores['parties'] = min(0.98, base_party_confidence + (len(parties) * 0.05))
        
        # Date extraction confidence - based on date context and quality
        date_indicators = len(re.findall(r'\b(?:date|dated|effective|expires|term|executed|signed)\b', text, re.IGNORECASE))
        base_date_confidence = 0.5
        if len(dates) >= 1:
            base_date_confidence += 0.2  # Found dates
        if date_indicators >= 2:
            base_date_confidence += 0.2  # Strong date context
        if has_signatures:
            base_date_confidence += 0.1  # Execution dates likely accurate
        scores['dates'] = min(0.98, base_date_confidence + (len(dates) * 0.05))
        
        # Contract terms confidence - based on legal document quality
        # Expanded contract language recognition
        contract_terms = len(re.findall(r'\b(?:shall|will|must|agree|covenant|undertake|obligation|duty|right|entitled|responsible|liable|bound|subject to|in accordance|pursuant|provided|including|excluding|except|unless|notwithstanding)\b', text, re.IGNORECASE))
        
        legal_structure = len(re.findall(r'\b(?:section|clause|paragraph|provision|article|subsection|term|condition|agreement|contract)\b', text, re.IGNORECASE))
        
        # Employment contract specific sections
        formal_sections = len(re.findall(r'\b(?:compensation|benefits|termination|confidentiality|duties|responsibilities|position|employment|salary|notice|governing|witness|executed|policies|procedures|retaliation|compliance|regulatory)\b', text, re.IGNORECASE))
        
        # Professional contract indicators
        contract_quality = len(re.findall(r'\b(?:annual|initial|standard|discretion|eligibility|performance|review|adjustment|participation|package|scheme|private|dental|vision|pension|holiday|proprietary|hazardous|authorities|personnel|good faith|appropriate)\b', text, re.IGNORECASE))
        
        base_contract_confidence = 0.4  # Start lower for better scaling
        
        # Formal contract structure (strong indicator)
        if has_formal_structure:
            base_contract_confidence += 0.30  # Strong formal contract structure
        
        # Contract language richness
        if contract_terms >= 15:
            base_contract_confidence += 0.25  # Very rich contract language
        elif contract_terms >= 10:
            base_contract_confidence += 0.20  # Rich contract language
        elif contract_terms >= 6:
            base_contract_confidence += 0.15  # Good contract language
        elif contract_terms >= 3:
            base_contract_confidence += 0.10  # Some contract language
        
        # Legal structure indicators
        if legal_structure >= 8:
            base_contract_confidence += 0.15  # Well-structured legal document
        elif legal_structure >= 4:
            base_contract_confidence += 0.10  # Some legal structure
        elif legal_structure >= 2:
            base_contract_confidence += 0.05  # Basic legal structure
        
        # Formal sections completeness
        if formal_sections >= 10:
            base_contract_confidence += 0.15  # Very comprehensive sections
        elif formal_sections >= 6:
            base_contract_confidence += 0.10  # Good section coverage
        elif formal_sections >= 3:
            base_contract_confidence += 0.05  # Basic sections present
        
        # Contract quality and sophistication
        if contract_quality >= 8:
            base_contract_confidence += 0.10  # High-quality professional contract
        elif contract_quality >= 4:
            base_contract_confidence += 0.05  # Some professional elements
        
        # Document comprehensiveness
        if word_count >= 1000:
            base_contract_confidence += 0.10  # Very comprehensive document
        elif word_count >= 500:
            base_contract_confidence += 0.05  # Comprehensive document
        
        scores['contract_terms'] = min(0.96, base_contract_confidence)
        
        # Key clauses confidence - based on clause identification quality
        clause_indicators = len(re.findall(r'\b(?:clause|section|paragraph|provision|term|condition)\b', text, re.IGNORECASE))
        important_clauses = len(re.findall(r'\b(?:termination|confidential|liability|payment|notice|breach)\b', text, re.IGNORECASE))
        
        base_clause_confidence = 0.4
        if len(clauses) >= 1:
            base_clause_confidence += 0.2  # Found key clauses
        if clause_indicators >= 2:
            base_clause_confidence += 0.2  # Strong clause indicators
        if important_clauses >= 3:
            base_clause_confidence += 0.2  # Important legal clauses present
        
        scores['key_clauses'] = min(0.94, base_clause_confidence + (len(clauses) * 0.05))
        
        # Legal analysis confidence - based on legal content richness
        # Expanded legal terminology recognition
        legal_terms = len(re.findall(r'\b(?:legal|law|regulation|statute|compliance|liability|jurisdiction|governing|agreement|contract|party|parties|employment|employee|employer|confidential|proprietary|termination|notice|provision|clause|section|obligations|duties|responsibilities|rights|entitled|benefits|compensation|salary|retaliation|witness|executed|incorporated|discretion)\b', text, re.IGNORECASE))
        
        legal_concepts = len(re.findall(r'\b(?:breach|damages|remedy|dispute|arbitration|mediation|court|at-will|cause|without cause|good faith|confidentiality|non-compliance|regulatory|authorities|policies|procedures|protocols)\b', text, re.IGNORECASE))
        
        # Contract-specific legal language
        contract_language = len(re.findall(r'\b(?:shall|hereby|whereas|therefore|notwithstanding|pursuant|subject to|in accordance with|provided that|including but not limited to|in witness whereof)\b', text, re.IGNORECASE))
        
        # Professional document indicators
        professional_indicators = len(re.findall(r'\b(?:director|manager|company|corporation|ltd|limited|inc|incorporated|signed|signature|date|annual|initial|standard|policies|practices)\b', text, re.IGNORECASE))
        
        base_legal_confidence = 0.3  # Start lower for more realistic scaling
        
        # Formal legal language (strong indicator)
        if has_legal_language or contract_language >= 3:
            base_legal_confidence += 0.25  # Strong formal legal language
        elif contract_language >= 1:
            base_legal_confidence += 0.15  # Some formal language
        
        # Legal terminology richness
        if legal_terms >= 15:
            base_legal_confidence += 0.25  # Very rich legal terminology
        elif legal_terms >= 10:
            base_legal_confidence += 0.20  # Rich legal terminology
        elif legal_terms >= 5:
            base_legal_confidence += 0.15  # Moderate legal terminology
        elif legal_terms >= 2:
            base_legal_confidence += 0.10  # Some legal terminology
        
        # Legal concepts present
        if legal_concepts >= 5:
            base_legal_confidence += 0.15  # Many legal concepts
        elif legal_concepts >= 3:
            base_legal_confidence += 0.10  # Some legal concepts
        elif legal_concepts >= 1:
            base_legal_confidence += 0.05  # Few legal concepts
        
        # Professional document structure
        if has_formal_structure:
            base_legal_confidence += 0.10  # Professional document structure
        
        # Professional indicators
        if professional_indicators >= 8:
            base_legal_confidence += 0.10  # Very professional
        elif professional_indicators >= 4:
            base_legal_confidence += 0.05  # Somewhat professional
        
        scores['legal_analysis'] = min(0.95, base_legal_confidence)
        
        return scores

    def _calculate_extraction_confidence(self, text: str, dates: List[date], parties: List[str], amounts: List[str], concepts: List[str]) -> float:
        """Calculate overall confidence for key information extraction"""
        # Base confidence
        confidence = 0.5
        
        # Boost confidence based on successful extractions
        if dates:
            confidence += 0.15
        if parties:
            confidence += 0.15
        if amounts:
            confidence += 0.1
        if concepts:
            confidence += 0.1
        
        # Text quality indicators
        if len(text) > 500:
            confidence += 0.05
        if len(text.split()) > 100:
            confidence += 0.05
        
        return min(0.95, confidence)

    def _assess_document_risks(self, text: str, document_type: str) -> Dict:
        """
        Assess potential legal and business risks in the document
        
        Returns:
            Dict containing risk level, specific issues, and recommendations
        """
        risks = {
            'overall_risk': 'low',
            'risk_score': 0.0,
            'issues': [],
            'recommendations': []
        }
        
        text_lower = text.lower()
        risk_score = 0.0
        
        # Check for high-risk patterns
        for pattern in self.risk_patterns['high_risk']:
            if re.search(pattern, text, re.IGNORECASE):
                risk_score += 0.3
                risks['issues'].append(f"High-risk clause detected: {pattern}")
                risks['recommendations'].append("Review high-risk provisions with legal counsel")
        
        # Check for medium-risk patterns
        for pattern in self.risk_patterns['medium_risk']:
            if re.search(pattern, text, re.IGNORECASE):
                risk_score += 0.15
                risks['issues'].append(f"Medium-risk clause detected: {pattern}")
        
        # Check for compliance risks
        for pattern in self.risk_patterns['compliance_risk']:
            if re.search(pattern, text, re.IGNORECASE):
                risk_score += 0.2
                risks['issues'].append(f"Compliance risk identified: {pattern}")
                risks['recommendations'].append("Ensure compliance procedures are in place")
        
        # Document-specific risk assessment
        if 'employment' in document_type.lower():
            if 'at will' not in text_lower and 'termination' in text_lower:
                risk_score += 0.1
                risks['issues'].append("Employment termination terms may be restrictive")
            
            if 'non-compete' in text_lower:
                risk_score += 0.15
                risks['issues'].append("Non-compete clause requires jurisdictional review")
        
        # Determine overall risk level
        if risk_score >= 0.5:
            risks['overall_risk'] = 'high'
        elif risk_score >= 0.25:
            risks['overall_risk'] = 'medium'
        else:
            risks['overall_risk'] = 'low'
        
        risks['risk_score'] = min(1.0, risk_score)
        
        # Add general recommendations based on risk level
        if risks['overall_risk'] == 'high':
            risks['recommendations'].append("Immediate legal review recommended before execution")
        elif risks['overall_risk'] == 'medium':
            risks['recommendations'].append("Consider legal review of identified risk areas")
        
        return risks

    def _analyze_compliance(self, text: str, document_type: str) -> Dict:
        """
        Analyze document for compliance with common legal and regulatory requirements
        
        Returns:
            Dict containing compliance status and specific compliance areas
        """
        compliance = {
            'status': 'compliant',
            'score': 1.0,
            'areas': [],
            'violations': [],
            'recommendations': []
        }
        
        text_lower = text.lower()
        compliance_score = 1.0
        
        # Data protection compliance (GDPR, privacy laws)
        if any(term in text_lower for term in ['personal data', 'data processing', 'privacy']):
            if 'gdpr' not in text_lower and 'data protection' not in text_lower:
                compliance_score -= 0.2
                compliance['violations'].append("Missing explicit data protection compliance references")
                compliance['recommendations'].append("Add GDPR/data protection compliance clauses")
            else:
                compliance['areas'].append("Data Protection Compliance")
        
        # Employment law compliance
        if 'employment' in document_type.lower():
            required_clauses = ['equal opportunity', 'discrimination', 'harassment']
            missing_clauses = [clause for clause in required_clauses if clause not in text_lower]
            
            if missing_clauses:
                compliance_score -= 0.1 * len(missing_clauses)
                compliance['violations'].extend([f"Missing {clause} provisions" for clause in missing_clauses])
                compliance['recommendations'].append("Include standard employment law protections")
            else:
                compliance['areas'].append("Employment Law Compliance")
        
        # Intellectual property compliance
        if any(term in text_lower for term in ['intellectual property', 'copyright', 'trademark']):
            if 'ownership' not in text_lower or 'assignment' not in text_lower:
                compliance_score -= 0.15
                compliance['violations'].append("Unclear intellectual property ownership terms")
                compliance['recommendations'].append("Clarify IP ownership and assignment terms")
            else:
                compliance['areas'].append("Intellectual Property Compliance")
        
        # Contract law compliance (consideration, capacity, legality)
        if 'contract' in document_type.lower() or 'agreement' in document_type.lower():
            if 'consideration' not in text_lower and '$' not in text and 'payment' not in text_lower:
                compliance_score -= 0.2
                compliance['violations'].append("No clear consideration identified")
                compliance['recommendations'].append("Ensure valid consideration is clearly stated")
        
        # Determine overall compliance status
        if compliance_score < 0.7:
            compliance['status'] = 'non-compliant'
        elif compliance_score < 0.9:
            compliance['status'] = 'partially_compliant'
        else:
            compliance['status'] = 'compliant'
        
        compliance['score'] = max(0.0, compliance_score)
        
        return compliance

    def _analyze_temporal_elements(self, text: str) -> Dict:
        """
        Analyze time-sensitive elements in the document
        
        Returns:
            Dict containing deadlines, renewal terms, and notice periods
        """
        temporal = {
            'deadlines': [],
            'renewal_terms': [],
            'notice_periods': [],
            'critical_dates': []
        }
        
        # Extract deadlines
        for pattern in self.temporal_patterns['deadlines']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                temporal['deadlines'].append({
                    'text': match.group(0),
                    'context': text[max(0, match.start()-50):match.end()+50]
                })
        
        # Extract renewal terms
        for pattern in self.temporal_patterns['renewal_terms']:
            if re.search(pattern, text, re.IGNORECASE):
                temporal['renewal_terms'].append(pattern)
        
        # Extract notice periods
        for pattern in self.temporal_patterns['notice_periods']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                temporal['notice_periods'].append({
                    'period': match.group(1) if match.groups() else 'unspecified',
                    'context': text[max(0, match.start()-30):match.end()+30]
                })
        
        return temporal

    def _perform_semantic_analysis(self, text: str, document_type: str) -> Dict:
        """
        Perform semantic analysis to understand document intent and relationships
        
        Returns:
            Dict containing semantic insights and relationship mappings
        """
        semantic = {
            'intent': 'unknown',
            'tone': 'neutral',
            'complexity': 'medium',
            'relationships': [],
            'obligations': [],
            'rights': []
        }
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Determine document intent
        if any(term in text_lower for term in ['establish', 'create', 'form']):
            semantic['intent'] = 'establishment'
        elif any(term in text_lower for term in ['modify', 'amend', 'change']):
            semantic['intent'] = 'modification'
        elif any(term in text_lower for term in ['terminate', 'end', 'cancel']):
            semantic['intent'] = 'termination'
        elif any(term in text_lower for term in ['notice', 'inform', 'notify']):
            semantic['intent'] = 'notification'
        
        # Analyze tone
        formal_indicators = len(re.findall(r'\b(?:hereby|whereas|notwithstanding|pursuant)\b', text, re.IGNORECASE))
        if formal_indicators >= 5:
            semantic['tone'] = 'formal'
        elif formal_indicators >= 2:
            semantic['tone'] = 'semi-formal'
        else:
            semantic['tone'] = 'informal'
        
        # Determine complexity
        legal_terms = len(re.findall(r'\b(?:' + '|'.join(self.legal_keywords['legal_concepts']) + r')\b', text, re.IGNORECASE))
        if word_count > 1000 and legal_terms > 15:
            semantic['complexity'] = 'high'
        elif word_count > 500 and legal_terms > 8:
            semantic['complexity'] = 'medium'
        else:
            semantic['complexity'] = 'low'
        
        # Extract obligations and rights
        obligation_patterns = [
            r'(?:shall|must|will|agree to|undertake to|covenant to)\s+([^.]{10,100})',
            r'(?:obligation|duty|responsibility)\s+(?:to|of)\s+([^.]{10,100})'
        ]
        
        for pattern in obligation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                semantic['obligations'].append(match.group(1).strip())
        
        rights_patterns = [
            r'(?:right|entitled|may|permitted)\s+(?:to|of)\s+([^.]{10,100})',
            r'(?:rights)\s+(?:include|encompass)\s+([^.]{10,100})'
        ]
        
        for pattern in rights_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                semantic['rights'].append(match.group(1).strip())
        
        return semantic

    def _generate_enhanced_summary(self, text: str, document_type: str, risk_assessment: Dict) -> str:
        """Generate an enhanced summary including risk and compliance insights"""
        # Get basic summary
        basic_summary = self._generate_summary(text, document_type)
        
        # Add risk information
        risk_level = risk_assessment.get('overall_risk', 'low')
        if risk_level == 'high':
            basic_summary += f" ⚠️ HIGH RISK: Immediate legal review recommended."
        elif risk_level == 'medium':
            basic_summary += f" ⚡ MEDIUM RISK: Consider legal review of identified areas."
        
        # Add key issues if any
        issues = risk_assessment.get('issues', [])
        if issues:
            key_issue = issues[0]  # Show first issue
            basic_summary += f" Key concern: {key_issue[:100]}..."
        
        return basic_summary

    def _extract_enhanced_clauses(self, text: str, document_type: str, semantic_analysis: Dict) -> List[str]:
        """Extract key clauses with enhanced semantic understanding"""
        clauses = self._extract_key_clauses(text, document_type)
        
        # Add semantic-based clauses
        obligations = semantic_analysis.get('obligations', [])
        rights = semantic_analysis.get('rights', [])
        
        # Add top obligations as clauses
        for obligation in obligations[:3]:
            clause_text = f"Obligation: {obligation[:80]}..."
            if clause_text not in clauses:
                clauses.append(clause_text)
        
        # Add top rights as clauses
        for right in rights[:2]:
            clause_text = f"Right: {right[:80]}..."
            if clause_text not in clauses:
                clauses.append(clause_text)
        
        return clauses[:10]  # Limit to top 10 clauses

    def _calculate_complexity_score(self, semantic_analysis: Dict, word_count: int) -> float:
        """Calculate document complexity score based on various factors"""
        complexity_score = 0.0
        
        # Base complexity from semantic analysis
        complexity_level = semantic_analysis.get('complexity', 'medium')
        if complexity_level == 'high':
            complexity_score += 0.4
        elif complexity_level == 'medium':
            complexity_score += 0.25
        else:
            complexity_score += 0.1
        
        # Word count factor
        if word_count > 2000:
            complexity_score += 0.3
        elif word_count > 1000:
            complexity_score += 0.2
        elif word_count > 500:
            complexity_score += 0.1
        
        # Legal language sophistication
        tone = semantic_analysis.get('tone', 'neutral')
        if tone == 'formal':
            complexity_score += 0.2
        elif tone == 'semi-formal':
            complexity_score += 0.1
        
        # Number of obligations and rights
        obligations_count = len(semantic_analysis.get('obligations', []))
        rights_count = len(semantic_analysis.get('rights', []))
        
        complexity_score += min(0.2, (obligations_count + rights_count) * 0.02)
        
        return min(1.0, complexity_score)