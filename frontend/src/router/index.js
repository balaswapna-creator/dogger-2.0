import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PatientsView from '../views/PatientsView.vue'
import PatientDetailView from '../views/PatientDetailView.vue'
import OwnersView from '../views/OwnersView.vue'
import MedicalRecordsView from '../views/MedicalRecordsView.vue'
import VaccinationsView from '../views/VaccinationsView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import PrescriptionsView from '../views/PrescriptionsView.vue'
import PassbooksView from '../views/PassbooksView.vue'
import PublicPassbookView from '../views/PublicPassbookView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/',
      redirect: '/dashboard',
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/patients',
      name: 'Patients',
      component: () => import('../views/PatientsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/patients/:id',
      name: 'PatientDetail',
      component: () => import('../views/PatientDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/owners',
      name: 'Owners',
      component: () => import('../views/OwnersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/medical-records',
      name: 'MedicalRecords',
      component: () => import('../views/MedicalRecordsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/vaccinations',
      name: 'Vaccinations',
      component: () => import('../views/VaccinationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      name: 'Payments',
      component: () => import('../views/PaymentsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/prescriptions',
      name: 'Prescriptions',
      component: () => import('../views/PrescriptionsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/passbooks',
      name: 'Passbooks',
      component: () => import('../views/PassbooksView.vue'),
      meta: { requiresAuth: true }
    },
    // ✅ PUBLIC PASSBOOK ROUTE (NO AUTH REQUIRED)
    {
      path: '/passbook/public/:token',
      name: 'PublicPassbook',
      component: () => import('../views/PublicPassbookView.vue'),
      meta: { requiresAuth: false }
    },
    // ✅ 404 Catch-all route
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFoundView.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  console.log('Router navigation:', { to: to.path, from: from.path, hasToken: !!token, requiresAuth })

  if (requiresAuth && !token) {
    console.log('No token, redirecting to login')
    next('/login')
  } else if (to.path === '/login' && token) {
    console.log('Already logged in, redirecting to dashboard')
    next('/dashboard')
  } else {
    console.log('Navigation allowed')
    next()
  }
})

export default router

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router