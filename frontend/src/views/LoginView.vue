<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-indigo-600 rounded-full mb-4">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800">Sri Adithya Pet Clinic</h1>
        <p class="text-gray-500 mt-2">Sign in to your account</p>
      </div>

      <div v-if="errorMessage" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-800">{{ errorMessage }}</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Username</label>
          <input v-model="username" type="text" required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            placeholder="Enter your username" />
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
          <input v-model="password" type="password" required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            placeholder="Enter your password" />
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 transition disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="!loading">Sign In</span>
          <span v-else>Signing in...</span>
        </button>
      </form>

      <div class="mt-6 text-center text-sm text-gray-500">
        <p>Demo Credentials:</p>
        <p class="font-mono text-xs mt-2">admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { TokenManager, UserManager } from '@/utils/security'

const router = useRouter()

const username = ref('admin')
const password = ref('admin123')
const errorMessage = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    // Call the login API
    const response = await api.login(username.value, password.value)
    
    console.log('✅ Login successful:', response)
    
    // Tokens are already stored by the api.login() method
    // Redirect to dashboard
    router.push('/dashboard')
    
  } catch (error) {
    console.error('❌ Login failed:', error)
    
    // Show user-friendly error message
    if (error.response) {
      if (error.response.status === 401) {
        errorMessage.value = 'Invalid username or password'
      } else if (error.response.status === 500) {
        errorMessage.value = 'Server error. Please try again later.'
      } else if (error.response.data?.detail) {
        errorMessage.value = error.response.data.detail
      } else {
        errorMessage.value = 'Login failed. Please try again.'
      }
    } else if (error.request) {
      errorMessage.value = 'Cannot connect to server. Please check your internet connection.'
    } else {
      errorMessage.value = 'An unexpected error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Tailwind classes are used, no additional styles needed */
</style>