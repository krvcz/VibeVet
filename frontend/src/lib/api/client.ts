import axios from 'axios';
import toast from 'react-hot-toast';
import { handleApiError, AppError, getErrorMessage } from '../../utils/apiErrors';

// Check if we're in debug mode
const isDebugMode = import.meta.env.VITE_DEBUG === 'YES';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  withXSRFToken: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

// Add request interceptor for auth
// apiClient.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token');
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   console.log('API Request:', config); // Add request logging
//   return config;
// });

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response); // Add response logging
    return response;
  },
  (error) => {
    console.error('API Error:', error); // Add error logging
    const appError = handleApiError(error);
    
    // Don't show toast for 401 errors as they're handled by the auth service
    if (appError.statusCode !== 401) {
      toast.error(getErrorMessage(appError));
    }
    
    return Promise.reject(appError);
  }
);

export { isDebugMode };