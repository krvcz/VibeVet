import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import type { DrugInteraction } from '../types';

export const interactionsApi = {
  // Create drug interaction query
  createInteraction: async (params: {
    drug_ids: number[];
    context?: string;
  }): Promise<DrugInteraction> => {
    if (isDebugMode) {
      await simulateDelay();
      
      // Mock interaction response
      const drugNames = params.drug_ids
        .map(id => mockData.drugs.find(d => d.id === String(id))?.name)
        .filter(Boolean)
        .join(', ');
      
      const newInteraction = {
        id: String(mockData.interactions.length + 1),
        query: drugNames,
        result: `Mock interaction analysis for: ${drugNames}${params.context ? ` Context: ${params.context}` : ''}`
      };
      
      mockData.interactions.push(newInteraction);
      return newInteraction;
    }
    
    const response = await apiClient.post<DrugInteraction>('/drug-interactions/', params);
    return response.data;
  },

  // Get interaction history
  getInteractions: async () => {
    if (isDebugMode) {
      await simulateDelay();
      return mockData.interactions;
    }
    
    const response = await apiClient.get<{ results: DrugInteraction[] }>('/drug-interactions/');
    return response.data.results;
  },

  // Rate interaction
  rateInteraction: async (id: string, rating: 'up' | 'down'): Promise<{ message: string }> => {
    if (isDebugMode) {
      await simulateDelay();
      
      const interaction = mockData.interactions.find(i => i.id === id);
      if (!interaction) {
        throw new Error('Interaction not found');
      }
      
      return { message: 'Rating updated successfully.' };
    }
    
    const response = await apiClient.patch<{ message: string }>(`/drug-interactions/${id}/rate/`, { rating });
    return response.data;
  }
};