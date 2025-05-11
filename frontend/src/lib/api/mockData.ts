import type { Drug, CustomDrug, DrugInteraction, TreatmentGuide, DosageCalcResult, User, SearchHistoryItem, Species, MeasurementUnit } from '../types';

// Define base data first
const species = [
  {
    id: '1',
    name: 'Dog',
    description: 'Domestic dog - man\'s best friend'
  },
  {
    id: '2',
    name: 'Cat',
    description: 'Domestic cat - independent pet'
  },
  {
    id: '3',
    name: 'Horse',
    description: 'Domestic horse - large companion animal'
  },
  {
    id: '4',
    name: 'Rabbit',
    description: 'Domestic rabbit - small herbivorous pet'
  },
  {
    id: '5',
    name: 'Bird',
    description: 'Avian species - various pet birds'
  }
];

const measurementUnits = [
  {
    id: '1',
    name: 'Milligram',
    short_name: 'mg'
  },
  {
    id: '2',
    name: 'Milliliter',
    short_name: 'ml'
  },
  {
    id: '3',
    name: 'Kilogram',
    short_name: 'kg'
  },
  {
    id: '4',
    name: 'International Unit',
    short_name: 'IU'
  },
  {
    id: '5',
    name: 'Microgram',
    short_name: 'μg'
  }
];

const drugs = [
  {
    id: '1',
    name: 'Amoxicillin',
    active_ingredient: 'Amoxicillin',
    species: species[0],
    measurement_value: '10.00000',
    measurement_unit: measurementUnits[0],
    per_weight_value: '1.00000',
    per_weight_unit: measurementUnits[2],
    contraindications: 'Penicillin allergy'
  },
  {
    id: '2',
    name: 'Metacam',
    active_ingredient: 'Meloxicam',
    species: species[0],
    measurement_value: '0.20000',
    measurement_unit: measurementUnits[0],
    per_weight_value: '1.00000',
    per_weight_unit: measurementUnits[2],
    contraindications: 'GI ulcers, renal disease'
  }
];

// Export the complete mockData object
export const mockData = {
  species,
  measurementUnits,
  drugs,
  customDrugs: [
    {
      id: '1',
      name: 'Custom Amoxicillin',
      active_ingredient: 'Amoxicillin',
      species: species[0],
      measurement_value: '15.00000',
      measurement_unit: measurementUnits[0],
      per_weight_value: '1.00000',
      per_weight_unit: measurementUnits[2],
      contraindications: 'Allergy history',
      user_id: '1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  ],
  interactions: [
    {
      id: '1',
      query: 'Amoxicillin + Metacam',
      result: 'No significant interactions found.',
      drugs: [drugs[0], drugs[1]],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  ],
  treatments: [
    {
      id: '1',
      factors: {
        temperature: 39.5,
        heart_rate: 120
      },
      result: 'Possible fever. Consider antibiotics.',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  ],
  searchHistory: [
    {
      id: '1',
      module: 'drug-interaction',
      query: 'Drug interaction query for drug IDs: [1, 2]',
      timestamp: new Date().toISOString()
    }
  ],
  users: [
    {
      id: '1',
      email: 'test@example.com',
      name: 'Test User'
    }
  ]
};

// Helper function to simulate API delay
export const simulateDelay = () => new Promise(resolve => setTimeout(resolve, 500));

// Helper function to generate mock token
export const generateMockToken = (userId: string) => {
  return btoa(`mock_token_${userId}_${Date.now()}`);
};