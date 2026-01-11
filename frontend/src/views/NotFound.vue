<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <!-- 404 Number -->
      <div>
        <h1 class="text-9xl font-extrabold text-indigo-600">
          404
        </h1>
      </div>

      <!-- Error Message -->
      <div>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          Page Not Found
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          The page you're looking for doesn't exist or has been moved.
        </p>
      </div>

      <!-- Illustration -->
      <div class="flex justify-center py-8">
        <svg class="h-48 w-48 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" 
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <!-- Action Buttons -->
      <div class="mt-8 space-y-3">
        <button
          @click="goToHome"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150"
        >
          Go to Homepage
        </button>
        
        <button
          @click="goBack"
          class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150"
        >
          Go Back
        </button>
      </div>

      <!-- Search or Help -->
      <div class="mt-6">
        <p class="text-xs text-gray-500">
          Try searching for what you need or return to the homepage.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  router.back();
};

const goToHome = () => {
  router.push({ name: 'Dashboard' });
};
</script>