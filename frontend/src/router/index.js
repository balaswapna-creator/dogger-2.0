import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PatientsView from '../views/PatientsView.vue'
import OwnersView from '../views/OwnersView.vue'
import RecordsView from '../views/RecordsView.vue'
import VaccinesView from '../views/VaccinesView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import PassbooksView from '../views/PassbooksView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/patients',
      name: 'patients',
      component: PatientsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/owners',
      name: 'owners',
      component: OwnersView,
      meta: { requiresAuth: true }
    },
    {
      path: '/records',
      name: 'records',
      component: RecordsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/vaccines',
      name: 'vaccines',
      component: VaccinesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      name: 'payments',
      component: PaymentsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/passbooks',
      name: 'passbooks',
      component: PassbooksView,
      meta: { requiresAuth: true }
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedView.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

// Simplified authentication guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  // If route requires auth and no token exists
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }
  
  // If trying to access login page while already logged in
  if (to.path === '/login' && token) {
    next('/dashboard')
    return
  }
  
  // Allow navigation
  next()
})

export default router