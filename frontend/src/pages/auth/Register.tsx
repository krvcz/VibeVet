import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Lock, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{
    email?: string;
    name?: string;
    password?: string;
    confirmPassword?: string;
  }>({});
  
  const { register } = useAuth();
  
  const validate = () => {
    const newErrors: {
      email?: string;
      name?: string;
      password?: string;
      confirmPassword?: string;
    } = {};
    
    if (!email.trim()) {
      newErrors.email = 'Email jest wymagany';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Nieprawidłowy format emaila';
    }
    
    if (!name.trim()) {
      newErrors.name = 'Imię jest wymagane';
    }
    
    if (!password) {
      newErrors.password = 'Hasło jest wymagane';
    } else if (password.length < 8) {
      newErrors.password = 'Hasło musi mieć co najmniej 8 znaków';
    }
    
    if (!confirmPassword) {
      newErrors.confirmPassword = 'Potwierdź hasło';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Hasła nie są identyczne';
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
      await register(email, password, confirmPassword);
    } catch (error) {
      // Error is already handled in the register function
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="fade-in">
      <h2 className="text-2xl font-bold text-center text-gray-900 mb-4">
        Utwórz konto
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
          label="Imię i Nazwisko"
          type="text"
          id="name"
          placeholder="Dr Jan Kowalski"
          fullWidth
          value={name}
          onChange={(e) => setName(e.target.value)}
          error={errors.name}
          leftIcon={<User className="h-4 w-4" />}
          autoComplete="name"
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
          autoComplete="new-password"
        />
        
        <Input
          label="Potwierdź Hasło"
          type="password"
          id="confirmPassword"
          placeholder="••••••••"
          fullWidth
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          error={errors.confirmPassword}
          leftIcon={<Lock className="h-4 w-4" />}
          autoComplete="new-password"
        />
        
        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
        >
          Utwórz Konto
        </Button>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Masz już konto?{' '}
            <Link to="/login" className="font-medium text-primary hover:text-primary/80">
              Zaloguj się
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
};

export default Register;