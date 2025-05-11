export interface Drug {
  id: string;
  name: string;
  active_ingredient: string;
  species: {
    id: string;
    name: string;
    description: string;
  };
  measurement_value: string;
  measurement_unit: {
    id: string;
    name: string;
    short_name: string;
  };
  per_weight_value: string;
  per_weight_unit: {
    id: string;
    name: string;
    short_name: string;
  };
  contraindications?: string;
}

export const drugs: Drug[] = [
  {
    id: '1',
    name: 'Amoxicillin',
    active_ingredient: 'Amoxicillin',
    species: {
      id: '1',
      name: 'Dog',
      description: 'Domestic dog - man\'s best friend'
    },
    measurement_value: '10.00000',
    measurement_unit: {
      id: '1',
      name: 'Milligram',
      short_name: 'mg'
    },
    per_weight_value: '1.00000',
    per_weight_unit: {
      id: '3',
      name: 'Kilogram',
      short_name: 'kg'
    },
    contraindications: 'Penicillin allergy'
  },
  {
    id: '2',
    name: 'Metacam',
    active_ingredient: 'Meloxicam',
    species: {
      id: '1',
      name: 'Dog',
      description: 'Domestic dog - man\'s best friend'
    },
    measurement_value: '0.20000',
    measurement_unit: {
      id: '1',
      name: 'Milligram',
      short_name: 'mg'
    },
    per_weight_value: '1.00000',
    per_weight_unit: {
      id: '3',
      name: 'Kilogram',
      short_name: 'kg'
    },
    contraindications: 'GI ulcers, renal disease'
  },
  {
    id: '3',
    name: 'Convenia',
    active_ingredient: 'Cefovecin',
    species: {
      id: '2',
      name: 'Cat',
      description: 'Domestic cat - independent pet'
    },
    measurement_value: '8.00000',
    measurement_unit: {
      id: '1',
      name: 'Milligram',
      short_name: 'mg'
    },
    per_weight_value: '1.00000',
    per_weight_unit: {
      id: '3',
      name: 'Kilogram',
      short_name: 'kg'
    },
    contraindications: 'Cephalosporin allergy'
  }
];