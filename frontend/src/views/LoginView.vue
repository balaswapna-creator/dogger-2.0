<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="mx-auto w-24 h-24 bg-indigo-600 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800">Sri Adithya Pet Clinic</h1>
        <p class="text-gray-600 mt-2">Sign in to your account</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Username -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Username
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder="admin"
          />
        </div>

        <!-- Password -->
        <div>
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
          />
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <!-- Demo Credentials -->
      <div class="mt-6 p-4 bg-gray-50 rounded-lg">
        <p class="text-sm text-gray-600 font-medium mb-2">Demo Credentials:</p>
        <p class="text-sm text-gray-700">admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    console.log('Attempting login with:', username.value)
    
    // Call the login API
    const response = await api.login(username.value, password.value)
    
    console.log('Login response:', response)
    
    // Check if we got tokens
    if (!response.access || !response.refresh) {
      throw new Error('Invalid response from server - missing tokens')
    }

    // Tokens are already stored by api.login()
    console.log('Login successful, redirecting to dashboard...')
    
    // Use window.location for reliable redirect
    window.location.href = '/dashboard'
    
  } catch (err) {
    console.error('Login error:', err)
    
    // Handle different error types
    if (err.response) {
      // Backend returned an error
      const status = err.response.status
      const data = err.response.data
      
      if (status === 401) {
        error.value = 'Invalid username or password'
      } else if (status === 429) {
        error.value = 'Too many login attempts. Please try again later.'
      } else if (status >= 500) {
        error.value = 'Server error. Please try again later.'
      } else {
        error.value = data.detail || data.message || 'Login failed'
      }
    } else if (err.request) {
      // Request was made but no response
      error.value = 'Cannot connect to server. Please check your internet connection.'
    } else {
      // Something else went wrong
      error.value = err.message || 'An unexpected error occurred'
    }
    
    loading.value = false
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>