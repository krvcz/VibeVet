import { BaseModel } from './types';

// User related types
export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  name?: string;
  confirm_password: string;
}

// Base interfaces
export interface BaseModel {
  id: string;
  created_at?: string;
  updated_at?: string;
}

// Species and measurement units
export interface Species {
  id: string;
  name: string;
  description: string;
}

export interface MeasurementUnit {
  id: string;
  name: string;
  short_name: string;
}

// Drug related types
export interface Drug {
  id: string;
  name: string;
  active_ingredient: string;
  species: Species;
  measurement_value: string;
  measurement_unit: MeasurementUnit;
  per_weight_value: string;
  per_weight_unit: MeasurementUnit;
  contraindications?: string;
}

// DTOs for custom drugs
export interface CustomDrugDto {
  id: string;
  name: string;
  active_ingredient: string;
  species: Species;
  contraindications?: string;
  measurement_value: string;
  measurement_unit: MeasurementUnit;
  per_weight_value: string;
  per_weight_unit: MeasurementUnit;
  created_at?: string;
  updated_at?: string;
}

export interface CreateCustomDrugDto {
  name: string;
  active_ingredient: string;
  species: string; // ID
  contraindications?: string;
  measurement_value: string;
  measurement_unit: string; // ID
  per_weight_value: string;
  per_weight_unit: string; // ID
}

export interface UpdateCustomDrugDto extends Partial<CreateCustomDrugDto> {}

export interface DosageCalcResult {
  drug_id: string;
  calculated_dose: string;
  unit: string;
}

export type DrugType = 'standard' | 'custom';

export interface DosageCalcParams {
  drug_id: string;
  drug_type: DrugType;
  weight: number;
  species: string;
  target_unit: string;
}

// Interaction related types
export interface DrugInteraction {
  id: string;
  query: string;
  result: string;
}

// Treatment related types
export interface DiagnosticFactors {
  [key: string]: any;
}

export interface TreatmentGuide {
  id: string;
  factors: DiagnosticFactors;
  result: string;
}

// History related types
export interface SearchHistoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: SearchHistoryItem[];
}

export interface SearchHistoryItem {
  id: string;
  module: string;
  query: string;
  timestamp: string;
}