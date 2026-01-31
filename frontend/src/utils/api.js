// frontend/src/utils/api.js
// API utility for Dogger 2.0 - Integrates with security.js

import { TokenManager, InputSanitizer, EnhancedSanitizer, SecurityMonitor } from './security.js';

// ============================================
// API CONFIGURATION
// ============================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://dogger2-backend.onrender.com/api';

// ============================================
// API REQUEST HANDLER
// ============================================

/**
 * Generic API request function with security integration
 * @param {string} method - HTTP method (GET, POST, PUT, PATCH, DELETE)
 * @param {string} endpoint - API endpoint (e.g., '/patients/')
 * @param {object} data - Request body data (optional)
 * @param {object} options - Additional options (optional)
 * @returns {Promise} - Response data
 */
export const apiRequest = async (method, endpoint, data = null, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = TokenManager.getAccessToken();

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
    ...options.fetchOptions,
  };

  // Add body for non-GET requests
  if (data && method !== 'GET') {
    // Sanitize data before sending
    const sanitizedData = options.skipSanitization ? data : EnhancedSanitizer.sanitizeObject(data);
    config.body = JSON.stringify(sanitizedData);
  }

  console.log(`API Request: ${method} ${endpoint}`);

  try {
    const response = await fetch(url, config);

    console.log(`API Response: ${endpoint} - Status ${response.status}`);

    // Handle 401 Unauthorized - Token expired or invalid
    if (response.status === 401) {
      SecurityMonitor.logSecurityEvent('unauthorized_access', {
        endpoint,
        method,
        status: 401
      });

      // Check if we have a refresh token
      const refreshToken = TokenManager.getRefreshToken();
      
      if (refreshToken && !TokenManager.isTokenExpired(refreshToken)) {
        // Try to refresh the access token
        try {
          const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
          });

          if (refreshResponse.ok) {
            const { access } = await refreshResponse.json();
            TokenManager.setAccessToken(access);

            // Retry the original request with new token
            headers['Authorization'] = `Bearer ${access}`;
            const retryResponse = await fetch(url, config);
            
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

      // If refresh failed or no refresh token, clear tokens and redirect
      TokenManager.clearTokens();
      window.location.href = '/login';
      throw new Error('Session expired. Please login again.');
    }

    // Handle 403 Forbidden
    if (response.status === 403) {
      SecurityMonitor.logSecurityEvent('forbidden_access', {
        endpoint,
        method,
        status: 403
      });
      throw new Error('Access forbidden. You do not have permission to perform this action.');
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
      
      // Log error for monitoring
      SecurityMonitor.logSecurityEvent('api_error', {
        endpoint,
        method,
        status: response.status,
        error: errorMessage
      });

      throw new Error(errorMessage);
    }

    return responseData;

  } catch (error) {
    console.error(`API Error: ${endpoint}`, error);
    
    // Network error or fetch failed
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      SecurityMonitor.logSecurityEvent('network_error', {
        endpoint,
        method,
        error: 'Network connection failed'
      });
      throw new Error('Network error. Please check your internet connection.');
    }

    throw error;
  }
};

// ============================================
// FILE UPLOAD HANDLER
// ============================================

/**
 * Upload file with FormData
 * @param {string} endpoint - API endpoint
 * @param {FormData} formData - FormData object with file
 * @param {function} onProgress - Progress callback (optional)
 * @returns {Promise} - Response data
 */
export const uploadFile = async (endpoint, formData, onProgress = null) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = TokenManager.getAccessToken();

  const headers = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  console.log(`File Upload: POST ${endpoint}`);

  try {
    // Create XMLHttpRequest for progress tracking
    if (onProgress) {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            onProgress(percentComplete);
          }
        });

        xhr.addEventListener('load', () => {
          if (xhr.status === 401) {
            TokenManager.clearTokens();
            window.location.href = '/login';
            reject(new Error('Unauthorized. Please login again.'));
            return;
          }

          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(JSON.parse(xhr.responseText));
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText);
              reject(new Error(errorData.detail || errorData.error || 'Upload failed'));
            } catch {
              reject(new Error('Upload failed'));
            }
          }
        });

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'));
        });

        xhr.open('POST', url);
        if (token) {
          xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        }
        xhr.send(formData);
      });
    }

    // Standard fetch for uploads without progress
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    console.log(`Upload Response: ${endpoint} - Status ${response.status}`);

    if (response.status === 401) {
      TokenManager.clearTokens();
      window.location.href = '/login';
      throw new Error('Unauthorized. Please login again.');
    }

    if (!response.ok) {
      const errorData = await response.json();
      const errorMessage = errorData.detail || errorData.error || 'Upload failed';
      throw new Error(errorMessage);
    }

    return await response.json();

  } catch (error) {
    console.error(`Upload Error: ${endpoint}`, error);
    SecurityMonitor.logSecurityEvent('upload_error', {
      endpoint,
      error: error.message
    });
    throw error;
  }
};

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

