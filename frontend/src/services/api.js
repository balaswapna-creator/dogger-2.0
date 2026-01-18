import axios from 'axios'

const API_BASE_URL = 'https://dogger2-backend.onrender.com'

// Create axios instance with base configuration
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor to attach token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
            refresh: refreshToken
          })

          const { access } = response.data
          localStorage.setItem('token', access)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`
          return axiosInstance(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API methods
const api = {
  // Auth methods
  login: async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/api/token/`, {
      username,
      password
    })
    
    if (response.data.access && response.data.refresh) {
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refreshToken', response.data.refresh)
      
      // Decode JWT to get user info
      try {
        const payload = JSON.parse(atob(response.data.access.split('.')[1]))
        const user = {
          id: payload.user_id,
          username: payload.username || username,
          email: payload.email || '',
          role: payload.role || 'user'
        }
        localStorage.setItem('user', JSON.stringify(user))
      } catch (e) {
        console.error('Error parsing JWT:', e)
      }
    }
    
    return response.data
  },

  logout: () => {
    localStorage.clear()
    window.location.href = '/login'
  },

  getUserProfile: () => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  // Dashboard
  getDashboardStats: () => axiosInstance.get('/api/dashboard/stats/'),

  // Patients
  getPatients: () => axiosInstance.get('/api/patients/'),
  getPatient: (id) => axiosInstance.get(`/api/patients/${id}/`),
  createPatient: (data) => axiosInstance.post('/api/patients/', data),
  updatePatient: (id, data) => axiosInstance.put(`/api/patients/${id}/`, data),
  deletePatient: (id) => axiosInstance.delete(`/api/patients/${id}/`),

  // Owners
  getOwners: () => axiosInstance.get('/api/owners/'),
  getOwner: (id) => axiosInstance.get(`/api/owners/${id}/`),
  createOwner: (data) => axiosInstance.post('/api/owners/', data),
  updateOwner: (id, data) => axiosInstance.put(`/api/owners/${id}/`, data),
  deleteOwner: (id) => axiosInstance.delete(`/api/owners/${id}/`),

  // Medical Records
  getMedicalRecords: () => axiosInstance.get('/api/medical-records/'),
  getMedicalRecord: (id) => axiosInstance.get(`/api/medical-records/${id}/`),
  createMedicalRecord: (data) => axiosInstance.post('/api/medical-records/', data),
  updateMedicalRecord: (id, data) => axiosInstance.put(`/api/medical-records/${id}/`, data),
  deleteMedicalRecord: (id) => axiosInstance.delete(`/api/medical-records/${id}/`),

  // Vaccinations
  getVaccinations: () => axiosInstance.get('/api/vaccinations/'),
  getVaccination: (id) => axiosInstance.get(`/api/vaccinations/${id}/`),
  createVaccination: (data) => axiosInstance.post('/api/vaccinations/', data),
  updateVaccination: (id, data) => axiosInstance.put(`/api/vaccinations/${id}/`, data),
  deleteVaccination: (id) => axiosInstance.delete(`/api/vaccinations/${id}/`),

  // Payments
  getPayments: () => axiosInstance.get('/api/payments/'),
  getPayment: (id) => axiosInstance.get(`/api/payments/${id}/`),
  createPayment: (data) => axiosInstance.post('/api/payments/', data),
  updatePayment: (id, data) => axiosInstance.put(`/api/payments/${id}/`, data),
  deletePayment: (id) => axiosInstance.delete(`/api/payments/${id}/`),

  // Passbooks
  getPassbooks: () => axiosInstance.get('/api/passbooks/'),
  getPassbook: (id) => axiosInstance.get(`/api/passbooks/${id}/`),
  createPassbook: (data) => axiosInstance.post('/api/passbooks/', data),
  updatePassbook: (id, data) => axiosInstance.put(`/api/passbooks/${id}/`, data),
  deletePassbook: (id) => axiosInstance.delete(`/api/passbooks/${id}/`),

  // Prescriptions
  getPrescriptions: () => axiosInstance.get('/api/prescriptions/'),
  getPrescription: (id) => axiosInstance.get(`/api/prescriptions/${id}/`),
  createPrescription: (data) => axiosInstance.post('/api/prescriptions/', data),
  updatePrescription: (id, data) => axiosInstance.put(`/api/prescriptions/${id}/`, data),
  deletePrescription: (id) => axiosInstance.delete(`/api/prescriptions/${id}/`),

  // Generic methods for direct axios usage
  get: (url, config) => axiosInstance.get(url, config),
  post: (url, data, config) => axiosInstance.post(url, data, config),
  put: (url, data, config) => axiosInstance.put(url, data, config),
  patch: (url, data, config) => axiosInstance.patch(url, data, config),
  delete: (url, config) => axiosInstance.delete(url, config)
}

export default api