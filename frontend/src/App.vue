<template>
  <div id="app">
    <!-- FIXED UNIFIED HEADER - Only show if NOT on public passbook route -->
    <header v-if="!isPublicPassbook && showNavigation" class="app-header">
      <div class="header-container">
        <!-- LEFT: Clinic Branding -->
        <div class="clinic-brand" @click="navigateTo('/dashboard')">
          <div class="clinic-logo">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div class="clinic-info">
            <div class="clinic-name">Sri Adithya Pet Clinic</div>
            <div class="app-name">Dogger 2.0 • Veterinary Management System</div>
          </div>
        </div>

        <!-- CENTER: Navigation Menu -->
        <nav class="main-nav">
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
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
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
            </svg>
            <span>Records</span>
          </router-link>

          <router-link to="/vaccinations" class="nav-link" active-class="active">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
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
            </svg>
            <span>Rx</span>
          </router-link>
        </nav>

        <!-- RIGHT: User Profile -->
        <div class="user-section">
          <div class="user-profile" @click="toggleUserMenu">
            <div class="user-avatar">{{ getUserInitial }}</div>
            <span class="user-username">{{ currentUser?.username || 'Admin' }}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>

          <!-- User Dropdown Menu -->
          <div v-if="showUserMenu" class="user-menu-dropdown">
            <button @click="logout" class="dropdown-item logout">
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
    </header>

    <!-- MAIN CONTENT AREA - Scrolls under header -->
    <main class="content-area" :class="{ 'no-header': isPublicPassbook || !showNavigation }">
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
/* === GLOBAL RESET === */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  height: 100%;
  overflow: hidden;
}

body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* === APP CONTAINER - Full Height Layout === */
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f8fafc;
}

/* === FIXED UNIFIED HEADER === */
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-container {
  height: 100%;
  max-width: 1920px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}

/* === CLINIC BRANDING === */
.clinic-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  flex-shrink: 0;
  transition: opacity 0.2s;
}

.clinic-brand:hover {
  opacity: 0.9;
}

.clinic-logo {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  backdrop-filter: blur(10px);
}

.clinic-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.clinic-name {
  color: white;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.app-name {
  color: rgba(255, 255, 255, 0.85);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.01em;
}

/* === NAVIGATION MENU === */
.main-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.main-nav::-webkit-scrollbar {
  display: none;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.12);
  color: white;
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* === USER SECTION === */
.user-section {
  position: relative;
  flex-shrink: 0;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.22);
}

.user-avatar {
  width: 38px;
  height: 38px;
  background: white;
  color: #7C3AED;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}

.user-username {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.user-menu-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  min-width: 180px;
  animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  width: 100%;
  padding: 14px 18px;
  border: none;
  background: none;
  color: #1e293b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
  text-align: left;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout:hover {
  background: #fee2e2;
}

/* === MAIN CONTENT AREA - Perfect Height Usage === */
.content-area {
  flex: 1;
  margin-top: 70px;
  height: calc(100vh - 70px);
  overflow-y: auto;
  overflow-x: hidden;
  background: #f8fafc;
}

.content-area.no-header {
  margin-top: 0;
  height: 100vh;
}

/* Custom Scrollbar */
.content-area::-webkit-scrollbar {
  width: 10px;
}

.content-area::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.content-area::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 5px;
}

.content-area::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 1200px) {
  .header-container {
    gap: 20px;
  }
  
  .nav-link span {
    display: none;
  }
  
  .nav-link {
    padding: 10px 12px;
  }
  
  .app-name {
    display: none;
  }
}

@media (max-width: 768px) {
  .app-header {
    height: 60px;
  }
  
  .content-area {
    margin-top: 60px;
    height: calc(100vh - 60px);
  }
  
  .header-container {
    padding: 0 16px;
    gap: 12px;
  }
  
  .clinic-logo {
    width: 40px;
    height: 40px;
  }
  
  .clinic-name {
    font-size: 16px;
  }
  
  .user-username {
    display: none;
  }
  
  .user-avatar {
    width: 34px;
    height: 34px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .clinic-info {
    display: none;
  }
  
  .nav-link {
    padding: 8px;
  }
}

/* === PRINT STYLES === */
@media print {
  .app-header {
    display: none;
  }
  
  .content-area {
    margin-top: 0;
    height: auto;
    overflow: visible;
  }
}
</style>