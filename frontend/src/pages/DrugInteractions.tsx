import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import Button from '../components/ui/Button';
import FeedbackButtons from '../components/FeedbackButtons';
import { Activity, AlertCircle, Search, X } from 'lucide-react';
import { drugsApi } from '../lib/api/drugs';
import { interactionsApi } from '../lib/api/interactions';
import toast from 'react-hot-toast';
import type { Drug } from '../lib/types';

interface InteractionFormData {
  selectedDrugs: string[];
}

interface InteractionResult {
  id: string;
  query: string;
  result: {
    severity: string;
    summary: string;
    mechanism: string;
    recommendations: string;
  };
}

const DrugInteractions: React.FC = () => {
  const [formData, setFormData] = useState<InteractionFormData>({
    selectedDrugs: []
  });
  
  const [drugs, setDrugs] = useState<Drug[]>([]);
  const [result, setResult] = useState<InteractionResult | null>(null);
  const [searching, setSearching] = useState(false);
  const [isLoadingDrugs, setIsLoadingDrugs] = useState(true);
  
  useEffect(() => {
    const loadDrugs = async () => {
      try {
        const drugsData = await drugsApi.getDrugs();
        setDrugs(drugsData);
      } catch (error) {
        if (error instanceof Error) {
          toast.error(error.message);
        } else {
          toast.error('Nie udało się załadować leków');
        }
      } finally {
        setIsLoadingDrugs(false);
      }
    };
    
    loadDrugs();
  }, []);
  
  const handleDrugSelection = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = Array.from(e.target.selectedOptions).map(option => option.value);
    setFormData(prev => ({
      ...prev,
      selectedDrugs: selectedOptions
    }));
  };
  
  const validate = (): boolean => {
    if (formData.selectedDrugs.length < 2) {
      toast.error('Wybierz co najmniej dwa leki do sprawdzenia interakcji');
      return false;
    }
    
    return true;
  };
  
  const checkInteractions = async (): Promise<void> => {
    if (!validate()) {
      return;
    }
    
    setSearching(true);
    
    try {
      const response = await interactionsApi.createInteraction({
        drug_ids: formData.selectedDrugs.map(id => parseInt(id))
      });
      
      setResult(response);
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Nie udało się sprawdzić interakcji leków');
      }
    } finally {
      setSearching(false);
    }
  };
  
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'wysoki':
        return 'text-error';
      case 'umiarkowany':
        return 'text-warning';
      case 'niski':
        return 'text-success';
      default:
        return 'text-gray-700';
    }
  };
  
  const handleFeedback = async (feedback: 'up' | 'down') => {
    if (result) {
      try {
        await interactionsApi.rateInteraction(result.id, feedback);
        toast.success('Dziękujemy za ocenę');
      } catch (error) {
        toast.error('Nie udało się przesłać oceny');
      }
    }
  };
  
  if (isLoadingDrugs) {
    return (
      <div className="max-w-2xl mx-auto fade-in">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="max-w-2xl mx-auto fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Interakcje Leków</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-6 w-6 text-secondary" />
            <span>Sprawdź Interakcje Leków</span>
          </CardTitle>
          <CardDescription>
            Wybierz leki, aby sprawdzić potencjalne interakcje, które mogą wpłynąć na leczenie.
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">
              Wybierz Leki
            </label>
            <select
              multiple
              className="w-full min-h-[120px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 input-focus-animation"
              value={formData.selectedDrugs}
              onChange={handleDrugSelection}
            >
              {drugs.map(drug => (
                <option key={drug.id} value={drug.id}>
                  {drug.name} ({drug.active_ingredient})
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500">
              Przytrzymaj Ctrl (Windows) lub Cmd (Mac), aby wybrać wiele leków
            </p>
          </div>
          
          <Button 
            onClick={checkInteractions}
            isLoading={searching}
            fullWidth
            className="mt-4"
            leftIcon={<Search className="h-4 w-4" />}
            disabled={formData.selectedDrugs.length < 2}
          >
            Sprawdź Interakcje
          </Button>
        </CardContent>
        
        {result && (
          <CardFooter className="flex flex-col items-start border-t pt-6">
            <div className="w-full p-4 rounded-lg mb-4" style={{ backgroundColor: 'rgba(var(--secondary), 0.05)' }}>
              <h3 className="font-semibold text-lg flex items-center mb-4">
                <Activity className="h-5 w-5 text-secondary mr-2" />
                Analiza Interakcji: {result.query}
              </h3>
              
              <div className="space-y-4">
                <div className="p-3 rounded-md bg-secondary/10">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle className={`h-5 w-5 ${getSeverityColor(result.result.severity)}`} />
                    <span className={`font-medium ${getSeverityColor(result.result.severity)}`}>
                      Poziom ryzyka: {result.result.severity}
                    </span>
                  </div>
                  <p className="text-gray-700">{result.result.summary}</p>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Mechanizm interakcji:</h4>
                  <p className="text-sm text-gray-700">{result.result.mechanism}</p>
                </div>

                <div className="p-3 rounded-md bg-warning/10">
                  <h4 className="font-medium mb-2">Zalecenia kliniczne:</h4>
                  <p className="text-sm text-gray-700">{result.result.recommendations}</p>
                </div>
              </div>
            </div>
            
            <div className="w-full flex justify-between items-center">
              <span className="text-sm text-gray-500">Czy te informacje były pomocne?</span>
              <FeedbackButtons onFeedback={handleFeedback} size="md" />
            </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default DrugInteractions;