import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import type { TreatmentGuide } from '../types';

export const treatmentsApi = {
  // Create treatment guide query
  createTreatmentGuide: async (factors: { [key: string]: any }): Promise<TreatmentGuide> => {
    if (isDebugMode) {
      await simulateDelay();
      
      // Mock response based on provided factors
      const newTreatment = {
        id: String(mockData.treatments.length + 1),
        factors,
        result: `Based on the provided factors:\n\n` +
               `Fever (High Probability): ${factors.temperature ? `Temperature of ${factors.temperature}°C suggests possible infection` : 'No temperature data provided'}\n\n` +
               `Cardiovascular Status (Medium Probability): ${factors.heart_rate ? `Heart rate of ${factors.heart_rate} bpm` : 'No heart rate data provided'}${factors.blood_pressure ? `, Blood pressure ${factors.blood_pressure}` : ''}\n\n` +
               `Laboratory Values: ${[
                 factors.calcium && `Calcium: ${factors.calcium}`,
                 factors.glucose && `Glucose: ${factors.glucose}`,
                 factors.potassium && `Potassium: ${factors.potassium}`,
                 factors.hemoglobin && `Hemoglobin: ${factors.hemoglobin}`,
                 factors.platelets && `Platelets: ${factors.platelets}`
               ].filter(Boolean).join(', ') || 'No laboratory values provided'}\n\n` +
               `Additional Information: ${factors.additional_notes || 'None provided'}`
      };
      
      mockData.treatments.push(newTreatment);
      return newTreatment;
    }
    
    const response = await apiClient.post<TreatmentGuide>('/treatment-guides/', { factors });
    return response.data;
  },

  // Rate treatment guide
  rateTreatmentGuide: async (id: string, rating: 'up' | 'down'): Promise<{ message: string }> => {
    if (isDebugMode) {
      await simulateDelay();
      
      const treatment = mockData.treatments.find(t => t.id === id);
      if (!treatment) {
        throw new Error('Treatment guide not found');
      }
      
      return { message: 'Rating updated successfully.' };
    }
    
    const response = await apiClient.patch<{ message: string }>(`/treatment-guides/${id}/rate/`, { rating });
    return response.data;
  }
};