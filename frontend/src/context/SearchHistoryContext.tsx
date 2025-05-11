import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { searchHistoryApi } from '../lib/api/searchHistory';
import toast from 'react-hot-toast';

export interface HistoryItem {
  id: string;
  module: string;
  query: string;
  timestamp: string;
}

interface SearchHistoryContextType {
  history: HistoryItem[];
  isLoading: boolean;
  error: string | null;
  pagination: {
    count: number;
    next: string | null;
    previous: string | null;
  };
  currentPage: number;
  setCurrentPage: (page: number) => void;
  loadHistory: (page?: number) => Promise<void>;
}

const SearchHistoryContext = createContext<SearchHistoryContextType | undefined>(undefined);

export const useSearchHistory = () => {
  const context = useContext(SearchHistoryContext);
  if (context === undefined) {
    throw new Error('useSearchHistory must be used within a SearchHistoryProvider');
  }
  return context;
};

export const SearchHistoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState({
    count: 0,
    next: null as string | null,
    previous: null as string | null
  });
  
  const { isAuthenticated } = useAuth();

  const loadHistory = async (page: number = 1) => {
    if (!isAuthenticated) {
      setHistory([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await searchHistoryApi.getHistory({
        page,
        limit: 20
      });
      
      setHistory(response.results);
      setPagination({
        count: response.count,
        next: response.next,
        previous: response.previous
      });
      setCurrentPage(page);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
        toast.error(error.message);
      } else {
        setError('An unexpected error occurred while loading search history');
        toast.error('Failed to load search history');
      }
      setHistory([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [isAuthenticated]);

  const value = {
    history,
    isLoading,
    error,
    pagination,
    currentPage,
    setCurrentPage,
    loadHistory
  };

  return <SearchHistoryContext.Provider value={value}>{children}</SearchHistoryContext.Provider>;
};