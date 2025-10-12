export interface Document {
  id: string;
  case_id: string;
  name: string;
  type: string; // "Contract", "Email", "Legal Brief", "Evidence"
  size: number;
  upload_date: string;
  content_preview: string;

}

