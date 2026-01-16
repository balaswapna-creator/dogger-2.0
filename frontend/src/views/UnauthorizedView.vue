<template>
  <div class="unauthorized-container">
    <div class="unauthorized-content">
      <div class="lock-icon">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      
      <h1>Access Denied</h1>
      <p>You don't have permission to access this page.</p>
      <p class="error-code">Error Code: 403 - Unauthorized</p>
      
      <div class="actions">
        <button @click="goBack" class="btn-secondary">
          Go Back
        </button>
        <button @click="goToDashboard" class="btn-primary">
          Go to Dashboard
        </button>
      </div>
      
      <p class="contact-info">
        If you believe this is an error, please contact your administrator.
      </p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}

const goToDashboard = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
.unauthorized-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.unauthorized-content {
  background: white;
  padding: 60px 40px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.lock-icon {
  color: #e53e3e;
  margin-bottom: 30px;
}

.lock-icon svg {
  display: inline-block;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

h1 {
  font-size: 32px;
  color: #2d3748;
  margin-bottom: 16px;
  font-weight: 700;
}

p {
  color: #718096;
  font-size: 16px;
  margin-bottom: 12px;
  line-height: 1.6;
}

.error-code {
  font-family: monospace;
  font-size: 14px;
  color: #a0aec0;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 30px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-secondary:hover {
  background: #cbd5e0;
  transform: translateY(-2px);
}

.contact-info {
  font-size: 14px;
  color: #a0aec0;
  font-style: italic;
}

@media (max-width: 640px) {
  .unauthorized-content {
    padding: 40px 24px;
  }
  
  h1 {
    font-size: 24px;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>