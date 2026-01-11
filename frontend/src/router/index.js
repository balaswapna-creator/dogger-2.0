// frontend/src/router/index.js
// Complete corrected router with security guards

import { createRouter, createWebHistory } from 'vue-router';
import { TokenManager, UserManager, SecurityMonitor } from '@/utils/security';
import TestSecureForms from '@/views/TestSecureForms.vue';

// Import views
import Login from '@/views/Login.vue';
import DashboardView from '@/views/DashboardView.vue';
import Unauthorized from '@/views/Unauthorized.vue';
import NotFound from '@/views/NotFound.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { 
      requiresAuth: true,
      roles: ['admin', 'doctor', 'staff']
    }
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: Unauthorized,
    meta: { requiresAuth: false }
  },
  {
    path: '/test-forms',
    name: 'TestForms',
    component: TestSecureForms,
    meta: { requiresAuth: false }  // Public for testing
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiredRoles = to.meta.roles || [];
  const isAuthenticated = TokenManager.isAuthenticated();
  
  console.log('🛡️ Router Guard Check:', {
    path: to.path,
    requiresAuth,
    requiredRoles,
    isAuthenticated
  });

  // Public routes - allow access
  if (!requiresAuth) {
    console.log('✅ Public route, allowing access');
    SecurityMonitor.logSecurityEvent('route_access', { 
      path: to.path, 
      public: true 
    });
    next();
    return;
  }

  // Authentication check
  if (!isAuthenticated) {
    console.warn('⚠️ Not authenticated, redirecting to login');
    SecurityMonitor.logSecurityEvent('unauthorized_access_attempt', { 
      path: to.path,
      reason: 'not_authenticated'
    });
    next({ 
      name: 'Login', 
      query: { redirect: to.fullPath } 
    });
    return;
  }

  // Role-based access check
  if (requiredRoles.length > 0) {
    const user = UserManager.getUser();
    
    console.log('👤 Current User Data:', {
      username: user?.username,
      role: user?.role,
      is_staff: user?.is_staff,
      is_superuser: user?.is_superuser
    });
    
    console.log('🔐 Required Roles:', requiredRoles);

    if (!user) {
      console.error('❌ No user data found in storage!');
      SecurityMonitor.logSecurityEvent('no_user_data', { path: to.path });
      TokenManager.clearTokens();
      next({ name: 'Login', query: { redirect: to.fullPath } });
      return;
    }

    const userRole = user.role;
    const hasRequiredRole = userRole && requiredRoles.includes(userRole);
    const isStaffUser = user.is_staff === true;
    const isSuperUser = user.is_superuser === true;
    
    console.log('🔍 Access Check:', {
      hasRequiredRole,
      isStaffUser,
      isSuperUser
    });
    
    if (hasRequiredRole || isStaffUser || isSuperUser) {
      console.log('✅ Access granted!');
      SecurityMonitor.logSecurityEvent('route_access', { 
        path: to.path, 
        user: user.username,
        role: userRole,
        grantReason: hasRequiredRole ? 'role_match' : 'staff_override'
      });
      next();
      return;
    }
    
    console.warn('❌ Access denied - Insufficient permissions:', {
      userRole,
      requiredRoles,
      isStaff: isStaffUser,
      isSuperUser
    });
    
    SecurityMonitor.logSecurityEvent('insufficient_permissions', {
      path: to.path,
      userRole,
      requiredRoles,
      username: user.username
    });
    
    next({ name: 'Unauthorized' });
    return;
  }

  // Default - allow access
  console.log('✅ No special requirements, allowing access');
  SecurityMonitor.logSecurityEvent('route_access', { 
    path: to.path, 
    user: UserManager.getUser()?.username 
  });
  next();
});

export default router;