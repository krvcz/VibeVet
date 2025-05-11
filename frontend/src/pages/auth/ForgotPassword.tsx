import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{ email?: string }>({});
  const [submitted, setSubmitted] = useState(false);
  
  const { forgotPassword } = useAuth();
  
  const validate = () => {
    const newErrors: { email?: string } = {};
    
    if (!email.trim()) {
      newErrors.email = 'Email jest wymagany';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Nieprawidłowy format emaila';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      await forgotPassword(email);
      setSubmitted(true);
    } catch (error) {
      // Error is already handled in the forgotPassword function
    } finally {
      setIsLoading(false);
    }
  };
  
  if (submitted) {
    return (
      <div className="text-center fade-in">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Sprawdź swoją skrzynkę
        </h2>
        <p className="text-gray-600 mb-6">
          Wysłaliśmy instrukcje resetowania hasła na adres {email}. Sprawdź swoją skrzynkę odbiorczą.
        </p>
        <Link to="/login" className="inline-block font-medium text-primary hover:text-primary/80">
          Powrót do logowania
        </Link>
      </div>
    );
  }
  
  return (
    <div className="fade-in">
      <h2 className="text-2xl font-bold text-center text-gray-900 mb-4">
        Zresetuj swoje hasło
      </h2>
      <p className="text-center text-gray-600 mb-6">
        Wprowadź swój adres email, a wyślemy Ci link do zresetowania hasła.
      </p>
      
      <form className="space-y-4" onSubmit={handleSubmit}>
        <Input
          label="Adres Email"
          type="email"
          id="email"
          placeholder="twoj@email.com"
          fullWidth
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={errors.email}
          leftIcon={<Mail className="h-4 w-4" />}
          autoComplete="email"
        />
        
        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
        >
          Wyślij Link do Resetowania
        </Button>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Pamiętasz hasło?{' '}
            <Link to="/login" className="font-medium text-primary hover:text-primary/80">
              Zaloguj się
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
};

export default ForgotPassword;