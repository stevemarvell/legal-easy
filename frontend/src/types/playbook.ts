export interface PlaybookRule {
  id: string;
  condition: string;
  action: string;
  weight: number;
  description: string;
}

export interface Playbook {
  id: string;
  case_type: string;
  name: string;
  rules: PlaybookRule[];
  decision_tree: Record<string, any>;
  monetary_ranges: Record<string, [number, number]>;
  escalation_paths: string[];
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