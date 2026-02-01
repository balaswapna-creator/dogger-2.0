// frontend/src/utils/api.js
// Simplified API utility for Dogger 2.0

// ============================================
// API CONFIGURATION
// ============================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://dogger2-backend.onrender.com/api';

// ============================================
// TOKEN MANAGEMENT (SIMPLE)
// ============================================

const getAccessToken = () => {
  // Try encrypted token first (from security.js)
  const encrypted = localStorage.getItem('access_token');
  if (encrypted) {
    try {
      return atob(encrypted).split('').reverse().join('');
    } catch {
      // If decryption fails, return as-is
      return encrypted;
    }
  }
  
  // Try plain token (fallback)
  return localStorage.getItem('token');
};

const getRefreshToken = () => {
  const encrypted = localStorage.getItem('refresh_token');
  if (encrypted) {
    try {
      return atob(encrypted).split('').reverse().join('');
    } catch {
      return encrypted;
    }
  }
  return null;
};

const setAccessToken = (token) => {
  const encrypted = btoa(token.split('').reverse().join(''));
  localStorage.setItem('access_token', encrypted);
};

const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('token'); // Also clear plain token
};

// ============================================
// API REQUEST HANDLER
// ============================================

export const apiRequest = async (method, endpoint, data = null, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAccessToken();

  console.log(`API Request: ${method} ${endpoint}`);
  console.log('Token exists:', !!token);
  if (token) {
    console.log('Token preview:', token.substring(0, 20) + '...');
  }

  // Build headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Build request config
  const config = {
    method,
    headers,
  };

  // Add body for non-GET requests
  if (data && method !== 'GET') {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, config);

    console.log(`API Response: ${endpoint} - Status ${response.status}`);

    // Handle 401 Unauthorized
    if (response.status === 401) {
      console.log('401 Unauthorized - attempting token refresh...');
      
      const refreshToken = getRefreshToken();
      
      if (refreshToken) {
        try {
          const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
          });

          if (refreshResponse.ok) {
            const { access } = await refreshResponse.json();
            setAccessToken(access);
            console.log('Token refreshed successfully!');

            // Retry original request
            headers['Authorization'] = `Bearer ${access}`;
            const retryResponse = await fetch(url, { ...config, headers });
            
            if (retryResponse.status === 204) return null;
            
            const retryData = await retryResponse.json();
            if (!retryResponse.ok) {
              throw new Error(retryData.detail || retryData.error || 'Request failed');
            }
            
            return retryData;
          }
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);
        }
      }

      // If refresh failed, clear tokens and redirect
      clearTokens();
      alert('Your session has expired. Please login again.');
      window.location.href = '/login';
      throw new Error('Session expired');
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null;
    }

    // Parse JSON response
    const responseData = await response.json();

    // Handle error responses
    if (!response.ok) {
      const errorMessage = responseData.detail || responseData.error || responseData.message || 'An error occurred';
      throw new Error(errorMessage);
    }

    return responseData;

  } catch (error) {
    console.error(`API Error: ${endpoint}`, error);
    
    if (error.message === 'Session expired') {
      throw error;
    }
    
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Network error. Please check your internet connection.');
    }

    throw error;
  }
};

// ============================================
// FILE UPLOAD HANDLER
// ============================================

export const uploadFile = async (endpoint, formData, onProgress = null) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAccessToken();

  const headers = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  console.log(`File Upload: POST ${endpoint}`);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    console.log(`Upload Response: ${endpoint} - Status ${response.status}`);

    if (response.status === 401) {
      clearTokens();
      window.location.href = '/login';
      throw new Error('Unauthorized. Please login again.');
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || errorData.error || 'Upload failed');
    }

    return await response.json();

  } catch (error) {
    console.error(`Upload Error: ${endpoint}`, error);
    throw error;
  }
};

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || errorData.error || 'Login failed');
    }

    const data = await response.json();

    // Store tokens
    if (data.access && data.refresh) {
      const encryptedAccess = btoa(data.access.split('').reverse().join(''));
      const encryptedRefresh = btoa(data.refresh.split('').reverse().join(''));
      localStorage.setItem('access_token', encryptedAccess);
      localStorage.setItem('refresh_token', encryptedRefresh);
      
      console.log('Login successful, tokens stored');
    }

    return data;

  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const logout = () => {
  clearTokens();
  window.location.href = '/login';
};

export const getCurrentUser = async () => {
  try {
    return await apiRequest('GET', '/auth/user/');
  } catch (error) {
    console.error('Failed to get current user:', error);
    return null;
  }
};

// ============================================
// HELPER FUNCTIONS
// ============================================

export const isAuthenticated = () => {
  return !!getAccessToken();
};

export const getAuthToken = () => {
  return getAccessToken();
};

// ============================================
// EXPORTS
// ============================================

export default {
  apiRequest,
  uploadFile,
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
  getAuthToken,
};
