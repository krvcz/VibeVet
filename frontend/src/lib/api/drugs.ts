import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import { handleApiError } from '../../utils/apiErrors';
import type { Drug, CustomDrugDto, CreateCustomDrugDto, UpdateCustomDrugDto, DosageCalcResult, DosageCalcParams } from '../types';

export const drugsApi = {
  // Get list of standard drugs
  getDrugs: async (search?: string): Promise<Drug[]> => {
    try {
      console.log('Fetching drugs with search:', search);
      
      if (isDebugMode) {
        await simulateDelay();
        const drugs = mockData.drugs;
        if (search) {
          return drugs.filter(drug => 
            drug.name.toLowerCase().includes(search.toLowerCase()) ||
            drug.active_ingredient.toLowerCase().includes(search.toLowerCase())
          );
        }
        return drugs;
      }
      
      const response = await apiClient.get<{ results: Drug[] }>('/drugs/', { params: { search } });
      return response.data.results;
    } catch (error) {
      console.error('Failed to fetch drugs:', error);
      throw handleApiError(error);
    }
  },

  // Get list of custom drugs with pagination
  getCustomDrugs: async (search?: string, page: number = 1) => {
    try {
      console.log('Fetching custom drugs with search:', search, 'page:', page);
      
      if (isDebugMode) {
        await simulateDelay();
        let drugs = mockData.customDrugs;
        
        if (search) {
          drugs = drugs.filter(drug => 
            drug.name.toLowerCase().includes(search.toLowerCase()) ||
            drug.active_ingredient.toLowerCase().includes(search.toLowerCase())
          );
        }
        
        // Mock pagination with 20 items per page
        const itemsPerPage = 20;
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedDrugs = drugs.slice(startIndex, endIndex);
        
        return {
          count: drugs.length,
          next: endIndex < drugs.length ? `/api/custom-drugs/?page=${page + 1}` : null,
          previous: page > 1 ? `/api/custom-drugs/?page=${page - 1}` : null,
          results: paginatedDrugs
        };
      }
      
      const response = await apiClient.get('/custom-drugs/', {
        params: { search, page }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch custom drugs:', error);
      throw handleApiError(error);
    }
  },

  // Get single custom drug by ID
  getCustomDrug: async (id: string): Promise<CustomDrugDto> => {
    try {
      console.log('Fetching custom drug:', id);
      
      if (isDebugMode) {
        await simulateDelay();
        const drug = mockData.customDrugs.find(d => d.id === id);
        if (!drug) {
          throw new Error('Drug not found');
        }
        return drug;
      }
      
      const response = await apiClient.get<CustomDrugDto>(`/custom-drugs/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch custom drug:', error);
      throw handleApiError(error);
    }
  },

  // Create custom drug
  createCustomDrug: async (drug: CreateCustomDrugDto): Promise<CustomDrugDto> => {
    try {
      console.log('Creating custom drug:', drug);
      
      if (isDebugMode) {
        await simulateDelay();
        const newDrug = {
          ...drug,
          id: String(mockData.customDrugs.length + 1),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        mockData.customDrugs.push(newDrug);
        return newDrug;
      }
      
      const response = await apiClient.post<CustomDrugDto>('/custom-drugs/', drug);
      return response.data;
    } catch (error) {
      console.error('Failed to create custom drug:', error);
      throw handleApiError(error);
    }
  },

  // Update custom drug
  updateCustomDrug: async (id: string, drug: UpdateCustomDrugDto): Promise<CustomDrugDto> => {
    try {
      console.log('Updating custom drug:', id, drug);
      
      if (isDebugMode) {
        await simulateDelay();
        const index = mockData.customDrugs.findIndex(d => d.id === id);
        if (index === -1) throw new Error('Drug not found');
        
        mockData.customDrugs[index] = {
          ...mockData.customDrugs[index],
          ...drug,
          updated_at: new Date().toISOString()
        };
        return mockData.customDrugs[index];
      }
      
      const response = await apiClient.put<CustomDrugDto>(`/custom-drugs/${id}/`, drug);
      return response.data;
    } catch (error) {
      console.error('Failed to update custom drug:', error);
      throw handleApiError(error);
    }
  },

  // Delete custom drug
  deleteCustomDrug: async (id: string): Promise<void> => {
    try {
      console.log('Deleting custom drug:', id);
      
      if (isDebugMode) {
        await simulateDelay();
        const index = mockData.customDrugs.findIndex(d => d.id === id);
        if (index === -1) throw new Error('Drug not found');
        mockData.customDrugs.splice(index, 1);
        return;
      }
      
      await apiClient.delete(`/custom-drugs/${id}/`);
    } catch (error) {
      console.error('Failed to delete custom drug:', error);
      throw handleApiError(error);
    }
  },

  // Calculate dosage
  calculateDosage: async (params: DosageCalcParams): Promise<DosageCalcResult> => {
    try {
      console.log('Calculating dosage with params:', params);
      
      if (isDebugMode) {
        await simulateDelay();
        
        if (params.weight <= 0 || params.weight >= 1000) {
          throw new Error('Weight must be between 1 and 999');
        }
        
        const drug = params.drug_type === 'custom' 
          ? mockData.customDrugs.find(d => d.id === params.drug_id)
          : mockData.drugs.find(d => d.id === params.drug_id);

        if (!drug) {
          throw new Error('Drug not found');
        }
        
        const calculatedDose = parseFloat(drug.measurement_value) * params.weight;
        
        const result = {
          drug_id: params.drug_id,
          calculated_dose: calculatedDose.toFixed(5),
          unit: drug.measurement_unit.short_name
        };
        
        console.log('Mock calculation result:', result);
        return result;
      }
      
      const response = await apiClient.post<DosageCalcResult>('/dosage-calc/', params);
      console.log('API Response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to calculate dosage:', error);
      throw handleApiError(error);
    }
  }
};