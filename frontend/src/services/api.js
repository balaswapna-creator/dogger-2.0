// frontend/src/services/api.js
// Secure API client with automatic token refresh and error handling

import axios from 'axios';
import { TokenManager, UserManager, SecurityMonitor } from '@/utils/security';
import router from '@/router';

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Track if we're currently refreshing token
let isRefreshing = false;
let failedQueue = [];

/**
 * Process failed request queue after token refresh
 */
const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

/**
 * Request interceptor - Add auth token to requests
 */
apiClient.interceptors.request.use(
  (config) => {
    const token = TokenManager.getAccessToken();
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add CSRF token for non-GET requests
    if (config.method !== 'get') {
      const csrfToken = getCSRFToken();
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - Handle token refresh
 */
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      
      // Check if the error is specifically about token expiration
      const errorCode = error.response?.data?.code;
      
      if (errorCode === 'token_not_valid' || errorCode === 'token_expired') {
        
        if (isRefreshing) {
          // If already refreshing, queue this request
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject });
          })
            .then(token => {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              return apiClient(originalRequest);
            })
            .catch(err => {
              return Promise.reject(err);
            });
        }
        
        originalRequest._retry = true;
        isRefreshing = true;
        
        const refreshToken = TokenManager.getRefreshToken();
        
        if (!refreshToken) {
          // No refresh token, logout
          handleLogout('No refresh token available');
          return Promise.reject(error);
        }
        
        try {
          // Try to refresh token
          const response = await axios.post(
            `${API_BASE_URL}/api/token/refresh/`,
            { refresh: refreshToken }
          );
          
          const { access } = response.data;
          
          // Store new access token
          TokenManager.setAccessToken(access);
          
          // Update authorization header
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          originalRequest.headers.Authorization = `Bearer ${access}`;
          
          // Process queued requests
          processQueue(null, access);
          
          isRefreshing = false;
          
          // Retry original request
          return apiClient(originalRequest);
          
        } catch (refreshError) {
          // Refresh failed, logout
          processQueue(refreshError, null);
          isRefreshing = false;
          
          handleLogout('Token refresh failed');
          
          return Promise.reject(refreshError);
        }
      } else {
        // Other 401 errors (invalid credentials, etc.)
        if (originalRequest.url.includes('/api/token/')) {
          // Login failed, don't logout
          return Promise.reject(error);
        }
        
        handleLogout('Unauthorized access');
        return Promise.reject(error);
      }
    }
    
    // Handle other error codes
    if (error.response?.status === 403) {
      SecurityMonitor.logSecurityEvent('forbidden_access', {
        url: originalRequest.url,
        method: originalRequest.method
      });
    }
    
    if (error.response?.status === 429) {
      SecurityMonitor.logSecurityEvent('rate_limit_exceeded', {
        url: originalRequest.url
      });
    }
    
    return Promise.reject(error);
  }
);

/**
 * Get CSRF token from cookie
 */
function getCSRFToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Handle logout
 */
function handleLogout(reason) {
  SecurityMonitor.logSecurityEvent('auto_logout', { reason });
  
  TokenManager.clearTokens();
  UserManager.clearUser();
  
  // Redirect to login
  if (router.currentRoute.value.path !== '/login') {
    router.push({
      path: '/login',
      query: { redirect: router.currentRoute.value.fullPath }
    });
  }
}

/**
 * API Methods
 */
