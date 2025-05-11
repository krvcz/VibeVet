import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import { handleApiError } from '../../utils/apiErrors';
import type { Species } from '../types';

export const speciesApi = {
  // Get list of species
  getSpecies: async (): Promise<Species[]> => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        return mockData.species;
      }
      
      const response = await apiClient.get<{ results: Species[] }>('/species');
      return response.data.results;
    } catch (error) {
      throw handleApiError(error);
    }
  }
};