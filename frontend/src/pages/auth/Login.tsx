import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Lock } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  
  const { login } = useAuth();
  
  const validate = () => {
    const newErrors: { email?: string; password?: string } = {};
    
    if (!email.trim()) {
      newErrors.email = 'Email jest wymagany';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Nieprawidłowy format emaila';
    }
    
    if (!password) {
      newErrors.password = 'Hasło jest wymagane';
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
      await login(email, password);
    } catch (error) {
      // Error is already handled in the login function
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="fade-in">
      <h2 className="text-2xl font-bold text-center text-gray-900 mb-4">
        Zaloguj się do swojego konta
      </h2>
      
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
        
        <Input
          label="Hasło"
          type="password"
          id="password"
          placeholder="••••••••"
          fullWidth
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={errors.password}
          leftIcon={<Lock className="h-4 w-4" />}
          autoComplete="current-password"
        />
        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
              Zapamiętaj mnie
            </label>
          </div>
          
          <Link to="/forgot-password" className="text-sm font-medium text-primary hover:text-primary/80">
            Zapomniałeś hasła?
          </Link>
        </div>
        
        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
        >
          Zaloguj się
        </Button>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Nie masz konta?{' '}
            <Link to="/register" className="font-medium text-primary hover:text-primary/80">
              Zarejestruj się
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
};

export default Login;