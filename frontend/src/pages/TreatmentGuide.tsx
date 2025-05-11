import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Textarea from '../components/ui/Textarea';
import Button from '../components/ui/Button';
import FeedbackButtons from '../components/FeedbackButtons';
import { BookOpen, PlusCircle, XCircle, Search, BookOpenCheck } from 'lucide-react';
import { treatmentsApi } from '../lib/api/treatments';
import toast from 'react-hot-toast';

interface DiagnosticFactor {
  id: string;
  name: string;
  value: string;
}

interface TreatmentResult {
  id: string;
  result: string;
  factors: { [key: string]: any };
}

const TreatmentGuide: React.FC = () => {
  const [factors, setFactors] = useState<DiagnosticFactor[]>([]);
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [result, setResult] = useState<TreatmentResult | null>(null);
  const [searching, setSearching] = useState(false);
  
  const handleFactorChange = (id: string, value: string) => {
    setFactors(prev => 
      prev.map(factor => 
        factor.id === id ? { ...factor, value } : factor
      )
    );
  };
  
  const addFactor = () => {
    setFactors(prev => [
      ...prev,
      { id: crypto.randomUUID(), name: '', value: '' }
    ]);
  };
  
  const removeFactor = (id: string) => {
    setFactors(prev => prev.filter(factor => factor.id !== id));
  };
  
  const handleNotesChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setAdditionalNotes(e.target.value);
  };
  
  const validate = (): boolean => {
    for (const factor of factors) {
      if (!factor.name.trim()) {
        toast.error('Nazwa czynnika jest wymagana');
        return false;
      }
      
      if (!factor.value.trim()) {
        toast.error('Wartość czynnika jest wymagana');
        return false;
      }
    }
    
    return true;
  };
  
  const findTreatments = async (): Promise<void> => {
    if (!validate()) {
      return;
    }
    
    setSearching(true);
    
    try {
      const diagnosticFactors: { [key: string]: any } = {};
      
      factors.forEach(factor => {
        if (factor.value) {
          diagnosticFactors[factor.name] = factor.value;
        }
      });
      
      if (additionalNotes) {
        diagnosticFactors.additional_notes = additionalNotes;
      }
      
      const response = await treatmentsApi.createTreatmentGuide(diagnosticFactors);
      
      setResult({
        id: response.id,
        result: response.result,
        factors: response.factors
      });
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Nie udało się wygenerować poradnika leczenia');
      }
    } finally {
      setSearching(false);
    }
  };
  
  const handleFeedback = async (feedback: 'up' | 'down') => {
    if (result) {
      try {
        await treatmentsApi.rateTreatmentGuide(result.id, feedback);
        toast.success('Dziękujemy za ocenę');
      } catch (error) {
        toast.error('Nie udało się przesłać oceny');
      }
    }
  };
  
  return (
    <div className="max-w-2xl mx-auto fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Poradnik Leczenia</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-6 w-6 text-accent" />
            <span>Asystent Diagnostyki Różnicowej</span>
          </CardTitle>
          <CardDescription>
            Wprowadź objawy pacjenta i wartości diagnostyczne, aby otrzymać sugestie leczenia wspomagane przez AI.
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium text-gray-700">
                Czynniki Diagnostyczne
              </label>
              {factors.length === 0 && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={addFactor}
                  leftIcon={<PlusCircle className="h-4 w-4" />}
                  size="sm"
                >
                  Dodaj Czynnik
                </Button>
              )}
            </div>
            
            {factors.map((factor) => (
              <div key={factor.id} className="flex items-start space-x-2">
                <div className="flex-1">
                  <Input
                    placeholder="Nazwa czynnika (np. temperatura)"
                    value={factor.name}
                    onChange={(e) => {
                      setFactors(prev =>
                        prev.map(f =>
                          f.id === factor.id ? { ...f, name: e.target.value } : f
                        )
                      );
                    }}
                    fullWidth
                  />
                </div>
                
                <div className="flex-1">
                  <Input
                    placeholder="Wartość (np. 39.5°C)"
                    value={factor.value}
                    onChange={(e) => handleFactorChange(factor.id, e.target.value)}
                    fullWidth
                  />
                </div>
                
                <div className="pt-2">
                  <button
                    type="button"
                    onClick={() => removeFactor(factor.id)}
                    className="text-gray-400 hover:text-error transition-colors"
                    aria-label="Usuń czynnik"
                  >
                    <XCircle className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))}
            
            {factors.length > 0 && (
              <Button
                type="button"
                variant="outline"
                onClick={addFactor}
                leftIcon={<PlusCircle className="h-4 w-4" />}
                size="sm"
              >
                Dodaj Czynnik
              </Button>
            )}
          </div>
          
          <Textarea
            label="Dodatkowe Uwagi (Opcjonalnie)"
            placeholder="Inne istotne informacje o pacjencie"
            value={additionalNotes}
            onChange={handleNotesChange}
            fullWidth
          />
          
          <Button 
            onClick={findTreatments}
            isLoading={searching}
            fullWidth
            className="mt-4"
            leftIcon={<Search className="h-4 w-4" />}
          >
            Znajdź Potencjalne Schorzenia
          </Button>
        </CardContent>
        
        {result && (
          <CardFooter className="flex flex-col items-start border-t pt-6">
            <div className="w-full p-4 rounded-lg mb-4" style={{ backgroundColor: 'rgba(var(--accent), 0.05)' }}>
              <h3 className="font-semibold text-lg flex items-center mb-4">
                <BookOpenCheck className="h-5 w-5 text-accent mr-2" />
                Analiza Diagnostyczna
              </h3>
              
              <div className="space-y-4">
                <div className="text-sm text-gray-700 whitespace-pre-wrap">
                  {result.result}
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

export default TreatmentGuide;