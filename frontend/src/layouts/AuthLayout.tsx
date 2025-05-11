import React, { useEffect } from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Pill } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const AuthLayout: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Link to="/" className="flex justify-center items-center">
          <Pill className="h-12 w-12 text-primary" />
        </Link>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          VetAssist
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Twój asystent w praktyce weterynaryjnej
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;