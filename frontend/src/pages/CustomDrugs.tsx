import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Button from '../components/ui/Button';
import { Beaker, Plus, Edit, Trash2, Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { drugsApi } from '../lib/api/drugs';
import { speciesApi } from '../lib/api/species';
import { unitsApi } from '../lib/api/units';
import toast from 'react-hot-toast';
import type { CustomDrugDto, CreateCustomDrugDto, Species, MeasurementUnit } from '../lib/types';

interface PaginationData {
  count: number;
  next: string | null;
  previous: string | null;
}

const ITEMS_PER_PAGE = 20;
const SEARCH_DEBOUNCE_MS = 300;

const CustomDrugs: React.FC = () => {
  const [customDrugs, setCustomDrugs] = useState<CustomDrugDto[]>([]);
  const [species, setSpecies] = useState<Species[]>([]);
  const [units, setUnits] = useState<MeasurementUnit[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentDrug, setCurrentDrug] = useState<CreateCustomDrugDto & { id?: string }>({
    name: '',
    active_ingredient: '',
    species: '',
    measurement_value: '',
    measurement_unit: '',
    per_weight_value: '',
    per_weight_unit: '',
    contraindications: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(true);
  
  const [pagination, setPagination] = useState<PaginationData>({
    count: 0,
    next: null,
    previous: null
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTimeout, setSearchTimeout] = useState<NodeJS.Timeout | null>(null);
  
  const loadCustomDrugs = useCallback(async (page: number = 1, search?: string) => {
    try {
      const response = await drugsApi.getCustomDrugs(search, page);
      setCustomDrugs(response.results);
      setPagination({
        count: response.count,
        next: response.next,
        previous: response.previous
      });
      setCurrentPage(page);
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Nie udało się załadować własnych leków');
      }
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoadingData(true);
        
        const [speciesData, unitsData] = await Promise.all([
          speciesApi.getSpecies(),
          unitsApi.getUnits()
        ]);
        
        setSpecies(speciesData);
        setUnits(unitsData);
        
        if (speciesData.length > 0 && unitsData.length > 0) {
          setCurrentDrug(prev => ({
            ...prev,
            species: speciesData[0].id,
            measurement_unit: unitsData[0].id,
            per_weight_unit: unitsData[0].id
          }));
        }
        
        await loadCustomDrugs();
      } catch (error) {
        if (error instanceof Error) {
          toast.error(error.message);
        } else {
          toast.error('Nie udało się załadować danych');
        }
      } finally {
        setIsLoadingData(false);
      }
    };
    
    loadData();
  }, [loadCustomDrugs]);

  const handlePageChange = (newPage: number) => {
    loadCustomDrugs(newPage, searchTerm);
  };

  const calculateTotalPages = () => {
    return Math.ceil(pagination.count / ITEMS_PER_PAGE);
  };

  const totalPages = calculateTotalPages();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;

    if (name === 'measurement_value' || name === 'per_weight_value') {
      const parts = value.split('.');
      if (parts.length > 1 && parts[1].length > 5) {
        return;
      }
    }
    
    setCurrentDrug(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const validate = (): boolean => {
    if (!currentDrug.name.trim()) {
      toast.error('Nazwa leku jest wymagana');
      return false;
    }
    
    if (currentDrug.name.length > 20) {
      toast.error('Nazwa nie może przekraczać 20 znaków');
      return false;
    }
    
    if (!currentDrug.active_ingredient.trim()) {
      toast.error('Składnik aktywny jest wymagany');
      return false;
    }
    
    if (currentDrug.active_ingredient.length > 20) {
      toast.error('Składnik aktywny nie może przekraczać 20 znaków');
      return false;
    }
    
    if (!currentDrug.species) {
      toast.error('Gatunek jest wymagany');
      return false;
    }
    
    if (!currentDrug.measurement_value.trim()) {
      toast.error('Wartość dawki jest wymagana');
      return false;
    }
    
    if (isNaN(parseFloat(currentDrug.measurement_value))) {
      toast.error('Wartość dawki musi być liczbą');
      return false;
    }

    const measurementParts = currentDrug.measurement_value.split('.');
    if (measurementParts.length > 1 && measurementParts[1].length > 5) {
      toast.error('Wartość dawki nie może mieć więcej niż 5 miejsc po przecinku');
      return false;
    }
    
    if (!currentDrug.measurement_unit) {
      toast.error('Jednostka dawki jest wymagana');
      return false;
    }

    if (!currentDrug.per_weight_value.trim()) {
      toast.error('Wartość na kg jest wymagana');
      return false;
    }
    
    if (isNaN(parseFloat(currentDrug.per_weight_value))) {
      toast.error('Wartość na kg musi być liczbą');
      return false;
    }

    const perWeightParts = currentDrug.per_weight_value.split('.');
    if (perWeightParts.length > 1 && perWeightParts[1].length > 5) {
      toast.error('Wartość na kg nie może mieć więcej niż 5 miejsc po przecinku');
      return false;
    }
    
    if (!currentDrug.per_weight_unit) {
      toast.error('Jednostka na kg jest wymagana');
      return false;
    }
    
    if (currentDrug.contraindications && currentDrug.contraindications.length > 100) {
      toast.error('Przeciwwskazania nie mogą przekraczać 100 znaków');
      return false;
    }
    
    return true;
  };
  
  const handleAddDrug = async () => {
    if (!validate()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      if (currentDrug.id) {
        await drugsApi.updateCustomDrug(currentDrug.id, currentDrug);
        toast.success('Lek został zaktualizowany');
      } else {
        await drugsApi.createCustomDrug(currentDrug);
        toast.success('Lek został dodany');
      }
      
      await loadCustomDrugs(currentPage, searchTerm);
      
      setCurrentDrug({
        name: '',
        active_ingredient: '',
        species: species[0]?.id || '',
        measurement_value: '',
        measurement_unit: units[0]?.id || '',
        per_weight_value: '',
        per_weight_unit: units[0]?.id || '',
        contraindications: ''
      });
      
      setIsEditing(false);
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Nie udało się zapisać leku');
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleEditDrug = (drug: CustomDrugDto) => {
    setCurrentDrug({
      id: drug.id,
      name: drug.name,
      active_ingredient: drug.active_ingredient,
      species: drug.species.id,
      measurement_value: drug.measurement_value,
      measurement_unit: drug.measurement_unit.id,
      per_weight_value: drug.per_weight_value,
      per_weight_unit: drug.per_weight_unit.id,
      contraindications: drug.contraindications || ''
    });
    setIsEditing(true);
  };
  
  const handleDeleteDrug = async (id: string) => {
    if (window.confirm('Czy na pewno chcesz usunąć ten lek?')) {
      setIsLoading(true);
      
      try {
        await drugsApi.deleteCustomDrug(id);
        await loadCustomDrugs(currentPage, searchTerm);
        toast.success('Lek został usunięty');
      } catch (error) {
        if (error instanceof Error) {
          toast.error(error.message);
        } else {
          toast.error('Nie udało się usunąć leku');
        }
      } finally {
        setIsLoading(false);
      }
    }
  };
  
  const handleCancelEdit = () => {
    setCurrentDrug({
      name: '',
      active_ingredient: '',
      species: species[0]?.id || '',
      measurement_value: '',
      measurement_unit: units[0]?.id || '',
      per_weight_value: '',
      per_weight_unit: units[0]?.id || '',
      contraindications: ''
    });
    
    setIsEditing(false);
  };

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    
    const timeoutId = setTimeout(() => {
      loadCustomDrugs(1, value || undefined);
    }, SEARCH_DEBOUNCE_MS);
    
    setSearchTimeout(timeoutId);
  };
  
  if (isLoadingData) {
    return (
      <div className="max-w-4xl mx-auto fade-in">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto fade-in">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Własne Leki</h1>
        
        {!isEditing && (
          <Button 
            onClick={() => setIsEditing(true)}
            leftIcon={<Plus className="h-4 w-4" />}
          >
            Dodaj Własny Lek
          </Button>
        )}
      </div>
      
      {isEditing ? (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Beaker className="h-6 w-6 text-primary" />
              <span>{currentDrug.id ? 'Edytuj' : 'Dodaj'} Własny Lek</span>
            </CardTitle>
            <CardDescription>
              {currentDrug.id ? 'Zaktualizuj szczegóły własnego leku' : 'Zdefiniuj nowy lek dla swojej praktyki'}
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <Input
                label="Nazwa Leku"
                name="name"
                placeholder="Wprowadź nazwę leku"
                value={currentDrug.name}
                onChange={handleInputChange}
                fullWidth
              />
              
              <Input
                label="Składnik Aktywny"
                name="active_ingredient"
                placeholder="Wprowadź składnik aktywny"
                value={currentDrug.active_ingredient}
                onChange={handleInputChange}
                fullWidth
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <Select
                label="Gatunek"
                name="species"
                value={currentDrug.species}
                onChange={(value) => handleInputChange({ target: { name: 'species', value } } as any)}
                options={species.map(s => ({ value: s.id, label: s.name }))}
                fullWidth
              />
              
              <div className="grid grid-cols-2 gap-2">
                <Input
                  label="Wartość Dawki"
                  name="measurement_value"
                  type="number"
                  step="0.00001"
                  placeholder="Wprowadź wartość"
                  value={currentDrug.measurement_value}
                  onChange={handleInputChange}
                  fullWidth
                />
                
                <Select
                  label="Jednostka"
                  name="measurement_unit"
                  value={currentDrug.measurement_unit}
                  onChange={(value) => handleInputChange({ target: { name: 'measurement_unit', value } } as any)}
                  options={units.map(unit => ({ value: unit.id, label: unit.short_name }))}
                  fullWidth
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="grid grid-cols-2 gap-2">
                <Input
                  label="Wartość na kg"
                  name="per_weight_value"
                  type="number"
                  step="0.00001"
                  placeholder="Wprowadź wartość"
                  value={currentDrug.per_weight_value}
                  onChange={handleInputChange}
                  fullWidth
                />
                
                <Select
                  label="Jednostka na kg"
                  name="per_weight_unit"
                  value={currentDrug.per_weight_unit}
                  onChange={(value) => handleInputChange({ target: { name: 'per_weight_unit', value } } as any)}
                  options={units.map(unit => ({ value: unit.id, label: unit.short_name }))}
                  fullWidth
                />
              </div>
              
              <Input
                label="Przeciwwskazania (Opcjonalnie)"
                name="contraindications"
                placeholder="Wprowadź przeciwwskazania"
                value={currentDrug.contraindications || ''}
                onChange={handleInputChange}
                fullWidth
              />
            </div>
            
            <div className="flex space-x-2">
              <Button
                onClick={handleAddDrug}
                isLoading={isLoading}
                leftIcon={currentDrug.id ? <Edit className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
              >
                {currentDrug.id ? 'Aktualizuj Lek' : 'Dodaj Lek'}
              </Button>
              
              <Button
                variant="outline"
                onClick={handleCancelEdit}
                disabled={isLoading}
              >
                Anuluj
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="mb-6">
          <div className="relative">
            <Input
              placeholder="Szukaj leków..."
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              fullWidth
              leftIcon={<Search className="h-4 w-4" />}
            />
          </div>
        </div>
      )}
      
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="min-w-full divide-y divide-gray-200">
          <div className="bg-gray-50">
            <div className="grid grid-cols-12 divide-x divide-gray-200">
              <div className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider col-span-2">
                Lek
              </div>
              <div className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider col-span-2">
                Gatunek
              </div>
              <div className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider col-span-3">
                Dawkowanie
              </div>
              <div className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider col-span-4">
                Przeciwwskazania
              </div>
              <div className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider col-span-1">
                Akcje
              </div>
            </div>
          </div>
          
          <div className="bg-white divide-y divide-gray-200">
            {customDrugs.length === 0 ? (
              <div className="px-6 py-4 text-center text-sm text-gray-500 col-span-12">
                {searchTerm ? 'Nie znaleziono leków pasujących do wyszukiwania.' : 'Nie dodano jeszcze własnych leków.'}
              </div>
            ) : (
              customDrugs.map(drug => (
                <div key={drug.id} className="grid grid-cols-12 divide-x divide-gray-200 hover:bg-gray-50">
                  <div className="px-6 py-4 text-sm text-gray-900 col-span-2">
                    <div className="font-medium truncate">{drug.name}</div>
                    <div className="text-gray-500 text-xs mt-1 truncate">{drug.active_ingredient}</div>
                  </div>
                  <div className="px-6 py-4 text-sm text-gray-900 col-span-2">
                    <div className="truncate">{drug.species.name}</div>
                  </div>
                  <div className="px-6 py-4 text-sm text-gray-900 col-span-3">
                    <div>{drug.measurement_value} {drug.measurement_unit.short_name}/{drug.per_weight_value} {drug.per_weight_unit.short_name}</div>
                  </div>
                  <div className="px-6 py-4 text-sm text-gray-900 col-span-4 truncate">
                    {drug.contraindications || 'Brak'}
                  </div>
                  <div className="px-6 py-4 text-sm text-gray-900 col-span-1 flex space-x-2">
                    <button
                      onClick={() => handleEditDrug(drug)}
                      className="text-primary hover:text-primary/80 transition-colors"
                      aria-label={`Edytuj ${drug.name}`}
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteDrug(drug.id)}
                      className="text-error hover:text-error/80 transition-colors"
                      aria-label={`Usuń ${drug.name}`}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        {customDrugs.length > 0 && (
          <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
            <div className="flex-1 flex justify-between sm:hidden">
              <Button
                variant="outline"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={!pagination.previous}
              >
                Poprzednia
              </Button>
              <Button
                variant="outline"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={!pagination.next}
              >
                Następna
              </Button>
            </div>
            
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Pokazuje <span className="font-medium">{((currentPage - 1) * ITEMS_PER_PAGE) + 1}</span>-
                  <span className="font-medium">
                    {Math.min(currentPage * ITEMS_PER_PAGE, pagination.count)}
                  </span> z{' '}
                  <span className="font-medium">{pagination.count}</span> wyników
                </p>
              </div>
              
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={!pagination.previous}
                  leftIcon={<ChevronLeft className="h-4 w-4" />}
                >
                  Poprzednia
                </Button>
                
                <div className="flex items-center space-x-2">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                    <Button
                      key={page}
                      variant={page === currentPage ? 'primary' : 'outline'}
                      size="sm"
                      onClick={() => handlePageChange(page)}
                    >
                      {page}
                    </Button>
                  ))}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={!pagination.next}
                  rightIcon={<ChevronRight className="h-4 w-4" />}
                >
                  Następna
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomDrugs;