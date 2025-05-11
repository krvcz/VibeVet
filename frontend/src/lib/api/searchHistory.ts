import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import type { SearchHistoryResponse } from '../types';

export const searchHistoryApi = {
  // Get search history
  getHistory: async (params?: {
    page?: number;
    limit?: number;
    module?: string;
    from_date?: string;
    to_date?: string;
  }) => {
    if (isDebugMode) {
      await simulateDelay();
      
      let results = mockData.searchHistory || [];
      
      // Apply filters if provided
      if (params?.module) {
        results = results.filter(item => item.module === params.module);
      }
      
      if (params?.from_date) {
        results = results.filter(item => 
          new Date(item.timestamp) >= new Date(params.from_date!)
        );
      }
      
      if (params?.to_date) {
        results = results.filter(item => 
          new Date(item.timestamp) <= new Date(params.to_date!)
        );
      }
      
      // Apply pagination
      const page = params?.page || 1;
      const limit = params?.limit || 10;
      const start = (page - 1) * limit;
      const end = start + limit;
      
      const paginatedResults = results.slice(start, end);
      
      return {
        count: results.length,
        next: end < results.length ? 
          `/api/search-history/?limit=${limit}&page=${page + 1}` : null,
        previous: page > 1 ? 
          `/api/search-history/?limit=${limit}&page=${page - 1}` : null,
        results: paginatedResults
      };
    }
    
    const response = await apiClient.get<SearchHistoryResponse>('/search-history', { params });
    return response.data;
  },

  // Rate history item
  rateHistoryItem: async (id: string, rating: 'up' | 'down'): Promise<{ message: string }> => {
    if (isDebugMode) {
      await simulateDelay();
      
      const item = mockData.searchHistory?.find(i => i.id === id);
      if (!item) {
        throw new Error('History item not found');
      }
      
      return { message: 'Rating updated successfully.' };
    }
    
    const response = await apiClient.patch<{ message: string }>(`/search-history/${id}/rate`, { rating });
    return response.data;
  },

  // Clear history
  clearHistory: async () => {
    if (isDebugMode) {
      await simulateDelay();
      mockData.searchHistory = [];
      return;
    }
    
    await apiClient.delete('/search-history');
  }
};