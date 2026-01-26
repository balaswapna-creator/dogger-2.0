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
    <div v-else-if="passbookData" class="passbook-content">
      <!-- Header -->
      <div class="passbook-header">
        <div class="clinic-logo">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
        </div>
        <h1>{{ passbookData.clinic_name || 'Sri Adithya Pet Clinic' }}</h1>
        <p class="subtitle">Digital Health Passbook</p>
      </div>

      <!-- Patient Info with Photo -->
      <div class="info-card patient-card">
        <h2>🐾 Patient Information</h2>
        
        <!-- Photo -->
        <div v-if="passbookData.photo" class="patient-photo">
          <img :src="passbookData.photo" :alt="passbookData.pet_name" />
        </div>
        
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Pet Name:</span>
            <span class="value">{{ passbookData.pet_name || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Species:</span>
            <span class="value">{{ passbookData.species || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Breed:</span>
            <span class="value">{{ passbookData.breed || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Gender:</span>
            <span class="value">{{ passbookData.gender || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Age:</span>
            <span class="value">{{ passbookData.age || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Color:</span>
            <span class="value">{{ passbookData.color || 'N/A' }}</span>
          </div>
        </div>
      </div>

      <!-- Owner Info -->
      <div class="info-card owner-card">
        <h2>👤 Owner Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Name:</span>
            <span class="value">{{ passbookData.owner_name || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Phone:</span>
            <span class="value">{{ passbookData.owner_phone || 'N/A' }}</span>
          </div>
        </div>
      </div>

      <!-- Vaccinations -->
      <div class="info-card">
        <h2>💉 Vaccination Records</h2>
        <div v-if="!passbookData.vaccinations || passbookData.vaccinations.length === 0" class="empty-state">
          <p>No vaccination records found</p>
        </div>
        <div v-else class="vaccination-list">
          <div v-for="(vacc, index) in passbookData.vaccinations" :key="index" class="vaccination-item">
            <div class="vacc-name">{{ vacc.vaccine_name }}</div>
            <div class="vacc-date">{{ formatDate(vacc.date_administered) }}</div>
            <div class="vacc-next" v-if="vacc.next_due_date">
              Next Due: {{ formatDate(vacc.next_due_date) }}
            </div>
            <div class="vacc-admin" v-if="vacc.administered_by">
              By: {{ vacc.administered_by }}
            </div>
          </div>
        </div>
      </div>

      <!-- Medical History -->
      <div class="info-card">
        <h2>🏥 Medical History</h2>
        <div v-if="!passbookData.consultations || passbookData.consultations.length === 0" class="empty-state">
          <p>No medical records found</p>
        </div>
        <div v-else class="records-list">
          <div v-for="(record, index) in passbookData.consultations" :key="index" class="record-item">
            <div class="record-date">{{ formatDate(record.visit_date) }} • {{ record.visit_type }}</div>
            <div class="record-details">
              <strong>{{ record.chief_complaint }}</strong>
              <p v-if="record.diagnosis">Diagnosis: {{ record.diagnosis }}</p>
              <p v-if="record.treatment_plan">Treatment: {{ record.treatment_plan }}</p>
              <div class="record-vitals" v-if="record.weight || record.temperature">
                <span v-if="record.weight">Weight: {{ record.weight }}kg</span>
                <span v-if="record.temperature">Temp: {{ record.temperature }}°F</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="qr-code-section">
        <p class="qr-text">Share this passbook URL to give access to medical records</p>
        <div class="passbook-url">{{ currentUrl }}</div>
      </div>
    </div>
  </div>
</template>

// Replace the ENTIRE <script setup> section in PassbookPublicView.vue with this:

import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const API_BASE_URL = 'https://dogger2-backend.onrender.com/api'

const passbookData = ref(null)
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

    // Fetch passbook data - backend returns data directly
    const response = await axios.get(`${API_BASE_URL}/passbooks-public/${token}/`)
    
    console.log('Backend response:', response.data)
    
    // Backend returns the data directly (not nested)
    passbookData.value = response.data
    
    console.log('Passbook data set:', passbookData.value)

  } catch (err) {
    console.error('Error fetching passbook:', err)
    error.value = err.response?.data?.error || 'Failed to load passbook. Please check the URL and try again.'
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
/* Add this to the existing <style scoped> section */

.patient-photo {
  text-align: center;
  margin-bottom: 24px;
}

.patient-photo img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.vacc-admin {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.record-vitals {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  font-size: 13px;
  color: #6b7280;
}
}
</style>