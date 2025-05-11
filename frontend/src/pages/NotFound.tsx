import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, Home } from 'lucide-react';
import Button from '../components/ui/Button';

const NotFound: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] fade-in">
      <AlertCircle className="h-16 w-16 text-error mb-6" />
      
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Strona Nie Znaleziona</h1>
      <p className="text-lg text-gray-600 mb-8 text-center max-w-md">
        Strona, której szukasz nie istnieje lub została przeniesiona.
      </p>
      
      <Button
        as={Link}
        to="/"
        leftIcon={<Home className="h-4 w-4" />}
      >
        Powrót do Strony Głównej
      </Button>
    </div>
  );
};

export default NotFound;