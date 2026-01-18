<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
    <div class="max-w-md w-full">
      <!-- Logo and Title -->
      <div class="text-center mb-8">
        <div class="mx-auto h-24 w-24 bg-indigo-600 rounded-full flex items-center justify-center mb-4">
          <svg class="h-12 w-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">Sri Adithya Pet Clinic</h1>
        <p class="text-gray-600 mt-2">Sign in to your account</p>
      </div>

      <!-- Login Form -->
      <div class="bg-white shadow-xl rounded-lg p-8">
        <!-- Error Alert -->
        <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-start">
            <svg class="h-5 w-5 text-red-400 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            <div class="text-sm text-red-600">{{ error }}</div>
          </div>
        </div>

        <form @submit.prevent="handleLogin">
          <!-- Username -->
          <div class="mb-4">
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Enter your username"
              :disabled="loading"
            />
          </div>

          <!-- Password -->
          <div class="mb-6">
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="••••••••"
              :disabled="loading"
            />
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <!-- Demo Credentials -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <p class="text-sm text-gray-600 text-center mb-2">Demo Credentials:</p>
          <p class="text-sm text-gray-800 text-center font-mono bg-gray-50 py-2 rounded">
            admin / admin123
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const API_BASE_URL = 'https://dogger2-backend.onrender.com'

const handleLogin = async () => {
  console.log('Attempting login with:', username.value)
  error.value = ''
  loading.value = true

  try {
    // Make login request
    console.log('API: Sending login request...')
    const response = await axios.post(`${API_BASE_URL}/api/token/`, {
      username: username.value,
      password: password.value
    })

    console.log('API: Login response received:', response.data)

    // Store tokens directly in localStorage (no TokenManager)
    if (response.data.access && response.data.refresh) {
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refreshToken', response.data.refresh)
      
      // Decode JWT to get user info
      try {
        const payload = JSON.parse(atob(response.data.access.split('.')[1]))
        const user = {
          id: payload.user_id,
          username: payload.username || username.value,
          email: payload.email || '',
          role: payload.role || 'user'
        }
        localStorage.setItem('user', JSON.stringify(user))
        console.log('User stored:', user)
      } catch (e) {
        console.error('Error parsing JWT:', e)
      }

      console.log('Login successful, redirecting to dashboard...')
      
      // Redirect to dashboard using window.location
      window.location.href = '/dashboard'
    } else {
      throw new Error('Invalid response from server')
    }

  } catch (err) {
    console.error('Login error:', err)
    
    // Handle different error types
    if (err.response) {
      // Server responded with error
      if (err.response.status === 401) {
        error.value = 'Invalid username or password'
      } else if (err.response.status === 429) {
        error.value = 'Too many login attempts. Please try again later.'
      } else {
        error.value = err.response.data?.detail || 'Login failed. Please try again.'
      }
    } else if (err.request) {
      // No response received
      error.value = 'Cannot connect to server. Please check your connection.'
    } else {
      // Other errors
      error.value = err.message || 'An unexpected error occurred'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>