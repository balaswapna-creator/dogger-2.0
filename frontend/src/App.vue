<template>
  <div id="app">
    <!-- Navigation Bar - Only show if NOT on public passbook route -->
    <nav v-if="!isPublicPassbook && showNavigation" class="navbar">
      <div class="navbar-content">
        <!-- Logo and Title -->
        <div class="navbar-brand" @click="navigateTo('/dashboard')">
          <div class="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div class="brand-info">
            <div class="clinic-name">Sri Adithya Pet Clinic</div>
            <div class="clinic-subtitle">Veterinary Management</div>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="nav-menu">
          <router-link to="/dashboard" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span>Dashboard</span>
          </router-link>

          <router-link to="/patients" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>Patients</span>
          </router-link>

          <router-link to="/owners" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span>Owners</span>
          </router-link>

          <router-link to="/medical-records" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <span>Records</span>
          </router-link>

          <router-link to="/vaccinations" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
            </svg>
            <span>Vaccines</span>
          </router-link>

          <router-link to="/payments" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
            <span>Payments</span>
          </router-link>

          <router-link to="/passbooks" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <span>Passbooks</span>
          </router-link>

          <router-link to="/prescriptions" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <span>Rx</span>
          </router-link>
        </div>

        <!-- User Menu -->
        <div class="user-section">
          <div class="user-badge" @click="toggleUserMenu">
            <div class="user-initial">{{ getUserInitial }}</div>
            <div class="user-name">{{ currentUser?.username || 'Admin' }}</div>
          </div>

          <!-- Dropdown -->
          <div v-if="showUserMenu" class="user-dropdown">
            <button @click="logout" class="logout-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from './services/api'

const router = useRouter()
const route = useRoute()

const showUserMenu = ref(false)
const currentUser = ref(null)

const showNavigation = computed(() => {
  return route.path !== '/login'
})

const getUserInitial = computed(() => {
  if (!currentUser.value?.username) return 'A'
  return currentUser.value.username.charAt(0).toUpperCase()
})

// Check if current route is the public passbook
const isPublicPassbook = computed(() => {
  return route.path.includes('/passbook/public/')
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const logout = () => {
  if (confirm('Are you sure you want to logout?')) {
    api.logout()
  }
}

const navigateTo = (path) => {
  router.push(path)
}

const loadUser = () => {
  currentUser.value = api.getUserProfile()
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.user-section')) {
    showUserMenu.value = false
  }
}

watch(() => route.path, () => {
  showUserMenu.value = false
})

loadUser()

if (typeof window !== 'undefined') {
  window.addEventListener('click', handleClickOutside)
}
</script>

<style>
/* Global Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

/* App Container - VERTICAL LAYOUT */
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: #f5f7fa;
}

body {
  margin: 0;
  padding: 0;
}

/* Navigation Bar */
.navbar {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
}

.navbar-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 16px;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex-shrink: 0;
}

.logo {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.clinic-name {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
}

.clinic-subtitle {
  font-size: 11px;
  opacity: 0.9;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  overflow-x: auto;
  scrollbar-width: none;
}

.nav-menu::-webkit-scrollbar {
  display: none;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.15);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.user-section {
  position: relative;
  flex-shrink: 0;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-badge:hover {
  background: rgba(255, 255, 255, 0.2);
}

.user-initial {
  width: 36px;
  height: 36px;
  background: white;
  color: #7C3AED;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-width: 160px;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.logout-btn {
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  color: #ef4444;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #fee2e2;
}

/* Main Content - TAKES REMAINING SPACE */
.main-content {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Responsive */
@media (max-width: 1024px) {
  .nav-item span {
    display: none;
  }
  
  .nav-item {
    padding: 10px;
  }
  
  .clinic-subtitle {
    display: none;
  }
}

@media (max-width: 768px) {
  .navbar-content {
    gap: 12px;
    height: 56px;
  }
  
  .clinic-name {
    font-size: 14px;
  }
  
  .user-name {
    display: none;
  }
  
  .user-initial {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>