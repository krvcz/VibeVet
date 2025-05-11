import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authApi } from '../lib/api/auth';
import type { User } from '../lib/types';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, confirmPassword: string) => Promise<void>;
  logout: () => void;
  forgotPassword: (email: string) => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>;
  deleteAccount: (password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const navigate = useNavigate();
  const location = useLocation();

  // Check auth status on initial load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      const isAuthRoute = location.pathname.startsWith('/login') || 
                         location.pathname.startsWith('/register') || 
                         location.pathname.startsWith('/forgot-password');

      if (token && !isAuthRoute) {
        try {
          const user = await authApi.getCurrentUser();
          setUser(user);
          setIsAuthenticated(true);
        } catch (error) {
          localStorage.removeItem('token');
          setUser(null);
          setIsAuthenticated(false);
          navigate('/login', { replace: true });
        }
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };
    
    checkAuth();
  }, [navigate, location.pathname]);

  const login = async (email: string, password: string) => {
    try {
      const { token, user } = await authApi.login({ email, password });
      localStorage.setItem('token', token);
      setUser(user);
      setIsAuthenticated(true);
      toast.success('Zalogowano pomyślnie');
      navigate('/', { replace: true });
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message || 'Nieprawidłowy email lub hasło');
      } else {
        toast.error('Nieprawidłowy email lub hasło');
      }
      throw error;
    }
  };

  const register = async (email: string, password: string, confirmPassword: string) => {
    try {
      const { token, user } = await authApi.register({
        email,
        password,
        confirm_password: confirmPassword
      });
      
      localStorage.setItem('token', token);
      setUser(user);
      setIsAuthenticated(true);
      toast.success('Rejestracja zakończona pomyślnie');
      navigate('/', { replace: true });
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message || 'Błąd rejestracji');
      } else {
        toast.error('Błąd rejestracji');
      }
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAuthenticated(false);
    toast.success('Wylogowano pomyślnie');
    navigate('/login', { replace: true });
  };

  const forgotPassword = async (email: string) => {
    try {
      await authApi.forgotPassword(email);
      toast.success('Link do resetowania hasła został wysłany na podany adres email');
      navigate('/login');
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message || 'Nie udało się wysłać linku do resetowania hasła');
      } else {
        toast.error('Nie udało się wysłać linku do resetowania hasła');
      }
      throw error;
    }
  };

  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      await authApi.changePassword({
        current_password: currentPassword,
        new_password: newPassword
      });
      toast.success('Hasło zostało zmienione');
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message || 'Nie udało się zmienić hasła');
      } else {
        toast.error('Nie udało się zmienić hasła');
      }
      throw error;
    }
  };

  const deleteAccount = async (password: string) => {
    try {
      await authApi.deleteAccount(password);
      localStorage.removeItem('token');
      setUser(null);
      setIsAuthenticated(false);
      toast.success('Konto zostało usunięte');
      navigate('/login', { replace: true });
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message || 'Nie udało się usunąć konta');
      } else {
        toast.error('Nie udało się usunąć konta');
      }
      throw error;
    }
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    forgotPassword,
    changePassword,
    deleteAccount
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};