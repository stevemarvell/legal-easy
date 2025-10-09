import { useParams } from 'react-router-dom';
import CaseList from '../components/CaseManagement/CaseList';
import CaseDetail from '../components/CaseManagement/CaseDetail';

const Cases = () => {
  const { caseId } = useParams<{ caseId: string }>();

  // If we have a caseId, show the detail view
  if (caseId) {
    return <CaseDetail />;
  }

  // Otherwise show the list view
  return <CaseList />;
};

export default Cases;