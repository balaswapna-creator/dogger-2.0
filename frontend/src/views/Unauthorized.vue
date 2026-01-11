<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <!-- Lock Icon -->
      <div class="flex justify-center">
        <div class="rounded-full bg-red-100 p-6">
          <svg class="h-16 w-16 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>

      <!-- Error Message -->
      <div>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          Access Denied
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          You don't have permission to access this page.
        </p>
        <p class="mt-4 text-xs text-gray-500">
          Error Code: 403 - Unauthorized
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="mt-8 space-y-3">
        <button
          @click="goBack"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150"
        >
          Go Back
        </button>
        
        <button
          @click="goToDashboard"
          class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150"
        >
          Go to Dashboard
        </button>
      </div>

      <!-- Help Text -->
      <div class="mt-6 text-xs text-gray-500">
        <p>If you believe this is an error, please contact your administrator.</p>
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

const goToDashboard = () => {
  router.push({ name: 'Dashboard' });
};
</script>