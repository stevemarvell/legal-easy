import { useEffect } from 'react';
import { APP_NAME } from '../constants/branding';

/**
 * Hook to set the document title
 * @param title - The page title (will be prefixed with app name)
 */
export const useDocumentTitle = (title?: string) => {
  useEffect(() => {
    if (title) {
      document.title = `${title} - ${APP_NAME}`;
    } else {
      document.title = `${APP_NAME} - Intelligent Legal Case Analysis`;
    }
  }, [title]);
};

export default useDocumentTitle;