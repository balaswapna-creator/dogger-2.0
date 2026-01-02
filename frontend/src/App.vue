<template>
  <div id="app">
    <!-- Only show navigation if user is logged in -->
    <nav v-if="isLoggedIn && $route.path !== '/login'" class="main-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <h1>🐾 Dogger 2.0</h1>
        </div>
        <div class="nav-links">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/patients" class="nav-link">Patients</router-link>
          <router-link to="/owners" class="nav-link">Owners</router-link>
          <!-- ✅ FIXED: Correct path -->
          <router-link to="/medical-records" class="nav-link">Records</router-link>
          <router-link to="/payments" class="nav-link">Payments</router-link>
          <router-link to="/passbooks" class="nav-link">📖 Passbooks</router-link>
          <router-link to="/vaccinations" class="nav-link">💉 Vaccinations</router-link>
          <button @click="logout" class="btn-logout">Logout</button>
        </div>
      </div>
    </nav>
    
    <!-- Main content area -->
    <main :class="{ 'with-nav': isLoggedIn && $route.path !== '/login' }">
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

.main-nav {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand h1 {
  color: white;
  font-size: 24px;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-left: 12px;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
}

main {
  min-height: calc(100vh - 70px);
}

main.with-nav {
  padding-top: 0;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>