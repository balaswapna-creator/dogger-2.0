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

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
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
    path: '/patients/:id',
    name: 'PatientDetail',
    component: PatientDetailView,
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
    path: '/vaccinations',
    name: 'Vaccinations',
    component: VaccinationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/payments',
    name: 'Payments',
    component: PaymentsView,
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
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication
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