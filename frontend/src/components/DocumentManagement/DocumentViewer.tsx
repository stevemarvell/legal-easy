import React from 'react';

interface DocumentViewerProps {
  documentId: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentId }) => {
  return (
    <div className="document-viewer">
      <h3>Document Viewer</h3>
      <p>Document ID: {documentId}</p>
      {/* Implementation will be added in later tasks */}
    </div>
  );
};

export default DocumentViewer;