import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Layouts
import Layout from './layouts/Layout';
import AuthLayout from './layouts/AuthLayout';

// Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import DosageCalculator from './pages/DosageCalculator';
import DrugInteractions from './pages/DrugInteractions';
import TreatmentGuide from './pages/TreatmentGuide';
import UserSettings from './pages/UserSettings';
import CustomDrugs from './pages/CustomDrugs';
import NotFound from './pages/NotFound';

// State provider
import { AuthProvider } from './context/AuthContext';
import { SearchHistoryProvider } from './context/SearchHistoryContext';

function App() {
  return (
    <Router>
      <AuthProvider>
        <SearchHistoryProvider>
          <Toaster position="top-right" />
          <Routes>
            {/* Auth routes */}
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
            </Route>
            
            {/* Protected routes */}
            <Route element={<Layout />}>
              <Route index element={<Navigate to="/dosage-calculator" replace />} />
              <Route path="/dosage-calculator" element={<DosageCalculator />} />
              <Route path="/drug-interactions" element={<DrugInteractions />} />
              <Route path="/treatment-guide" element={<TreatmentGuide />} />
              <Route path="/settings" element={<UserSettings />} />
              <Route path="/custom-drugs" element={<CustomDrugs />} />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </SearchHistoryProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;