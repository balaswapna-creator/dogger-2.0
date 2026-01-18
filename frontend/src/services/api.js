import axios from 'axios'
import { TokenManager, UserManager } from '../utils/security'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://dogger2-backend.onrender.com'

// Create axios instance
const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = TokenManager.getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = TokenManager.getRefreshToken()
        
        if (!refreshToken) {
          // No refresh token, redirect to login
          TokenManager.clearTokens()
          UserManager.clearUser()
          window.location.href = '/login'
          return Promise.reject(error)
        }

        // Try to refresh the token
        const response = await axios.post(
          `${API_BASE_URL}/api/token/refresh/`,
          { refresh: refreshToken }
        )

        const { access } = response.data
        TokenManager.setAccessToken(access)

        // Retry the original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        // Refresh failed, clear everything and redirect to login
        TokenManager.clearTokens()
        UserManager.clearUser()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Helper function to decode JWT and extract user info
const decodeJWT = (token) => {
  try {
    // JWT structure: header.payload.signature
    const parts = token.split('.')
    if (parts.length !== 3) {
      console.error('Invalid JWT format')
      return null
    }

    // Decode the payload (second part)
    const payload = parts[1]
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )

    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Error decoding JWT:', error)
    return null
  }
}

// API methods
const api = {
  // Authentication
  async login(username, password) {
    try {
      console.log('API: Sending login request...')
      
      const response = await axiosInstance.post('/token/', {
        username,
        password,
      })

      console.log('API: Login response received:', response.data)

      const { access, refresh } = response.data

      if (!access || !refresh) {
        throw new Error('Invalid response: missing tokens')
      }

      // Store tokens
      TokenManager.setAccessToken(access)
      TokenManager.setRefreshToken(refresh)

      // Decode token to get user info
      const payload = decodeJWT(access)
      console.log('API: Decoded JWT payload:', payload)

      if (payload) {
        // Extract user info from JWT payload
        const userInfo = {
          id: payload.user_id,
          username: payload.username || username,
          email: payload.email || '',
          // Add any other fields that exist in your JWT payload
        }

        // Store user info
        UserManager.setUser(userInfo)
        console.log('API: User info stored:', userInfo)
      } else {
        console.warn('API: Could not decode JWT payload')
      }

      return response.data
    } catch (error) {
      console.error('API: Login error:', error)
      throw error
    }
  },

  logout() {
    TokenManager.clearTokens()
    UserManager.clearUser()
  },

  // Get current user info from stored data
  getUserProfile() {
    return UserManager.getUser()
  },

  // Dashboard
  async getDashboardStats() {
    const response = await axiosInstance.get('/dashboard/stats/')
    return response.data
  },

  // Patients
  async getPatients() {
    const response = await axiosInstance.get('/patients/')
    return response.data
  },

  async getPatient(id) {
    const response = await axiosInstance.get(`/patients/${id}/`)
    return response.data
  },

  async createPatient(data) {
    const response = await axiosInstance.post('/patients/', data)
    return response.data
  },

  async updatePatient(id, data) {
    const response = await axiosInstance.put(`/patients/${id}/`, data)
    return response.data
  },

  async deletePatient(id) {
    const response = await axiosInstance.delete(`/patients/${id}/`)
    return response.data
  },

  // Owners
  async getOwners() {
    const response = await axiosInstance.get('/owners/')
    return response.data
  },

  async getOwner(id) {
    const response = await axiosInstance.get(`/owners/${id}/`)
    return response.data
  },

  async createOwner(data) {
    const response = await axiosInstance.post('/owners/', data)
    return response.data
  },

  async updateOwner(id, data) {
    const response = await axiosInstance.put(`/owners/${id}/`, data)
    return response.data
  },

  async deleteOwner(id) {
    const response = await axiosInstance.delete(`/owners/${id}/`)
    return response.data
  },

  // Medical Records
  async getMedicalRecords() {
    const response = await axiosInstance.get('/medical-records/')
    return response.data
  },

  async getMedicalRecord(id) {
    const response = await axiosInstance.get(`/medical-records/${id}/`)
    return response.data
  },

  async createMedicalRecord(data) {
    const response = await axiosInstance.post('/medical-records/', data)
    return response.data
  },

  async updateMedicalRecord(id, data) {
    const response = await axiosInstance.put(`/medical-records/${id}/`, data)
    return response.data
  },

  async deleteMedicalRecord(id) {
    const response = await axiosInstance.delete(`/medical-records/${id}/`)
    return response.data
  },

  // Vaccinations
  async getVaccinations() {
    const response = await axiosInstance.get('/vaccinations/')
    return response.data
  },

  async getVaccination(id) {
    const response = await axiosInstance.get(`/vaccinations/${id}/`)
    return response.data
  },

  async createVaccination(data) {
    const response = await axiosInstance.post('/vaccinations/', data)
    return response.data
  },

  async updateVaccination(id, data) {
    const response = await axiosInstance.put(`/vaccinations/${id}/`, data)
    return response.data
  },

  async deleteVaccination(id) {
    const response = await axiosInstance.delete(`/vaccinations/${id}/`)
    return response.data
  },

  // Payments
  async getPayments() {
    const response = await axiosInstance.get('/payments/')
    return response.data
  },

  async getPayment(id) {
    const response = await axiosInstance.get(`/payments/${id}/`)
    return response.data
  },

  async createPayment(data) {
    const response = await axiosInstance.post('/payments/', data)
    return response.data
  },

  async updatePayment(id, data) {
    const response = await axiosInstance.put(`/payments/${id}/`, data)
    return response.data
  },

  async deletePayment(id) {
    const response = await axiosInstance.delete(`/payments/${id}/`)
    return response.data
  },

  // Passbooks
  async getPassbooks() {
    const response = await axiosInstance.get('/passbooks/')
    return response.data
  },

  async getPassbook(id) {
    const response = await axiosInstance.get(`/passbooks/${id}/`)
    return response.data
  },

  async createPassbook(data) {
    const response = await axiosInstance.post('/passbooks/', data)
    return response.data
  },

  async updatePassbook(id, data) {
    const response = await axiosInstance.put(`/passbooks/${id}/`, data)
    return response.data
  },

  async deletePassbook(id) {
    const response = await axiosInstance.delete(`/passbooks/${id}/`)
    return response.data
  },

  // Prescriptions
  async getPrescriptions() {
    const response = await axiosInstance.get('/prescriptions/')
    return response.data
  },

  async getPrescription(id) {
    const response = await axiosInstance.get(`/prescriptions/${id}/`)
    return response.data
  },

  async createPrescription(data) {
    const response = await axiosInstance.post('/prescriptions/', data)
    return response.data
  },

  async updatePrescription(id, data) {
    const response = await axiosInstance.put(`/prescriptions/${id}/`, data)
    return response.data
  },

  async deletePrescription(id) {
    const response = await axiosInstance.delete(`/prescriptions/${id}/`)
    return response.data
  },
}

export default api