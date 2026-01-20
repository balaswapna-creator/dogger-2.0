import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PatientsView from '../views/PatientsView.vue'
import OwnersView from '../views/OwnersView.vue'
import MedicalRecordsView from '../views/MedicalRecordsView.vue'
import VaccinationsView from '../views/VaccinationsView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import PassbooksView from '../views/PassbooksView.vue'
import PrescriptionsView from '../views/PrescriptionsView.vue'

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
      path: '/patients/:id',
      name: 'patient-detail',
      component: () => import('../views/PatientDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/owners',
      name: 'owners',
      component: OwnersView,
      meta: { requiresAuth: true }
    },
    {
      path: '/medical-records',
      name: 'medical-records',
      component: MedicalRecordsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/vaccinations',
      name: 'vaccinations',
      component: VaccinationsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      name: 'payments',
      component: PaymentsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/prescriptions',
      name: 'prescriptions',
      component: PrescriptionsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/passbooks',
      name: 'passbooks',
      component: PassbooksView,
      meta: { requiresAuth: true }
    },
    {
      path: '/passbook/public/:token',
      name: 'passbook-public',
      component: () => import('../views/PassbookPublicView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
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