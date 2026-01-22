<template>
  <div class="passbook-detail-container">
    <div class="passbook-header">
      <button @click="goBack" class="btn-back">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        Back
      </button>
      <h1>Digital Passbook</h1>
      <div></div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading passbook...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Error Loading Passbook</h2>
      <p>{{ error }}</p>
    </div>

    <!-- Passbook Content -->
    <div v-else-if="passbook" class="passbook-content">
      <div class="passbook-card">
        <h2>{{ patient?.pet_name || 'Unknown' }}'s Health Passbook</h2>
        
        <div class="passbook-info">
          <div class="info-row">
            <span class="label">Status:</span>
            <span :class="['status-badge', passbook.is_active ? 'active' : 'inactive']">
              {{ passbook.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          
          <div class="info-row" v-if="passbook.subscription_end">
            <span class="label">Valid Until:</span>
            <span>{{ formatDate(passbook.subscription_end) }}</span>
          </div>
          
          <div class="info-row">
            <span class="label">Access Count:</span>
            <span>{{ passbook.access_count || 0 }} times</span>
          </div>
        </div>

        <div class="passbook-actions">
          <button @click="viewPublicPassbook" class="btn-view-public">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            View Public Passbook
          </button>
          
          <button @click="sharePassbook" class="btn-share">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="18" cy="5" r="3"></circle>
              <circle cx="6" cy="12" r="3"></circle>
              <circle cx="18" cy="19" r="3"></circle>
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
              <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
            </svg>
            Share Link
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const passbook = ref(null)
const patient = ref(null)
const loading = ref(true)
const error = ref(null)

const publicUrl = computed(() => {
  if (!passbook.value?.access_token) return ''
  return `${window.location.origin}/passbook/public/${passbook.value.access_token}`
})

const fetchPassbook = async () => {
  try {
    loading.value = true
    const passbookId = route.params.id
    
    const response = await api.getPassbook(passbookId)
    passbook.value = response.data
    
    // Fetch patient info
    if (passbook.value.patient) {
      const patientId = passbook.value.patient.id || passbook.value.patient
      const patientResponse = await api.getPatient(patientId)
      patient.value = patientResponse.data
    }
    
  } catch (err) {
    console.error('Error fetching passbook:', err)
    error.value = err.response?.data?.detail || 'Failed to load passbook'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/passbooks')
}

const viewPublicPassbook = () => {
  if (passbook.value?.access_token) {
    window.open(`/passbook/public/${passbook.value.access_token}`, '_blank')
  }
}

const sharePassbook = async () => {
  if (publicUrl.value) {
    try {
      await navigator.clipboard.writeText(publicUrl.value)
      alert('✅ Passbook link copied to clipboard!')
    } catch (err) {
      prompt('Copy this link:', publicUrl.value)
    }
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchPassbook()
})
</script>

<style scoped>
.passbook-detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.passbook-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.passbook-header h1 {
  font-size: 28px;
  color: #1a1a1a;
  margin: 0;
}

.btn-back {
  background: white;
  border: 2px solid #e5e7eb;
  color: #374151;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #7C3AED;
  color: #7C3AED;
}

.loading-state, .error-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #7C3AED;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.passbook-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.passbook-card h2 {
  font-size: 24px;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  padding-bottom: 16px;
  border-bottom: 2px solid #f3f4f6;
}

.passbook-info {
  margin-bottom: 32px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.label {
  font-weight: 600;
  color: #6b7280;
  min-width: 120px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
}

.status-badge.active {
  background: #d1fae5;
  color: #047857;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #dc2626;
}

.passbook-actions {
  display: flex;
  gap: 16px;
}

.btn-view-public,
.btn-share {
  flex: 1;
  padding: 14px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  border: none;
}

.btn-view-public {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-view-public:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.btn-share {
  background: white;
  color: #7C3AED;
  border: 2px solid #7C3AED;
}

.btn-share:hover {
  background: #f9fafb;
}

.error-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .passbook-actions {
    flex-direction: column;
  }
}
</style>