/**
 * Login user and store tokens
 * @param {string} username
 * @param {string} password
 * @returns {Promise} - User data with tokens
 */
export const login = async (username, password) => {
  try {
    const sanitizedUsername = InputSanitizer.sanitizeInput(username);
    
    const response = await apiRequest('POST', '/auth/login/', {
      username: sanitizedUsername,
      password,
    }, { skipSanitization: true });

    // Store tokens securely
    if (response.access && response.refresh) {
      TokenManager.setTokens(response.access, response.refresh);
      
      SecurityMonitor.logSecurityEvent('login_success', {
        username: sanitizedUsername,
        timestamp: new Date().toISOString()
      });
    }

    return response;

  } catch (error) {
    SecurityMonitor.logSecurityEvent('login_failure', {
      username: InputSanitizer.sanitizeInput(username),
      error: error.message
    });
    throw error;
  }
};

/**
 * Logout user and clear tokens
 */
export const logout = () => {
  SecurityMonitor.logSecurityEvent('logout', {
    timestamp: new Date().toISOString()
  });

  TokenManager.clearTokens();
  window.location.href = '/login';
};

/**
 * Get current user info
 * @returns {Promise} - User data
 */
export const getCurrentUser = async () => {
  try {
    return await apiRequest('GET', '/auth/user/');
  } catch (error) {
    console.error('Failed to get current user:', error);
    return null;
  }
};

/**
 * Refresh access token
 * @returns {Promise} - New access token
 */
export const refreshAccessToken = async () => {
  const refreshToken = TokenManager.getRefreshToken();
  
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken })
    });

    if (!response.ok) {
      throw new Error('Token refresh failed');
    }

    const { access } = await response.json();
    TokenManager.setAccessToken(access);
    
    return access;

  } catch (error) {
    TokenManager.clearTokens();
    window.location.href = '/login';
    throw error;
  }
};

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  return TokenManager.isAuthenticated();
};

/**
 * Get auth token for manual use
 * @returns {string|null}
 */
export const getAuthToken = () => {
  return TokenManager.getAccessToken();
};

/**
 * Build query string from object
 * @param {object} params - Query parameters
 * @returns {string} - Query string
 */
export const buildQueryString = (params) => {
  if (!params || Object.keys(params).length === 0) {
    return '';
  }

  const queryString = Object.entries(params)
    .filter(([_, value]) => value !== null && value !== undefined && value !== '')
    .map(([key, value]) => {
      const sanitizedKey = encodeURIComponent(key);
      const sanitizedValue = encodeURIComponent(String(value));
      return `${sanitizedKey}=${sanitizedValue}`;
    })
    .join('&');

  return queryString ? `?${queryString}` : '';
};

/**
 * Make a GET request with query parameters
 * @param {string} endpoint - API endpoint
 * @param {object} params - Query parameters
 * @returns {Promise} - Response data
 */
export const apiGet = async (endpoint, params = {}) => {
  const queryString = buildQueryString(params);
  return await apiRequest('GET', `${endpoint}${queryString}`);
};

/**
 * Make a POST request
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body
 * @returns {Promise} - Response data
 */
export const apiPost = async (endpoint, data) => {
  return await apiRequest('POST', endpoint, data);
};

/**
 * Make a PUT request
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body
 * @returns {Promise} - Response data
 */
export const apiPut = async (endpoint, data) => {
  return await apiRequest('PUT', endpoint, data);
};

/**
 * Make a PATCH request
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body
 * @returns {Promise} - Response data
 */
export const apiPatch = async (endpoint, data) => {
  return await apiRequest('PATCH', endpoint, data);
};

/**
 * Make a DELETE request
 * @param {string} endpoint - API endpoint
 * @returns {Promise} - Response data
 */
export const apiDelete = async (endpoint) => {
  return await apiRequest('DELETE', endpoint);
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
  refreshAccessToken,
  isAuthenticated,
  getAuthToken,
  buildQueryString,
  apiGet,
  apiPost,
  apiPut,
  apiPatch,
  apiDelete,
};