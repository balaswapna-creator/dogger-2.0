import axios from 'axios'

const API_BASE_URL = 'https://dogger2-backend.onrender.com/api'

// Create axios instance
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 second timeout
})

// Request interceptor - add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor - handle token refresh
axiosInstance.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.config.url} - Status ${response.status}`)
    return response
  },
  async (error) => {
    console.error('API Error:', error.response?.status, error.config?.url)
    
    const originalRequest = error.config

    // If 401 and haven't tried refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        console.log('Attempting token refresh...')
        const response = await axios.post(
          `${API_BASE_URL}/token/refresh/`,
          { refresh: refreshToken }
        )

        const { access } = response.data
        localStorage.setItem('token', access)
        console.log('Token refreshed successfully')

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access}`
        return axiosInstance(originalRequest)
        
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError)
        // Clear storage and redirect to login
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API object with all methods
const api = {
  // ===== AUTHENTICATION =====
  login: async (username, password) => {
    try {
      console.log('Logging in as:', username)
      
      const response = await axios.post(
        `${API_BASE_URL}/token/`,
        { username, password }
      )

      const { access, refresh } = response.data
      
      if (!access || !refresh) {
        throw new Error('Invalid login response - missing tokens')
      }

      // Store tokens
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)

      // Decode JWT to extract user info
      try {
        const base64Url = access.split('.')[1]
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
        const payload = JSON.parse(window.atob(base64))
        
        const user = {
          id: payload.user_id,
          username: payload.username || username,
          email: payload.email || '',
          role: payload.role || 'user'
        }
        
        localStorage.setItem('user', JSON.stringify(user))
        console.log('Login successful, user:', user)
      } catch (e) {
        console.error('Error parsing JWT:', e)
      }

      return response.data
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  },

  logout: () => {
    localStorage.clear()
    window.location.href = '/login'
  },

  getUserProfile: () => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  // ===== DASHBOARD =====
  getDashboardStats: () => axiosInstance.get('/dashboard/stats/'),

  // ===== PATIENTS =====
  getPatients: () => axiosInstance.get('/patients/'),
  getPatient: (id) => axiosInstance.get(`/patients/${id}/`),
  createPatient: (data) => axiosInstance.post('/patients/', data),
  updatePatient: (id, data) => axiosInstance.put(`/patients/${id}/`, data),
  deletePatient: (id) => axiosInstance.delete(`/patients/${id}/`),

  // ===== OWNERS =====
  getOwners: () => axiosInstance.get('/owners/'),
  getOwner: (id) => axiosInstance.get(`/owners/${id}/`),
  createOwner: (data) => axiosInstance.post('/owners/', data),
  updateOwner: (id, data) => axiosInstance.put(`/owners/${id}/`, data),
  deleteOwner: (id) => axiosInstance.delete(`/owners/${id}/`),

  // ===== MEDICAL RECORDS =====
  getMedicalRecords: () => axiosInstance.get('/medical-records/'),
  getMedicalRecord: (id) => axiosInstance.get(`/medical-records/${id}/`),
  createMedicalRecord: (data) => axiosInstance.post('/medical-records/', data),
  updateMedicalRecord: (id, data) => axiosInstance.put(`/medical-records/${id}/`, data),
  deleteMedicalRecord: (id) => axiosInstance.delete(`/medical-records/${id}/`),

  // ===== VACCINATIONS =====
  getVaccinations: () => axiosInstance.get('/vaccinations/'),
  getVaccination: (id) => axiosInstance.get(`/vaccinations/${id}/`),
  createVaccination: (data) => axiosInstance.post('/vaccinations/', data),
  updateVaccination: (id, data) => axiosInstance.put(`/vaccinations/${id}/`, data),
  deleteVaccination: (id) => axiosInstance.delete(`/vaccinations/${id}/`),

  // ===== PAYMENTS =====
  getPayments: () => axiosInstance.get('/payments/'),
  getPayment: (id) => axiosInstance.get(`/payments/${id}/`),
  createPayment: (data) => axiosInstance.post('/payments/', data),
  updatePayment: (id, data) => axiosInstance.put(`/payments/${id}/`, data),
  deletePayment: (id) => axiosInstance.delete(`/payments/${id}/`),

  // ===== PASSBOOKS =====
  getPassbooks: () => axiosInstance.get('/passbooks/'),
  getPassbook: (id) => axiosInstance.get(`/passbooks/${id}/`),
  createPassbook: (data) => axiosInstance.post('/passbooks/', data),
  updatePassbook: (id, data) => axiosInstance.put(`/passbooks/${id}/`, data),
  deletePassbook: (id) => axiosInstance.delete(`/passbooks/${id}/`),

  // ===== PRESCRIPTIONS =====
  getPrescriptions: () => axiosInstance.get('/prescriptions/'),
  getPrescription: (id) => axiosInstance.get(`/prescriptions/${id}/`),
  createPrescription: (data) => axiosInstance.post('/prescriptions/', data),
  updatePrescription: (id, data) => axiosInstance.put(`/prescriptions/${id}/`, data),
  deletePrescription: (id) => axiosInstance.delete(`/prescriptions/${id}/`),

  // ===== GENERIC METHODS =====
  get: (url, config) => axiosInstance.get(url, config),
  post: (url, data, config) => axiosInstance.post(url, data, config),
  put: (url, data, config) => axiosInstance.put(url, data, config),
  patch: (url, data, config) => axiosInstance.patch(url, data, config),
  delete: (url, config) => axiosInstance.delete(url, config)
}

export default api