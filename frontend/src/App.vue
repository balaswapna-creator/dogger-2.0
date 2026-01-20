<template>
  <div id="app">
    <!-- Navigation Header (shown on all pages except login) -->
    <nav v-if="showNavigation" class="navbar">
      <div class="navbar-container">
        <!-- Logo and Title -->
        <div class="navbar-brand" @click="navigateTo('/dashboard')">
          <div class="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div class="brand-text">
            <div class="brand-title">Sri Adithya Pet Clinic</div>
            <div class="brand-subtitle">Veterinary Management System</div>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="navbar-links">
          <router-link to="/dashboard" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span>Dashboard</span>
          </router-link>

          <router-link to="/patients" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <span>Patients</span>
          </router-link>

          <router-link to="/owners" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span>Owners</span>
          </router-link>

          <router-link to="/medical-records" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span>Records</span>
          </router-link>

          <router-link to="/vaccinations" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
              <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
            </svg>
            <span>Vaccines</span>
          </router-link>

          <router-link to="/payments" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
            <span>Payments</span>
          </router-link>

          <router-link to="/passbooks" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <span>Passbooks</span>
          </router-link>

          <router-link to="/prescriptions" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="12" y1="18" x2="12" y2="12"></line>
              <line x1="9" y1="15" x2="15" y2="15"></line>
            </svg>
            <span>Prescriptions</span>
          </router-link>
        </div>

        <!-- User Menu -->
        <div class="navbar-user">
          <div class="user-info" @click="toggleUserMenu">
            <div class="user-avatar">
              {{ getUserInitial }}
            </div>
            <div class="user-details">
              <div class="user-name">{{ currentUser?.username || 'Admin' }}</div>
              <div class="user-role">Administrator</div>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>

          <!-- Dropdown Menu -->
          <div v-if="showUserMenu" class="user-dropdown">
            <button @click="logout" class="dropdown-item logout">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main :class="{ 'with-navbar': showNavigation }">
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

// Show navigation on all pages except login
const showNavigation = computed(() => {
  return route.path !== '/login'
})

// Get user initial for avatar
const getUserInitial = computed(() => {
  if (!currentUser.value?.username) return 'A'
  return currentUser.value.username.charAt(0).toUpperCase()
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

// Load current user
const loadUser = () => {
  currentUser.value = api.getUserProfile()
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.navbar-user')) {
    showUserMenu.value = false
  }
}

// Watch for route changes to close menu
watch(() => route.path, () => {
  showUserMenu.value = false
})

// Initialize
loadUser()

// Add click listener for closing dropdown
if (typeof window !== 'undefined') {
  window.addEventListener('click', handleClickOutside)
}
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f5f7fa;
  min-height: 100vh;
}

/* Navigation Bar */
.navbar {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
  height: 70px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.navbar-brand:hover {
  opacity: 0.9;
}

.logo {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  white-space: nowrap;
}

.brand-subtitle {
  font-size: 11px;
  opacity: 0.85;
  font-weight: 500;
  white-space: nowrap;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-user {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.1);
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.15);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  backdrop-filter: blur(10px);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  line-height: 1;
}

.user-role {
  font-size: 11px;
  opacity: 0.85;
  line-height: 1;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  overflow: hidden;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  transition: all 0.3s;
  text-align: left;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout:hover {
  background: #fee2e2;
}

/* Main Content */
main {
  min-height: calc(100vh - 70px);
}

main.with-navbar {
  padding-top: 0;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .navbar-links {
    gap: 2px;
  }
  
  .nav-link {
    padding: 10px 12px;
    font-size: 13px;
  }
  
  .nav-link span {
    display: none;
  }
  
  .brand-text {
    display: none;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 16px;
    height: 60px;
  }
  
  .navbar-links {
    overflow-x: auto;
    flex: 1;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .navbar-links::-webkit-scrollbar {
    display: none;
  }
  
  .nav-link {
    padding: 8px;
    min-width: 44px;
    justify-content: center;
  }
  
  .user-details {
    display: none;
  }
}
</style>