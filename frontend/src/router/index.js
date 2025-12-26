// FILE: frontend/src/router/index.js
// Complete working router configuration

import { createRouter, createWebHistory } from 'vue-router'

// Import all views
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PatientsView from '../views/PatientsView.vue'
import OwnersView from '../views/OwnersView.vue'
import MedicalRecordsView from '../views/MedicalRecordsView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import VaccinationsView from '../views/VaccinationsView.vue'
import PrescriptionsView from '../views/PrescriptionsView.vue'
import PassbooksView from '../views/PassbooksView.vue'
import PublicPassbookView from '../views/PublicPassbookView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue'),  // ✅ Changed to LoginView
      meta: { requiresAuth: false }
    },
    {
      path: '/patients',
      name: 'Patients',
      component: () => import('../views/PatientsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/owners',
      name: 'Owners',
      component: () => import('../views/OwnersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/vaccinations',
      name: 'Vaccinations',
      component: () => import('../views/VaccinationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/medical-records',
      name: 'MedicalRecords',
      component: () => import('../views/MedicalRecordsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      name: 'Payments',
      component: () => import('../views/PaymentsView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router