import React from 'react';

interface DocumentListProps {
  caseId: string;
}

const DocumentList: React.FC<DocumentListProps> = ({ caseId }) => {
  return (
    <div className="document-list">
      <h3>Documents</h3>
      <p>Case ID: {caseId}</p>
      {/* Implementation will be added in later tasks */}
    </div>
  );
};

export default DocumentList;