import React from 'react';

interface PlaybookViewerProps {
  caseType: string;
}

const PlaybookViewer: React.FC<PlaybookViewerProps> = ({ caseType }) => {
  return (
    <div className="playbook-viewer">
      <h3>Playbook Viewer</h3>
      <p>Case Type: {caseType}</p>
      {/* Implementation will be added in later tasks */}
    </div>
  );
};

export default PlaybookViewer;