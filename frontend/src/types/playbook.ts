export interface PlaybookRule {
  id: string;
  condition: string;
  action: string;
  weight: number;
  description: string;
  legal_basis?: string;
  evidence_required?: string[];
}

export interface MonetaryRange {
  range: [number, number];
  description: string;
  factors: string[];
}

export interface EscalationPath {
  step: number;
  action: string;
  timeline: string;
  description: string;
}

export interface Playbook {
  id: string;
  case_type: string;
  name: string;
  description?: string;
  version?: string;
  last_updated?: string;
  rules: PlaybookRule[];
  decision_tree: Record<string, any>;
  monetary_ranges: Record<string, MonetaryRange>;
  escalation_paths: EscalationPath[];
  key_statutes?: string[];
  success_factors?: string[];
}

export interface CaseStrengthAssessment {
  overall_strength: "Strong" | "Moderate" | "Weak" | "Unknown";
  confidence_level: number;
  key_strengths: string[];
  potential_weaknesses: string[];
  supporting_evidence: string[];
}

export interface StrategicRecommendation {
  id: string;
  title: string;
  description: string;
  priority: "High" | "Medium" | "Low";
  rationale: string;
  supporting_precedents: string[];
}

export interface LegalPrecedent {
  id: string;
  title: string;
  category: "statutes" | "case_law" | "regulations";
  relevance: string;
  key_principle?: string;
}

export interface AppliedPlaybook {
  id: string;
  name: string;
  case_type: string;
}

export interface ComprehensiveAnalysis {
  case_id: string;
  case_strength_assessment: CaseStrengthAssessment;
  strategic_recommendations: StrategicRecommendation[];
  relevant_precedents: LegalPrecedent[];
  applied_playbook: AppliedPlaybook | null;
  analysis_timestamp: string;
  fallback_reason?: string;
}

export interface PlaybookResult {
  case_id: string;
  playbook_id: string;
  applied_rules: string[];
  recommendations: string[];
  case_strength: string;
  reasoning: string;
}

export interface CaseAssessment {
  case_id: string;
  playbook_used: string;
  case_strength: string; // "Strong", "Moderate", "Weak"
  key_issues: string[];
  recommended_actions: string[];
  monetary_assessment?: [number, number];
  applied_rules: string[];
  reasoning: string;
}