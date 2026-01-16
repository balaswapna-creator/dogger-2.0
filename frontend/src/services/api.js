// frontend/src/services/api.js
// Secure API client with automatic token refresh and error handling

import axios from 'axios';
import { TokenManager, UserManager, SecurityMonitor } from '@/utils/security';
import router from '@/router';

// API base URL - UPDATE THIS TO YOUR RENDER BACKEND URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://dogger2-backend.onrender.com';

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
      
      // Step 3: Try to fetch user profile (if endpoint exists)
      let userProfile = null;
      try {
        // Try multiple possible profile endpoints
        const profileEndpoints = ['/api/auth/me/', '/api/profile/', '/api/user/'];
        
        for (const endpoint of profileEndpoints) {
          try {
            const profileResponse = await apiClient.get(endpoint);
            userProfile = profileResponse.data;
            console.log(`✅ User profile fetched from ${endpoint}`);
            break;
          } catch (e) {
            // Try next endpoint
            continue;
          }
        }
        
        // If no profile endpoint works, decode user from JWT token
        if (!userProfile) {
          console.log('ℹ️ No profile endpoint found, using token data');
          const tokenData = parseJwt(access);
          userProfile = {
            id: tokenData.user_id,
            username: username,
            role: 'user', // Default role
            is_staff: false
          };
        }
        
        // Store user data
        UserManager.setUser(userProfile);
        
        console.log('✅ Login successful:', {
          username: userProfile.username,
          role: userProfile.role
        });
        
        SecurityMonitor.logSecurityEvent('login_success', { 
          username,
          role: userProfile.role 
        });
        
      } catch (profileError) {
        console.warn('⚠️ Could not fetch user profile, but login succeeded');
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
      // Try to call logout endpoint if it exists
      try {
        await apiClient.post('/api/logout/');
      } catch (e) {
        // Logout endpoint might not exist, that's okay
        console.log('ℹ️ No logout endpoint, clearing tokens locally');
      }
      
      TokenManager.clearTokens();
      UserManager.clearUser();
      SecurityMonitor.logSecurityEvent('logout_success');
      
    } catch (error) {
      // Even if API call fails, clear local tokens
      TokenManager.clearTokens();
      UserManager.clearUser();
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
    // Try multiple possible profile endpoints
    const profileEndpoints = ['/api/auth/me/', '/api/profile/', '/api/user/'];
    
    for (const endpoint of profileEndpoints) {
      try {
        const response = await apiClient.get(endpoint);
        return response.data;
      } catch (e) {
        continue;
      }
    }
    
    // If no endpoint works, return cached user data
    return UserManager.getUser();
  },

  async updateProfile(data) {
    // Try multiple possible endpoints
    const updateEndpoints = ['/api/profile/update/', '/api/profile/', '/api/auth/me/'];
    
    for (const endpoint of updateEndpoints) {
      try {
        const response = await apiClient.put(endpoint, data);
        return response.data;
      } catch (e) {
        continue;
      }
    }
    
    throw new Error('Profile update endpoint not found');
  },

  async changePassword(oldPassword, newPassword) {
    // Try multiple possible endpoints
    const passwordEndpoints = [
      '/api/profile/change-password/',
      '/api/auth/change-password/',
      '/api/change-password/'
    ];
    
    for (const endpoint of passwordEndpoints) {
      try {
        const response = await apiClient.post(endpoint, {
          old_password: oldPassword,
          new_password: newPassword
        });
        return response.data;
      } catch (e) {
        continue;
      }
    }
    
    throw new Error('Change password endpoint not found');
  },

  // Health & Monitoring
  async getHealth() {
    try {
      const response = await apiClient.get('/api/health/');
      return response.data;
    } catch (e) {
      return { status: 'ok' }; // Fallback
    }
  },

  async getMetrics() {
    try {
      const response = await apiClient.get('/api/metrics/');
      return response.data;
    } catch (e) {
      return {}; // Fallback
    }
  },

  // Dashboard
  async getDashboardStats() {
    try {
      // Try the stats endpoint first
      const response = await apiClient.get('/api/dashboard/stats/');
      return response.data;
    } catch (e) {
      // If that doesn't exist, try just /api/dashboard/
      try {
        const response = await apiClient.get('/api/dashboard/');
        return response.data;
      } catch (e2) {
        // If neither works, fetch data from individual endpoints
        const [patients, owners, records, vaccinations, payments] = await Promise.all([
          this.getPatients().catch(() => ({ results: [] })),
          this.getOwners().catch(() => ({ results: [] })),
          this.getMedicalRecords().catch(() => ({ results: [] })),
          this.getVaccinations().catch(() => ({ results: [] })),
          this.getPayments().catch(() => ({ results: [] }))
        ]);
        
        return {
          total_patients: patients.results?.length || 0,
          total_owners: owners.results?.length || 0,
          total_records: records.results?.length || 0,
          total_vaccinations: vaccinations.results?.length || 0,
          total_payments: payments.results?.length || 0
        };
      }
    }
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

  // Passbooks
  async getPassbooks(params = {}) {
    const response = await apiClient.get('/api/passbooks/', { params });
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

/**
 * Helper function to parse JWT token
 */
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return {};
  }
}

export default api;
export { apiClient };