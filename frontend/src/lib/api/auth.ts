import { apiClient, isDebugMode } from './client';
import { mockData, simulateDelay } from './mockData';
import type { User, LoginCredentials, RegisterData } from '../types';

export const authApi = {
  // Login user
  login: async (credentials: LoginCredentials) => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        // Mock authentication logic
        const user = mockData.users.find(u => u.email === credentials.email);
        if (!user || credentials.password !== 'password') {
          throw new Error('Invalid email or password');
        }
        
        const token = generateMockToken(user.id);
        return { token, user };
      }
      
      const response = await apiClient.post<{ token: string; user: User }>('/auth/login/', credentials);
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },

  // Register user
  register: async (data: RegisterData) => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        // Check if user exists
        if (mockData.users.some(u => u.email === data.email)) {
          throw new Error('Email already registered');
        }
        
        // Create new user
        const newUser = {
          id: String(mockData.users.length + 1),
          email: data.email,
          first_name: data.name?.split(' ')[0],
          last_name: data.name?.split(' ')[1]
        };
        
        mockData.users.push(newUser);
        const token = generateMockToken(newUser.id);
        
        return { token, user: newUser };
      }
      
      const response = await apiClient.post<{ token: string; user: User }>('/auth/register/', data);
      return response.data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token found');
        }
        
        // In mock mode, always return the first user
        return mockData.users[0];
      }
      
      const response = await apiClient.get<User>('/auth/me/');
      return response.data;
    } catch (error) {
      console.error('Failed to get current user:', error);
      throw error;
    }
  },

  // Change password
  changePassword: async (data: { current_password: string; new_password: string }) => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        if (data.current_password !== 'password') {
          throw new Error('Current password is incorrect');
        }
        
        return { message: 'Password changed successfully' };
      }
      
      const response = await apiClient.post('/auth/change-password/', data);
      return response.data;
    } catch (error) {
      console.error('Failed to change password:', error);
      throw error;
    }
  },

  // Request password reset
  forgotPassword: async (email: string) => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        const user = mockData.users.find(u => u.email === email);
        if (!user) {
          throw new Error('User not found');
        }
        
        return { message: 'Password reset link sent' };
      }
      
      const response = await apiClient.post('/auth/forgot-password/', { email });
      return response.data;
    } catch (error) {
      console.error('Failed to send reset link:', error);
      throw error;
    }
  },

  // Delete account
  deleteAccount: async (password: string) => {
    try {
      if (isDebugMode) {
        await simulateDelay();
        
        if (password !== 'password') {
          throw new Error('Invalid password');
        }
        
        return { message: 'Account deleted successfully' };
      }
      
      const response = await apiClient.post('/auth/delete-account/', { password });
      return response.data;
    } catch (error) {
      console.error('Failed to delete account:', error);
      throw error;
    }
  }
};

// Helper function to generate mock token
function generateMockToken(userId: string) {
  return btoa(`mock_token_${userId}_${Date.now()}`);
}