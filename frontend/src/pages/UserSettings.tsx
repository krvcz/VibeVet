import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import { Settings, Lock, User, Trash2, History } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import SearchHistoryList from '../components/SearchHistoryList';

interface PasswordFormData {
  currentPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}

interface DeleteAccountFormData {
  password: string;
  confirmText: string;
}

const UserSettings: React.FC = () => {
  const { user, changePassword, deleteAccount } = useAuth();
  
  const [passwordData, setPasswordData] = useState<PasswordFormData>({
    currentPassword: '',
    newPassword: '',
    confirmNewPassword: ''
  });
  
  const [deleteData, setDeleteData] = useState<DeleteAccountFormData>({
    password: '',
    confirmText: ''
  });
  
  const [passwordErrors, setPasswordErrors] = useState<{ [key: string]: string }>({});
  const [deleteErrors, setDeleteErrors] = useState<{ [key: string]: string }>({});
  
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'history'>('profile');
  
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    setPasswordData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (passwordErrors[name]) {
      setPasswordErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };
  
  const handleDeleteChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    setDeleteData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (deleteErrors[name]) {
      setDeleteErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };
  
  const validatePasswordForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};
    
    if (!passwordData.currentPassword) {
      newErrors.currentPassword = 'Aktualne hasło jest wymagane';
    }
    
    if (!passwordData.newPassword) {
      newErrors.newPassword = 'Nowe hasło jest wymagane';
    } else if (passwordData.newPassword.length < 8) {
      newErrors.newPassword = 'Nowe hasło musi mieć co najmniej 8 znaków';
    }
    
    if (!passwordData.confirmNewPassword) {
      newErrors.confirmNewPassword = 'Potwierdź nowe hasło';
    } else if (passwordData.newPassword !== passwordData.confirmNewPassword) {
      newErrors.confirmNewPassword = 'Hasła nie są identyczne';
    }
    
    setPasswordErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const validateDeleteForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};
    
    if (!deleteData.password) {
      newErrors.password = 'Hasło jest wymagane do potwierdzenia usunięcia';
    }
    
    if (deleteData.confirmText !== 'DELETE') {
      newErrors.confirmText = 'Wpisz DELETE aby potwierdzić';
    }
    
    setDeleteErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validatePasswordForm()) {
      return;
    }
    
    setIsChangingPassword(true);
    
    try {
      await changePassword(passwordData.currentPassword, passwordData.newPassword);
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      });
    } finally {
      setIsChangingPassword(false);
    }
  };
  
  const handleDeleteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateDeleteForm()) {
      return;
    }
    
    setIsDeletingAccount(true);
    
    try {
      await deleteAccount(deleteData.password);
    } finally {
      setIsDeletingAccount(false);
    }
  };
  
  return (
    <div className="max-w-3xl mx-auto fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Ustawienia Konta</h1>
      
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8" aria-label="Zakładki">
            <button
              onClick={() => setActiveTab('profile')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'profile'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <User className="w-4 h-4 inline mr-2" />
              Profil
            </button>
            <button
              onClick={() => setActiveTab('security')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'security'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Lock className="w-4 h-4 inline mr-2" />
              Bezpieczeństwo
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'history'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <History className="w-4 h-4 inline mr-2" />
              Historia Wyszukiwania
            </button>
          </nav>
        </div>
      </div>
      
      {activeTab === 'profile' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-6 w-6 text-primary" />
              <span>Informacje o Profilu</span>
            </CardTitle>
            <CardDescription>
              Zaktualizuj informacje o swoim koncie
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="rounded-full bg-primary w-16 h-16 flex items-center justify-center text-white text-2xl font-bold">
                {user?.name ? user.name[0] : 'U'}
              </div>
              
              <div>
                <h3 className="font-medium">{user?.name || 'Użytkownik'}</h3>
                <p className="text-sm text-gray-500">{user?.email}</p>
              </div>
            </div>
            
            <div className="border-t pt-4 mt-4">
              <p className="text-sm text-gray-500 mb-4">
                Edycja profilu nie jest dostępna w wersji MVP.
              </p>
              
              <Button variant="outline" disabled>
                Edytuj Profil
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
      
      {activeTab === 'security' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lock className="h-6 w-6 text-primary" />
                <span>Zmiana Hasła</span>
              </CardTitle>
              <CardDescription>
                Zaktualizuj hasło do swojego konta, aby zapewnić jego bezpieczeństwo
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <form onSubmit={handlePasswordSubmit} className="space-y-4">
                <Input
                  label="Aktualne Hasło"
                  type="password"
                  name="currentPassword"
                  placeholder="Wprowadź aktualne hasło"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  error={passwordErrors.currentPassword}
                  fullWidth
                />
                
                <Input
                  label="Nowe Hasło"
                  type="password"
                  name="newPassword"
                  placeholder="Wprowadź nowe hasło"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  error={passwordErrors.newPassword}
                  fullWidth
                />
                
                <Input
                  label="Potwierdź Nowe Hasło"
                  type="password"
                  name="confirmNewPassword"
                  placeholder="Potwierdź nowe hasło"
                  value={passwordData.confirmNewPassword}
                  onChange={handlePasswordChange}
                  error={passwordErrors.confirmNewPassword}
                  fullWidth
                />
                
                <Button
                  type="submit"
                  isLoading={isChangingPassword}
                >
                  Aktualizuj Hasło
                </Button>
              </form>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-error">
                <Trash2 className="h-6 w-6" />
                <span>Usuń Konto</span>
              </CardTitle>
              <CardDescription>
                Trwale usuń swoje konto i wszystkie powiązane dane
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="p-4 bg-error/10 border border-error/20 rounded-md mb-4">
                <p className="text-sm text-gray-700">
                  <strong>Uwaga:</strong> Ta operacja nie może zostać cofnięta. Wszystkie Twoje dane, w tym zapisane leki, historia wyszukiwania i ustawienia zostaną trwale usunięte.
                </p>
              </div>
              
              <form onSubmit={handleDeleteSubmit} className="space-y-4">
                <Input
                  label="Wprowadź hasło, aby potwierdzić"
                  type="password"
                  name="password"
                  placeholder="Twoje aktualne hasło"
                  value={deleteData.password}
                  onChange={handleDeleteChange}
                  error={deleteErrors.password}
                  fullWidth
                />
                
                <Input
                  label="Wpisz DELETE, aby potwierdzić"
                  type="text"
                  name="confirmText"
                  placeholder="DELETE"
                  value={deleteData.confirmText}
                  onChange={handleDeleteChange}
                  error={deleteErrors.confirmText}
                  fullWidth
                />
                
                <Button
                  type="submit"
                  variant="danger"
                  isLoading={isDeletingAccount}
                >
                  Trwale Usuń Konto
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
      
      {activeTab === 'history' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-6 w-6 text-primary" />
              <span>Historia Wyszukiwania</span>
            </CardTitle>
            <CardDescription>
              Przeglądaj i zarządzaj swoimi poprzednimi wyszukiwaniami
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            <SearchHistoryList showFilterButtons showClearButton />
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default UserSettings;