import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { Case, Document, LegalSearchResult } from '../types/api';

// State interface
interface AppState {
  cases: Case[];
  documents: Document[];
  searchResults: LegalSearchResult[];
  loading: {
    cases: boolean;
    documents: boolean;
    search: boolean;
  };
  error: string | null;
}

// Action types
type AppAction =
  | { type: 'SET_LOADING'; payload: { key: keyof AppState['loading']; value: boolean } }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_CASES'; payload: Case[] }
  | { type: 'ADD_CASE'; payload: Case }
  | { type: 'UPDATE_CASE'; payload: Case }
  | { type: 'SET_DOCUMENTS'; payload: Document[] }
  | { type: 'ADD_DOCUMENT'; payload: Document }
  | { type: 'SET_SEARCH_RESULTS'; payload: LegalSearchResult[] }
  | { type: 'CLEAR_SEARCH_RESULTS' };

// Initial state
const initialState: AppState = {
  cases: [],
  documents: [],
  searchResults: [],
  loading: {
    cases: false,
    documents: false,
    search: false,
  },
  error: null,
};

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        loading: {
          ...state.loading,
          [action.payload.key]: action.payload.value,
        },
      };
    
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    
    case 'SET_CASES':
      return {
        ...state,
        cases: action.payload,
      };
    
    case 'ADD_CASE':
      return {
        ...state,
        cases: [...state.cases, action.payload],
      };
    
    case 'UPDATE_CASE':
      return {
        ...state,
        cases: state.cases.map(c => 
          c.id === action.payload.id ? action.payload : c
        ),
      };
    
    case 'SET_DOCUMENTS':
      return {
        ...state,
        documents: action.payload,
      };
    
    case 'ADD_DOCUMENT':
      return {
        ...state,
        documents: [...state.documents, action.payload],
      };
    
    case 'SET_SEARCH_RESULTS':
      return {
        ...state,
        searchResults: action.payload,
      };
    
    case 'CLEAR_SEARCH_RESULTS':
      return {
        ...state,
        searchResults: [],
      };
    
    default:
      return state;
  }
}

// Context
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

// Provider component
export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

// Action creators (helper functions)
export const useAppActions = () => {
  const { dispatch } = useAppContext();

  return {
    setLoading: (key: keyof AppState['loading'], value: boolean) =>
      dispatch({ type: 'SET_LOADING', payload: { key, value } }),
    
    setError: (error: string | null) =>
      dispatch({ type: 'SET_ERROR', payload: error }),
    
    setCases: (cases: Case[]) =>
      dispatch({ type: 'SET_CASES', payload: cases }),
    
    addCase: (case_: Case) =>
      dispatch({ type: 'ADD_CASE', payload: case_ }),
    
    updateCase: (case_: Case) =>
      dispatch({ type: 'UPDATE_CASE', payload: case_ }),
    
    setDocuments: (documents: Document[]) =>
      dispatch({ type: 'SET_DOCUMENTS', payload: documents }),
    
    addDocument: (document: Document) =>
      dispatch({ type: 'ADD_DOCUMENT', payload: document }),
    
    setSearchResults: (results: LegalSearchResult[]) =>
      dispatch({ type: 'SET_SEARCH_RESULTS', payload: results }),
    
    clearSearchResults: () =>
      dispatch({ type: 'CLEAR_SEARCH_RESULTS' }),
  };
};