<template>
  <div class="passbook-public-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading passbook...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Unable to Load Passbook</h2>
      <p>{{ error }}</p>
      <button @click="retry" class="btn-retry">Try Again</button>
    </div>

    <!-- Passbook Content -->
    <div v-else-if="passbook" class="passbook-content">
      <!-- Header -->
      <div class="passbook-header">
        <div class="clinic-logo">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
        </div>
        <h1>Sri Adithya Pet Clinic</h1>
        <p class="subtitle">Digital Health Passbook</p>
      </div>

      <!-- Patient Info -->
      <div class="info-card patient-card">
        <h2>🐾 Patient Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Pet Name:</span>
            <span class="value">{{ patient?.pet_name || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Species:</span>
            <span class="value">{{ patient?.species || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Breed:</span>
            <span class="value">{{ patient?.breed || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Age:</span>
            <span class="value">{{ patient?.age || 'N/A' }} years</span>
          </div>
        </div>
      </div>

      <!-- Owner Info -->
      <div class="info-card owner-card" v-if="owner">
        <h2>👤 Owner Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Name:</span>
            <span class="value">{{ owner.name }}</span>
          </div>
          <div class="info-item">
            <span class="label">Phone:</span>
            <span class="value">{{ owner.phone }}</span>
          </div>
        </div>
      </div>

      <!-- Medical Records -->
      <div class="info-card">
        <h2>🏥 Medical History</h2>
        <div v-if="medicalRecords.length === 0" class="empty-state">
          <p>No medical records found</p>
        </div>
        <div v-else class="records-list">
          <div v-for="record in medicalRecords" :key="record.id" class="record-item">
            <div class="record-date">{{ formatDate(record.visit_date) }}</div>
            <div class="record-details">
              <strong>{{ record.chief_complaint }}</strong>
              <p>{{ record.diagnosis }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Vaccinations -->
      <div class="info-card">
        <h2>💉 Vaccination Records</h2>
        <div v-if="vaccinations.length === 0" class="empty-state">
          <p>No vaccinations recorded</p>
        </div>
        <div v-else class="vaccination-list">
          <div v-for="vacc in vaccinations" :key="vacc.id" class="vaccination-item">
            <div class="vacc-name">{{ vacc.vaccine_name }}</div>
            <div class="vacc-date">{{ formatDate(vacc.vaccination_date) }}</div>
            <div class="vacc-next" v-if="vacc.next_due_date">
              Next: {{ formatDate(vacc.next_due_date) }}
            </div>
          </div>
        </div>
      </div>

      <!-- QR Code -->
      <div class="qr-code-section">
        <p class="qr-text">Share this passbook URL to give access to medical records</p>
        <div class="passbook-url">{{ currentUrl }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const API_BASE_URL = 'https://dogger2-backend.onrender.com/api'

const passbook = ref(null)
const patient = ref(null)
const owner = ref(null)
const medicalRecords = ref([])
const vaccinations = ref([])
const loading = ref(true)
const error = ref(null)

const currentUrl = computed(() => window.location.href)

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const fetchPassbookData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const token = route.params.token
    console.log('Fetching passbook with token:', token)

    // Fetch passbook data
    const passbookResponse = await axios.get(`${API_BASE_URL}/passbooks-public/${token}/`)
    passbook.value = passbookResponse.data
    console.log('Passbook data:', passbook.value)

    // Extract patient ID
    const patientId = passbook.value.patient?.id || passbook.value.patient

    if (patientId) {
      // Fetch patient details
      const patientResponse = await axios.get(`${API_BASE_URL}/patients/${patientId}/`)
      patient.value = patientResponse.data

      // Fetch owner if available
      const ownerId = patient.value.owner?.id || patient.value.owner
      if (ownerId) {
        const ownerResponse = await axios.get(`${API_BASE_URL}/owners/${ownerId}/`)
        owner.value = ownerResponse.data
      }

      // Fetch medical records for this patient
      const recordsResponse = await axios.get(`${API_BASE_URL}/medical-records/`)
      const allRecords = Array.isArray(recordsResponse.data) 
        ? recordsResponse.data 
        : (recordsResponse.data.results || [])
      
      medicalRecords.value = allRecords.filter(r => {
        const recordPatientId = r.patient?.id || r.patient
        return String(recordPatientId) === String(patientId)
      })

      // Fetch vaccinations for this patient
      const vaccinationsResponse = await axios.get(`${API_BASE_URL}/vaccinations/`)
      const allVaccinations = Array.isArray(vaccinationsResponse.data)
        ? vaccinationsResponse.data
        : (vaccinationsResponse.data.results || [])
      
      vaccinations.value = allVaccinations.filter(v => {
        const vaccPatientId = v.patient?.id || v.patient
        return String(vaccPatientId) === String(patientId)
      })
    }

  } catch (err) {
    console.error('Error fetching passbook:', err)
    error.value = err.response?.data?.detail || 'Failed to load passbook. Please check the URL and try again.'
  } finally {
    loading.value = false
  }
}

const retry = () => {
  fetchPassbookData()
}

onMounted(() => {
  fetchPassbookData()
})
</script>

<style scoped>
.passbook-public-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: 40px 20px;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 80px 20px;
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

.error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.btn-retry {
  margin-top: 20px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
}

.passbook-content {
  max-width: 800px;
  margin: 0 auto;
}

.passbook-header {
  text-align: center;
  background: white;
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.clinic-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 20px;
}

.passbook-header h1 {
  font-size: 32px;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.info-card h2 {
  font-size: 20px;
  color: #1a1a1a;
  margin: 0 0 20px 0;
  padding-bottom: 16px;
  border-bottom: 2px solid #f3f4f6;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
}

.value {
  font-size: 15px;
  color: #1a1a1a;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #9ca3af;
}

.records-list,
.vaccination-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item,
.vaccination-item {
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid #7C3AED;
}

.record-date,
.vacc-date {
  font-size: 13px;
  color: #7C3AED;
  font-weight: 600;
  margin-bottom: 8px;
}

.record-details strong {
  color: #1a1a1a;
  font-size: 15px;
}

.record-details p {
  margin: 4px 0 0 0;
  color: #6b7280;
  font-size: 14px;
}

.vacc-name {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.vacc-next {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.qr-code-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.qr-text {
  color: #6b7280;
  margin: 0 0 16px 0;
}

.passbook-url {
  background: #f3f4f6;
  padding: 12px;
  border-radius: 8px;
  color: #7C3AED;
  font-family: monospace;
  font-size: 13px;
  word-break: break-all;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .passbook-header {
    padding: 24px;
  }
  
  .passbook-header h1 {
    font-size: 24px;
  }
}
</style>