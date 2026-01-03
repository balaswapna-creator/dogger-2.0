<template>
  <div id="app">
    <!-- ✅ UNIFIED FIXED HEADER -->
    <header v-if="isLoggedIn && $route.path !== '/login'" class="app-header">
      <div class="header-container">
        <!-- Left: Clinic Branding -->
        <div class="clinic-brand">
          <div class="logo-box">
            <img src="/logo.png" alt="Logo" class="logo-img" />
          </div>
          <div class="clinic-text">
            <h1>Sri Adithya Pet Clinic</h1>
            <span class="app-name">Dogger 2.0</span>
          </div>
        </div>

        <!-- Right: Navigation & Logout -->
        <div class="header-actions">
          <nav class="nav-menu">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            <router-link to="/patients" class="nav-link">Patients</router-link>
            <router-link to="/owners" class="nav-link">Owners</router-link>
            <router-link to="/medical-records" class="nav-link">Records</router-link>
            <router-link to="/vaccinations" class="nav-link">Vaccines</router-link>
            <router-link to="/payments" class="nav-link">Payments</router-link>
            <router-link to="/passbooks" class="nav-link">Passbooks</router-link>
          </nav>
          <button @click="logout" class="btn-logout">Logout</button>
        </div>
      </div>
    </header>
    
    <!-- ✅ CONTENT AREA - Pushed down by header height -->
    <main :class="{ 'with-header': isLoggedIn && $route.path !== '/login' }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
}

/* ✅ FIXED UNIFIED HEADER */
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);
  z-index: 1000;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Clinic Branding - Left Side */
.clinic-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-box {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 8px;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.clinic-text h1 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
}

.app-name {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Navigation & Actions - Right Side */
.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-menu {
  display: flex;
  gap: 4px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ✅ CONTENT AREA - Pushed down by header */
main.with-header {
  margin-top: 64px; /* Must match header height */
  min-height: calc(100vh - 64px);
}

/* ✅ RESPONSIVE */
@media (max-width: 1024px) {
  .nav-menu {
    gap: 2px;
  }
  
  .nav-link {
    padding: 8px 10px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .app-header {
    height: auto;
    min-height: 64px;
  }
  
  .header-container {
    flex-direction: column;
    padding: 12px 16px;
    gap: 12px;
  }
  
  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  main.with-header {
    margin-top: 120px; /* Adjust for wrapped mobile header */
  }
}
</style>