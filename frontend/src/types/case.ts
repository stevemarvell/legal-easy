export interface Case {
  id: string;
  title: string;
  case_type: string; // "Employment Dispute", "Contract Breach", "Debt Claim"
  client_name: string;
  status: string; // "Active", "Under Review", "Resolved"
  created_date: string;
  summary: string;
  key_parties: string[];
  documents: string[]; // Document IDs
  playbook_id: string;
}

export interface CaseStatistics {
  total_cases: number;
  active_cases: number;
  resolved_cases: number;
  under_review_cases: number;
  recent_activity_count: number;
}