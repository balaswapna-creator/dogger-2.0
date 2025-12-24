<template>
  <div v-if="authStore.isAuthenticated" class="min-h-screen bg-gray-50">
    <!-- Top Navigation Bar -->
    <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="w-full px-6">
        <div class="flex justify-between items-center h-16">
          <!-- Logo & Title -->
          <div class="flex items-center gap-3">
            <span class="text-2xl">🐾</span>
            <h1 class="text-xl font-bold text-gray-900">Dogger 2.0</h1>
          </div>
          
          <!-- Navigation Links -->
          <div class="flex items-center gap-1">
            <router-link
              to="/"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/' }"
            >
              Dashboard
            </router-link>
            <router-link
              to="/patients"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/patients' }"
            >
              Patients
            </router-link>
            <router-link
              to="/owners"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/owners' }"
            >
              Owners
            </router-link>
            <router-link
              to="/records"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/records' }"
            >
              Records
            </router-link>
            <router-link
              to="/payments"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/payments' }"
            >
              Payments
            </router-link>
            <router-link
              to="/vaccinations" 
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
              :class="{ 'bg-blue-50 text-blue-600 font-medium': $route.path === '/vaccinations' }"
            >
            <router-link to="/passbooks" class="text-emerald-600 hover:text-emerald-700 font-medium">
              🎫 Passbooks
            </router-link>
            >
              💉 Vaccinations
            </router-link>
          </div>       
          
          <!-- Logout Button -->
          <button
            @click="logout"
            class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
    
    <!-- Main Content -->
    <router-view />
  </div>
  
  <!-- Login View (No Navigation) -->
  <router-view v-else />
</template>

<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
}
</script>