import React, { useState } from 'react';
import { Outlet, useLocation, Link, Navigate } from 'react-router-dom';
import { 
  Pill, 
  Activity, 
  BookOpen, 
  Settings, 
  Beaker,
  Menu, 
  X,
  LogOut 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Layout: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  const navigationItems = [
    { name: 'Kalkulator Dawkowania', href: '/dosage-calculator', icon: <Pill className="w-5 h-5" /> },
    { name: 'Interakcje Leków', href: '/drug-interactions', icon: <Activity className="w-5 h-5" /> },
    { name: 'Poradnik Leczenia', href: '/treatment-guide', icon: <BookOpen className="w-5 h-5" /> },
    { name: 'Własne Leki', href: '/custom-drugs', icon: <Beaker className="w-5 h-5" /> },
    { name: 'Ustawienia', href: '/settings', icon: <Settings className="w-5 h-5" /> },
  ];

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            {/* Logo and brand */}
            <div className="flex-shrink-0">
              <Link to="/" className="flex items-center space-x-2">
                <Pill className="h-8 w-8 text-primary" />
                <span className="text-xl font-bold text-primary hidden sm:inline">VetAssist</span>
              </Link>
            </div>

            {/* Desktop navigation */}
            <nav className="hidden lg:flex items-center">
              <div className="flex items-center space-x-1 xl:space-x-2">
                {navigationItems.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-2 xl:px-3 py-2 rounded-md text-sm font-medium transition-colors whitespace-nowrap ${
                      location.pathname === item.href
                        ? 'bg-primary text-white'
                        : 'text-gray-600 hover:text-primary hover:bg-gray-100'
                    }`}
                  >
                    {item.icon}
                    <span className="ml-1.5 xl:ml-2">{item.name}</span>
                  </Link>
                ))}
              </div>
              <div className="ml-1 xl:ml-2 pl-1 xl:pl-2 border-l border-gray-200">
                <button 
                  onClick={logout}
                  className="flex items-center px-2 xl:px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-primary hover:bg-gray-100 transition-colors whitespace-nowrap"
                >
                  <LogOut className="w-5 h-5" />
                  <span className="ml-1.5 xl:ml-2">Wyloguj</span>
                </button>
              </div>
            </nav>

            {/* Mobile menu button */}
            <div className="lg:hidden">
              <button
                onClick={toggleMobileMenu}
                className="text-gray-600 hover:text-primary focus:outline-none p-2"
                aria-label="Przełącz menu"
              >
                {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        <div className={`${mobileMenuOpen ? 'block' : 'hidden'} lg:hidden`}>
          <div className="px-2 pt-2 pb-3 space-y-1 bg-white shadow-md border-t border-gray-200">
            {navigationItems.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-3 py-2 rounded-md text-base font-medium ${
                  location.pathname === item.href
                    ? 'bg-primary text-white'
                    : 'text-gray-600 hover:text-primary hover:bg-gray-100'
                }`}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.icon}
                <span className="ml-3">{item.name}</span>
              </Link>
            ))}
            <button 
              onClick={() => { setMobileMenuOpen(false); logout(); }}
              className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-primary hover:bg-gray-100"
            >
              <LogOut className="w-5 h-5" />
              <span className="ml-3">Wyloguj</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-gray-500">
            <p>© 2025 VetAssist. Wszelkie prawa zastrzeżone.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;