const api = {
  // Authentication
  async login(username, password) {
    try {
      // Step 1: Get tokens from Django JWT endpoint
      const response = await apiClient.post('/api/token/', { username, password });
      const { access, refresh } = response.data;
      
      // Step 2: Store tokens immediately
      TokenManager.setTokens(access, refresh);
      
      // Step 3: ALWAYS fetch user profile after login
      let userProfile = null;
      try {
        const profileResponse = await apiClient.get('/api/profile/');
        userProfile = profileResponse.data;
        
        // Step 4: Store user data with role
        UserManager.setUser(userProfile);
        
        console.log('✅ User profile fetched successfully:', {
          username: userProfile.username,
          role: userProfile.role,
          is_staff: userProfile.is_staff
        });
        
        SecurityMonitor.logSecurityEvent('login_success', { 
          username,
          role: userProfile.role 
        });
        
      } catch (profileError) {
        console.error('❌ Failed to fetch user profile:', profileError);
        
        SecurityMonitor.logSecurityEvent('profile_fetch_failed', { 
          username,
          error: profileError.response?.data 
        });
      }
      
      // Return response with user data
      return {
        ...response.data,
        user: userProfile
      };
      
    } catch (error) {
      SecurityMonitor.logSecurityEvent('login_failed', { 
        username,
        error: error.response?.data 
      });
      throw error;
    }
  },

  async logout() {
    try {
      const response = await apiClient.post('/api/logout/');
      TokenManager.clearTokens();
      UserManager.clearUser();
      SecurityMonitor.logSecurityEvent('logout_success');
      return response.data;
    } catch (error) {
      // Even if API call fails, clear local tokens
      TokenManager.clearTokens();
      UserManager.clearUser();
      throw error;
    }
  },

  async refreshToken() {
    const refreshToken = TokenManager.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await apiClient.post('/api/token/refresh/', {
      refresh: refreshToken
    });
    
    const { access } = response.data;
    TokenManager.setAccessToken(access);
    
    return response.data;
  },

  async getUserProfile() {
    const response = await apiClient.get('/api/profile/');
    return response.data;
  },

  async updateProfile(data) {
    const response = await apiClient.put('/api/profile/update/', data);
    return response.data;
  },

  async changePassword(oldPassword, newPassword) {
    const response = await apiClient.post('/api/profile/change-password/', {
      old_password: oldPassword,
      new_password: newPassword
    });
    return response.data;
  },

  // Health & Monitoring
  async getHealth() {
    const response = await apiClient.get('/api/health/');
    return response.data;
  },

  async getMetrics() {
    const response = await apiClient.get('/api/metrics/');
    return response.data;
  },

  // Dashboard
  async getDashboardStats() {
    const response = await apiClient.get('/api/dashboard/stats/');
    return response.data;
  },

  // Patients
  async getPatients(params = {}) {
    const response = await apiClient.get('/api/patients/', { params });
    return response.data;
  },

  async getPatient(id) {
    const response = await apiClient.get(`/api/patients/${id}/`);
    return response.data;
  },

  async createPatient(data) {
    const response = await apiClient.post('/api/patients/', data);
    return response.data;
  },

  async updatePatient(id, data) {
    const response = await apiClient.put(`/api/patients/${id}/`, data);
    return response.data;
  },

  async deletePatient(id) {
    const response = await apiClient.delete(`/api/patients/${id}/`);
    return response.data;
  },

  // Owners
  async getOwners(params = {}) {
    const response = await apiClient.get('/api/owners/', { params });
    return response.data;
  },

  async getOwner(id) {
    const response = await apiClient.get(`/api/owners/${id}/`);
    return response.data;
  },

  async createOwner(data) {
    const response = await apiClient.post('/api/owners/', data);
    return response.data;
  },

  async updateOwner(id, data) {
    const response = await apiClient.put(`/api/owners/${id}/`, data);
    return response.data;
  },

  async deleteOwner(id) {
    const response = await apiClient.delete(`/api/owners/${id}/`);
    return response.data;
  },

  // Medical Records
  async getMedicalRecords(params = {}) {
    const response = await apiClient.get('/api/medical-records/', { params });
    return response.data;
  },

  async createMedicalRecord(data) {
    const response = await apiClient.post('/api/medical-records/', data);
    return response.data;
  },

  // Vaccinations
  async getVaccinations(params = {}) {
    const response = await apiClient.get('/api/vaccinations/', { params });
    return response.data;
  },

  async createVaccination(data) {
    const response = await apiClient.post('/api/vaccinations/', data);
    return response.data;
  },

  // Payments
  async getPayments(params = {}) {
    const response = await apiClient.get('/api/payments/', { params });
    return response.data;
  },

  async createPayment(data) {
    const response = await apiClient.post('/api/payments/', data);
    return response.data;
  },

  // File upload helper
  async uploadFile(endpoint, file, additionalData = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    Object.keys(additionalData).forEach(key => {
      formData.append(key, additionalData[key]);
    });
    
    const response = await apiClient.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }
};

export default api;
export { apiClient };