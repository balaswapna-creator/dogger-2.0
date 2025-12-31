<template>
  <div class="passbooks-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
          </svg>
          <h1>Digital Passbooks</h1>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading passbooks...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-card">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Failed to Load Passbooks</h3>
      <p>{{ error }}</p>
      <button @click="fetchPassbooks" class="btn-retry">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="passbooks.length === 0" class="empty-state-card">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
      </svg>
      <h3>No Digital Passbooks Found</h3>
      <p>Create digital passbooks from the patient details page to track medical history.</p>
    </div>

    <!-- Passbooks Grid -->
    <div v-else class="passbooks-grid">
      <div v-for="passbook in passbooks" :key="passbook.id" class="passbook-card">
        <div class="passbook-header">
          <div class="qr-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
              <rect x="3" y="3" width="8" height="8" rx="1"></rect>
              <rect x="3" y="13" width="8" height="8" rx="1"></rect>
              <rect x="13" y="3" width="8" height="8" rx="1"></rect>
              <rect x="13" y="13" width="3" height="3"></rect>
              <rect x="18" y="13" width="3" height="3"></rect>
              <rect x="13" y="18" width="3" height="3"></rect>
              <rect x="18" y="18" width="3" height="3"></rect>
            </svg>
          </div>
        </div>
        
        <div class="passbook-content">
          <h3>{{ getPatientName(passbook) }}</h3>
          <div class="passbook-details">
            <div class="detail-row">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>{{ getOwnerName(passbook) }}</span>
            </div>
            <div class="detail-row qr-code">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
              <span class="qr-id">{{ getAccessToken(passbook) }}</span>
            </div>
          </div>
        </div>
        
        <button @click="viewPassbook(passbook.id)" class="btn-view-passbook">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          View Passbook
        </button>
      </div>
    </div>
  </div>
</template>

<script>
<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'PassbooksView',
  setup() {
    const passbooks = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchPassbooks = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await api.get('/passbooks/')
        
        // ✅ Handle array or paginated response
        const data = response.data || []
        passbooks.value = Array.isArray(data) ? data : (data.results || [])
        
        console.log('Passbooks loaded:', passbooks.value)
        
      } catch (err) {
        console.error('Error fetching passbooks:', err)
        error.value = 'Failed to load passbooks. Please try again.'
        passbooks.value = []
      } finally {
        loading.value = false
      }
    }

    // ✅ Safe helper functions
    const getPatientName = (passbook) => {
      if (!passbook) return 'Unknown'
      if (passbook.patient_name) return passbook.patient_name
      if (passbook.patient?.pet_name) return passbook.patient.pet_name
      return 'Unknown Patient'
    }

    const getOwnerName = (passbook) => {
      if (!passbook) return 'Unknown'
      if (passbook.owner_name) return passbook.owner_name
      if (passbook.patient?.owner_name) return passbook.patient.owner_name
      return 'Unknown Owner'
    }

    const getAccessToken = (passbook) => {
      if (!passbook) return 'N/A'
      if (passbook.access_token) return String(passbook.access_token).slice(0, 8)
      if (passbook.id) return String(passbook.id).slice(0, 8)
      return 'N/A'
    }

    const viewPassbook = (passbookId) => {
      if (!passbookId) {
        console.error('No passbook ID provided')
        return
      }
      
      // Find the passbook to get its access_token
      const passbook = passbooks.value.find(pb => pb.id === passbookId)
      
      if (passbook) {
        const token = passbook.access_token || passbook.id
        console.log('Opening passbook with token:', token)
        // ✅ FIXED: Use correct public endpoint URL
        window.open(`/passbook/public/${token}`, '_blank')
      } else {
        alert('Passbook not found')
      }
    }

    onMounted(() => {
      fetchPassbooks()
    })

    return {
      passbooks,
      loading,
      error,
      getPatientName,
      getOwnerName,
      getAccessToken,
      viewPassbook,
      fetchPassbooks
    }
  }
}
</script>

<style scoped>
.passbooks-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-title svg {
  color: #14B8A6;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #14B8A6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-card, .empty-state-card {
  background: white;
  border-radius: 16px;
  padding: 60px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.error-card svg {
  color: #EF4444;
  margin-bottom: 16px;
}

.empty-state-card svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.error-card h3, .empty-state-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.error-card p, .empty-state-card p {
  color: #6B7280;
  margin: 0 0 24px 0;
  max-width: 400px;
  margin: 0 auto;
}

.btn-retry {
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 24px;
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4);
}

.passbooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.passbook-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.passbook-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(20, 184, 166, 0.15);
}

.passbook-header {
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px;
}

.qr-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.passbook-content {
  padding: 20px;
}

.passbook-content h3 {
  margin: 0 0 16px 0;
  font-size: 20px;
  font-weight: 700;
  color: #1F2937;
}

.passbook-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  font-size: 14px;
}

.detail-row svg {
  color: #14B8A6;
  flex-shrink: 0;
}

.detail-row.qr-code {
  background: #F0FDFA;
  padding: 8px 12px;
  border-radius: 8px;
}

.qr-id {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #0F766E;
  word-break: break-all;
}

.btn-view-passbook {
  width: 100%;
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  color: white;
  border: none;
  padding: 14px 20px;
  border-top: 1px solid #E5E7EB;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-view-passbook:hover {
  background: linear-gradient(135deg, #0D9488, #0F766E);
}

@media (max-width: 768px) {
  .passbooks-wrapper {
    padding: 16px;
  }
  
  .passbooks-grid {
    grid-template-columns: 1fr;
  }
}
</style>