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

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients',
    name: 'Patients',
    component: PatientsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/owners',
    name: 'Owners',
    component: OwnersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/records',
    name: 'MedicalRecords',
    component: MedicalRecordsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/payments',
    name: 'Payments',
    component: PaymentsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/vaccinations',
    name: 'Vaccinations',
    component: VaccinationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/prescriptions',
    name: 'Prescriptions',
    component: PrescriptionsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/passbooks',
    name: 'Passbooks',
    component: PassbooksView,
    meta: { requiresAuth: true }
  },
  {
    path: '/passbook/:token',
    name: 'PublicPassbook',
    component: PublicPassbookView,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  
  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router