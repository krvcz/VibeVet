import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import Select from '../components/ui/Select';
import Textarea from '../components/ui/Textarea';
import Button from '../components/ui/Button';
import FeedbackButtons from '../components/FeedbackButtons';
import { Activity, AlertCircle, Search } from 'lucide-react';
import { drugsApi } from '../lib/api/drugs';
import { interactionsApi } from '../lib/api/interactions';
import toast from 'react-hot-toast';
import type { Drug } from '../lib/types';

interface InteractionFormData {
  selectedDrugs: string[];
  context: string;
}

interface InteractionResult {
  id: string;
  summary: string;
  details: string;
}

const DrugInteractions: React.FC = () => {
  const [formData, setFormData] = useState<InteractionFormData>({
    selectedDrugs: [],
    context: ''
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
  
  const drugOptions = drugs.map(drug => ({
    value: drug.id,
    label: `${drug.name} (${drug.active_ingredient})`
  }));
  
  const handleDrugSelectionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const options = e.target.options;
    const selectedValues: string[] = [];
    
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selectedValues.push(options[i].value);
      }
    }
    
    setFormData(prev => ({
      ...prev,
      selectedDrugs: selectedValues
    }));
  };
  
  const handleContextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      context: e.target.value
    }));
  };
  
  const validate = (): boolean => {
    if (formData.selectedDrugs.length < 2) {
      toast.error('Wybierz co najmniej dwa leki do sprawdzenia interakcji');
      return false;
    }
    
    if (formData.context && formData.context.length > 50) {
      toast.error('Kontekst nie może przekraczać 50 znaków');
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
        drug_ids: formData.selectedDrugs.map(id => parseInt(id)),
        context: formData.context || undefined
      });
      
      const [summary, ...details] = response.result.split('\n\n');
      
      const interactionResult: InteractionResult = {
        id: response.id,
        summary: summary.trim(),
        details: details.join('\n\n').trim()
      };
      
      setResult(interactionResult);
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
            Wybierz kilka leków, aby sprawdzić potencjalne interakcje, które mogą wpłynąć na leczenie.
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">
              Wybierz Leki
            </label>
            <select
              multiple
              className="w-full min-h-[120px] rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 input-focus-animation"
              onChange={handleDrugSelectionChange}
              value={formData.selectedDrugs}
            >
              {drugOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500">
              Przytrzymaj Ctrl (PC) lub Cmd (Mac), aby wybrać wiele leków
            </p>
          </div>
          
          <Textarea
            label="Dodatkowy Kontekst (Opcjonalnie)"
            name="context"
            placeholder="Szczególne okoliczności lub uwagi (max 50 znaków)"
            value={formData.context}
            onChange={handleContextChange}
            fullWidth
          />
          
          <Button 
            onClick={checkInteractions}
            isLoading={searching}
            fullWidth
            className="mt-4"
            leftIcon={<Search className="h-4 w-4" />}
          >
            Sprawdź Interakcje
          </Button>
        </CardContent>
        
        {result && (
          <CardFooter className="flex flex-col items-start border-t pt-6">
            <div className="w-full p-4 rounded-lg mb-4" style={{ backgroundColor: 'rgba(var(--secondary), 0.05)' }}>
              <h3 className="font-semibold text-lg flex items-center mb-2">
                <Activity className="h-5 w-5 text-secondary mr-2" />
                Analiza Interakcji
              </h3>
              
              <div className="flex flex-col space-y-4">
                <div className="p-3 rounded-md bg-secondary/10">
                  <div className="flex items-center gap-2 font-medium text-secondary">
                    <AlertCircle className="h-4 w-4" />
                    {result.summary}
                  </div>
                </div>
                
                {result.details && (
                  <div>
                    <h4 className="font-medium mb-1">Szczegóły:</h4>
                    <p className="text-sm text-gray-700 whitespace-pre-wrap">{result.details}</p>
                  </div>
                )}
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