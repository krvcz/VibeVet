import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Button from '../components/ui/Button';
import { Calculator, Pill, HeartPulse } from 'lucide-react';
import { drugsApi } from '../lib/api/drugs';
import { speciesApi } from '../lib/api/species';
import { unitsApi } from '../lib/api/units';
import toast from 'react-hot-toast';
import type { Drug, Species, MeasurementUnit, CustomDrugDto, DrugType } from '../types';

interface DosageFormData {
  drugId: string;
  weight: string;
  speciesId: string;
  targetUnitId: string;
}

interface DosageResult {
  drug: string;
  dose: string;
  unit: string;
  referenceDose: string;
  referenceUnit: string;
  notes?: string;
}

const DosageCalculator: React.FC = () => {
  const [formData, setFormData] = useState<DosageFormData>({
    drugId: '',
    weight: '',
    speciesId: '',
    targetUnitId: ''
  });
  
  const [standardDrugs, setStandardDrugs] = useState<Drug[]>([]);
  const [customDrugs, setCustomDrugs] = useState<CustomDrugDto[]>([]);
  const [speciesList, setSpeciesList] = useState<Species[]>([]);
  const [units, setUnits] = useState<MeasurementUnit[]>([]);
  const [result, setResult] = useState<DosageResult | null>(null);
  const [calculating, setCalculating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [useCustomDrugs, setUseCustomDrugs] = useState(false);
  
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        const [drugsData, customDrugsData, speciesData, unitsData] = await Promise.all([
          drugsApi.getDrugs(),
          drugsApi.getCustomDrugs(),
          speciesApi.getSpecies(),
          unitsApi.getUnits()
        ]);
        
        setStandardDrugs(drugsData);
        setCustomDrugs(customDrugsData.results);
        setSpeciesList(speciesData);
        setUnits(unitsData);
        
        if ((drugsData.length > 0 || customDrugsData.results.length > 0) && speciesData.length > 0 && unitsData.length > 0) {
          setFormData({
            drugId: useCustomDrugs ? customDrugsData.results[0]?.id : drugsData[0]?.id,
            speciesId: speciesData[0].id,
            targetUnitId: unitsData[0].id,
            weight: ''
          });
        }
      } catch (error) {
        if (error instanceof Error) {
          toast.error(error.message);
        } else {
          toast.error('Nie udało się załadować danych');
        }
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const validate = (): boolean => {
    if (!formData.drugId) {
      toast.error('Proszę wybrać lek');
      return false;
    }
    
    if (!formData.weight) {
      toast.error('Proszę podać wagę');
      return false;
    }
    
    const weightNum = parseInt(formData.weight);
    if (isNaN(weightNum) || weightNum <= 0 || weightNum >= 1000) {
      toast.error('Waga musi być liczbą dodatnią mniejszą niż 1000');
      return false;
    }
    
    if (!formData.speciesId) {
      toast.error('Proszę wybrać gatunek');
      return false;
    }
    
    if (!formData.targetUnitId) {
      toast.error('Proszę wybrać jednostkę docelową');
      return false;
    }
    
    return true;
  };
  
  const calculateDosage = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }
    
    setCalculating(true);
    
    try {
      const selectedDrug = useCustomDrugs 
        ? customDrugs.find(drug => drug.id == formData.drugId)
        : standardDrugs.find(drug => drug.id == formData.drugId);

      if (!selectedDrug) {
        throw new Error('Nie znaleziono leku');
      }

      const result = await drugsApi.calculateDosage({
        drug_id: formData.drugId,
        drug_type: useCustomDrugs ? 'custom' : 'standard',
        weight: parseInt(formData.weight),
        species: formData.speciesId,
        target_unit: formData.targetUnitId
      });
      
      const dosageResult: DosageResult = {
        drug: selectedDrug.name,
        dose: result.calculated_dose,
        unit: result.unit,
        referenceDose: `${selectedDrug.measurement_value}`,
        referenceUnit: `${selectedDrug.measurement_unit.short_name}/${selectedDrug.per_weight_unit.short_name}`,
        notes: selectedDrug.contraindications
      };
      
      setResult(dosageResult);
    } catch (error) {
      setResult(null);
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Wystąpił błąd podczas obliczania dawki');
      }
    } finally {
      setCalculating(false);
    }
  };

  const handleDrugTypeToggle = () => {
    setUseCustomDrugs(!useCustomDrugs);
    setFormData(prev => ({
      ...prev,
      drugId: !useCustomDrugs 
        ? (customDrugs[0]?.id || '')
        : (standardDrugs[0]?.id || '')
    }));
    setResult(null);
  };
  
  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto fade-in">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }
  
  const availableDrugs = useCustomDrugs ? customDrugs : standardDrugs;
  
  return (
    <div className="max-w-2xl mx-auto fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Kalkulator Dawkowania</h1>
      
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Calculator className="h-6 w-6 text-primary" />
              <span>Oblicz Dawkę Leku</span>
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              <span className={`text-sm ${!useCustomDrugs ? 'text-primary font-medium' : 'text-gray-500'}`}>
                Standardowe
              </span>
              <button
                type="button"
                role="switch"
                aria-checked={useCustomDrugs}
                onClick={handleDrugTypeToggle}
                className={`
                  relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2
                  ${useCustomDrugs ? 'bg-primary' : 'bg-gray-200'}
                `}
              >
                <span
                  className={`
                    inline-block h-4 w-4 transform rounded-full bg-white transition-transform
                    ${useCustomDrugs ? 'translate-x-6' : 'translate-x-1'}
                  `}
                />
              </button>
              <span className={`text-sm ${useCustomDrugs ? 'text-primary font-medium' : 'text-gray-500'}`}>
                Własne
              </span>
            </div>
          </div>
          <CardDescription>
            Wprowadź dane pacjenta i lek, aby obliczyć odpowiednią dawkę.
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <form onSubmit={calculateDosage} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                label="Wybierz Lek"
                name="drugId"
                value={formData.drugId}
                onChange={(value) => handleInputChange({ target: { name: 'drugId', value } } as any)}
                options={availableDrugs.map(drug => ({ 
                  value: drug.id, 
                  label: `${drug.name} (${drug.active_ingredient})` 
                }))}
                fullWidth
              />
              
              <Input
                label="Waga Zwierzęcia (kg)"
                name="weight"
                type="number"
                min="1"
                max="999"
                placeholder="Wprowadź wagę"
                value={formData.weight}
                onChange={handleInputChange}
                fullWidth
                leftIcon={<HeartPulse className="h-4 w-4" />}
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                label="Gatunek"
                name="speciesId"
                value={formData.speciesId}
                onChange={(value) => handleInputChange({ target: { name: 'speciesId', value } } as any)}
                options={speciesList.map(s => ({ value: s.id, label: s.name }))}
                fullWidth
              />
              
              <Select
                label="Jednostka Docelowa"
                name="targetUnitId"
                value={formData.targetUnitId}
                onChange={(value) => handleInputChange({ target: { name: 'targetUnitId', value } } as any)}
                options={units.map(unit => ({ value: unit.id, label: unit.short_name }))}
                fullWidth
              />
            </div>
            
            <Button 
              type="submit"
              isLoading={calculating}
              fullWidth
              className="mt-4"
              leftIcon={<Calculator className="h-4 w-4" />}
            >
              Oblicz Dawkę
            </Button>
          </form>
        </CardContent>
        
        {result && (
          <CardFooter className="flex flex-col items-start border-t pt-6">
            <div className="w-full p-4 bg-primary/5 rounded-lg">
              <h3 className="font-semibold text-lg flex items-center mb-2">
                <Pill className="h-5 w-5 text-primary mr-2" />
                Obliczona Dawka
              </h3>
              
              <div className="flex flex-col space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Lek:</span>
                  <span className="font-medium">{result.drug}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-gray-600">Dawka referencyjna:</span>
                  <span className="font-medium">{result.referenceDose} {result.referenceUnit}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-gray-600">Obliczona dawka:</span>
                  <span className="font-medium text-lg text-primary">{result.dose} {result.unit}</span>
                </div>
                
                {result.notes && (
                  <div className="mt-2 pt-2 border-t border-gray-200">
                    <span className="text-gray-600 block mb-1">Uwagi:</span>
                    <p className="text-sm text-gray-700">{result.notes}</p>
                  </div>
                )}
              </div>
            </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default DosageCalculator;