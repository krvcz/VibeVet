import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import { handleApiError } from '../../utils/apiErrors';
import type { MeasurementUnit } from '../types';

export const unitsApi = {
  // Get list of measurement units
  getUnits: async (): Promise<MeasurementUnit[]> => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        return mockData.measurementUnits;
      }
      
      const response = await apiClient.get<{ results: MeasurementUnit[] }>('/units');
      return response.data.results;
    } catch (error) {
      throw handleApiError(error);
    }
  }
};