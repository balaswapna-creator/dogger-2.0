import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = ref(!!token.value)

  // Login function
  async function login(username, password) {
    try {
      const response = await api.post('/token/', {
        username,
        password
      })
      
      token.value = response.data.access
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refreshToken', response.data.refresh)
      
      // Set auth header for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      isAuthenticated.value = true
      
      // Get user info
      await fetchUser()
      
      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  // Fetch current user
  async function fetchUser() {
    try {
      // FIXED: Changed from '/users/me/' to '/auth/me/'
      const response = await api.get('/auth/me/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      // If token is invalid, logout
      if (error.response?.status === 401) {
        logout()
      }
    }
  }

  // Logout function
  function logout() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    delete api.defaults.headers.common['Authorization']
  }

  // Check authentication on app load
  async function checkAuth() {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      await fetchUser()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth,
    fetchUser
  }
})