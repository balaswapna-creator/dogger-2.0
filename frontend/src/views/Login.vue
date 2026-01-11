<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-4">
          <svg class="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800">Dogger 2.0</h1>
        <p class="text-gray-600 mt-2">Veterinary Clinic Management System</p>
        <p class="text-sm text-gray-500 mt-1">Username: <strong>admin</strong></p>
        <p class="text-sm text-gray-500">Version 2.0.0 - Secure Edition</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Username Field -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Username
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            :class="{ 'border-red-500': error }"
            placeholder="Enter your username"
          />
        </div>

        <!-- Password Field -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            :class="{ 'border-red-500': error }"
            placeholder="••••••••"
          />
        </div>

        <!-- Remember Me -->
        <div class="flex items-center">
          <input
            id="remember"
            v-model="rememberMe"
            type="checkbox"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label for="remember" class="ml-2 block text-sm text-gray-700">
            Remember me
          </label>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p class="text-sm">{{ error }}</p>
        </div>

        <!-- Rate Limit Warning -->
        <div v-if="isRateLimited" class="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg">
          <p class="text-sm">Too many login attempts. Please wait {{ rateLimitCountdown }} seconds.</p>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="loading || isRateLimited"
          class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">
            <svg class="animate-spin inline h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Signing in...
          </span>
          <span v-else>Sign in</span>
        </button>

        <!-- Forgot Password Link -->
        <div class="text-center">
          <a href="#" class="text-sm text-blue-600 hover:text-blue-800">
            Forgot password?
          </a>
        </div>
      </form>

      <!-- Footer -->
      <div class="mt-8 text-center text-sm text-gray-500">
        <p>&copy; 2026 Dogger 2.0. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { InputSanitizer, SecurityMonitor } from '@/utils/security';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      loading: false,
      error: null,
      loginAttempts: 0,
      maxAttempts: 5,
      isRateLimited: false,
      rateLimitCountdown: 0,
      rateLimitTimer: null
    };
  },
  methods: {
    async handleLogin() {
      // Clear previous errors
      this.error = null;

      // Check rate limiting
      if (this.isRateLimited) {
        return;
      }

      // Validate inputs
      if (!this.username || !this.password) {
        this.error = 'Please enter both username and password';
        return;
      }

      // Sanitize inputs using correct method names
      const sanitizedUsername = InputSanitizer.sanitizeInput(this.username);
      const sanitizedPassword = InputSanitizer.sanitizeInput(this.password);

      this.loading = true;

      try {
        // Call API login
        const response = await api.login(sanitizedUsername, sanitizedPassword);

        // Reset login attempts on success
        this.loginAttempts = 0;

        // Log successful login
        SecurityMonitor.logSecurityEvent('login_success', {
          username: sanitizedUsername,
          timestamp: new Date().toISOString()
        });

        // Redirect to dashboard or intended page
        const redirect = this.$route.query.redirect || '/dashboard';
        this.$router.push(redirect);

      } catch (err) {
        console.error('Login error:', err);
        
        // Increment login attempts
        this.loginAttempts++;

        // Log failed login attempt
        SecurityMonitor.logSecurityEvent('login_failed', {
          username: sanitizedUsername,
          attempt: this.loginAttempts,
          error: err.response?.data?.detail || err.message
        });

        // Check if rate limit reached
        if (this.loginAttempts >= this.maxAttempts) {
          this.startRateLimitCountdown();
          this.error = 'Too many failed login attempts. Please try again later.';
        } else {
          const remainingAttempts = this.maxAttempts - this.loginAttempts;
          this.error = err.response?.data?.detail || 'Invalid username or password';
          
          if (remainingAttempts <= 2) {
            this.error += ` (${remainingAttempts} attempts remaining)`;
          }
        }
      } finally {
        this.loading = false;
      }
    },

    startRateLimitCountdown() {
      this.isRateLimited = true;
      this.rateLimitCountdown = 60; // 60 seconds cooldown

      this.rateLimitTimer = setInterval(() => {
        this.rateLimitCountdown--;
        
        if (this.rateLimitCountdown <= 0) {
          this.isRateLimited = false;
          this.loginAttempts = 0;
          clearInterval(this.rateLimitTimer);
        }
      }, 1000);
    }
  },

  beforeUnmount() {
    // Clear timer when component is destroyed
    if (this.rateLimitTimer) {
      clearInterval(this.rateLimitTimer);
    }
  }
};
</script>

<style scoped>
/* Add any additional custom styles here */
</style>