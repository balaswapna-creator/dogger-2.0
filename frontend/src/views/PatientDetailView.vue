<template>
  <div class="patient-detail-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading patient information...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Error Loading Patient</h2>
      <p>{{ error }}</p>
      <button @click="$router.push('/patients')" class="btn-back">
        Back to Patients
      </button>
    </div>

    <!-- Patient Detail -->
    <div v-else-if="patient" class="patient-detail">
      <!-- Header -->
      <div class="detail-header">
        <button @click="$router.push('/patients')" class="btn-back">
          ← Back to Patients
        </button>
        <h1>{{ patient.pet_name }}</h1>
      </div>

      <!-- Patient Info Card -->
      <div class="info-card">
        <div class="card-header">
          <h2>🐾 Patient Information</h2>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <div class="photo-section" v-if="patient.photo">
              <img :src="getPhotoUrl(patient.photo)" :alt="patient.pet_name" class="patient-photo" />
            </div>
            <div class="photo-section" v-else>
              <div class="no-photo">📷</div>
            </div>
          </div>
          
          <div class="info-details">
            <div class="detail-row">
              <span class="label">Species:</span>
              <span class="value">{{ patient.species }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Breed:</span>
              <span class="value">{{ patient.breed || 'Not specified' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Age:</span>
              <span class="value">{{ patient.age }} years</span>
            </div>
            <div class="detail-row">
              <span class="label">Gender:</span>
              <span class="value">{{ patient.gender }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Color:</span>
              <span class="value">{{ patient.color || 'Not specified' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Registration Date:</span>
              <span class="value">{{ formatDate(patient.date_of_registration) }}</span>
            </div>
            <div class="detail-row" v-if="patient.microchip_number">
              <span class="label">Microchip:</span>
              <span class="value">{{ patient.microchip_number }}</span>
            </div>
          </div>
        </div>

        <!-- Owner Information -->
        <div class="owner-section" v-if="patient.owner_name">
          <h3>👤 Owner Information</h3>
          <div class="detail-row">
            <span class="label">Name:</span>
            <span class="value">{{ patient.owner_name }}</span>
          </div>
          <div class="detail-row" v-if="patient.owner_phone">
            <span class="label">Phone:</span>
            <span class="value">{{ patient.owner_phone }}</span>
          </div>
          <div class="detail-row" v-if="patient.owner_email">
            <span class="label">Email:</span>
            <span class="value">{{ patient.owner_email }}</span>
          </div>
        </div>
      </div>

      <!-- Digital Passbook Section -->
      <div class="passbook-section info-card">
        <div class="card-header">
          <h2>📖 Digital Passbook</h2>
        </div>
        
        <div v-if="!hasPassbook" class="passbook-create">
          <p class="passbook-info">
            Create a digital passbook for {{ patient.pet_name }} to share medical records with the owner via QR code.
          </p>
          <button @click="showPassbookModal = true" class="btn-create-passbook">
            ➕ Create Digital Passbook
          </button>
        </div>
        
        <div v-else class="passbook-exists">
          <div class="passbook-success">
            <span class="success-icon">✅</span>
            <span>Digital Passbook Active</span>
          </div>
          <button @click="viewPassbook" class="btn-view-passbook">
            👁️ View Passbook
          </button>
        </div>
      </div>

      <!-- Medical Records Section -->
      <div class="records-section info-card">
        <div class="card-header">
          <h2>🏥 Medical Records</h2>
          <span class="record-count">{{ medicalRecords.length }} records</span>
        </div>
        
        <div v-if="medicalRecords.length === 0" class="empty-state">
          <p>No medical records found</p>
        </div>
        
        <div v-else class="records-list">
          <div v-for="record in medicalRecords" :key="record.id" class="record-item">
            <div class="record-date">
              {{ formatDate(record.visit_date) }}
            </div>
            <div class="record-details">
              <div class="record-type">{{ record.visit_type || 'Consultation' }}</div>
              <div class="record-complaint">{{ record.chief_complaint }}</div>
              <div class="record-diagnosis">{{ record.diagnosis }}</div>
            </div>
            <div class="record-fee">
              ₹{{ record.consultation_fee || '0' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Vaccinations Section -->
      <div class="vaccinations-section info-card">
        <div class="card-header">
          <h2>💉 Vaccinations</h2>
          <span class="record-count">{{ vaccinations.length }} vaccinations</span>
        </div>
        
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

      <!-- Payments Section -->
      <div class="payments-section info-card">
        <div class="card-header">
          <h2>💰 Payments</h2>
          <span class="record-count">{{ payments.length }} payments</span>
        </div>
        
        <div v-if="payments.length === 0" class="empty-state">
          <p>No payments recorded</p>
        </div>
        
        <div v-else class="payment-list">
          <div v-for="payment in payments" :key="payment.id" class="payment-item">
            <div class="payment-date">{{ formatDate(payment.payment_date) }}</div>
            <div class="payment-amount">₹{{ payment.total_amount }}</div>
            <div class="payment-method">{{ payment.payment_method }}</div>
            <div class="payment-status" :class="payment.payment_status">
              {{ payment.payment_status }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Passbook Modal -->
    <div v-if="showPassbookModal" class="modal-overlay" @click="showPassbookModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create Digital Passbook</h2>
          <button @click="showPassbookModal = false" class="btn-close">✕</button>
        </div>
        
        <div class="modal-body">
          <p>Are you sure you want to create a digital passbook for <strong>{{ patient?.pet_name }}</strong>?</p>
          <p class="modal-info">This will generate a QR code that the owner can use to access medical records.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="showPassbookModal = false" class="btn-cancel">Cancel</button>
          <button @click="createPassbook" :disabled="creatingPassbook" class="btn-confirm">
            <span v-if="creatingPassbook">Creating...</span>
            <span v-else>Create Passbook</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

export default {
  name: 'PatientDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const patient = ref(null)
    const medicalRecords = ref([])
    const vaccinations = ref([])
    const payments = ref([])
    const passbooks = ref([])
    const loading = ref(true)
    const error = ref(null)
    const showPassbookModal = ref(false)
    const creatingPassbook = ref(false)

    // ✅ FIXED: hasPassbook as computed property
    const hasPassbook = computed(() => {
      if (!patient.value || !passbooks.value || passbooks.value.length === 0) {
        return false
      }
      
      const patientId = String(patient.value.id)
      
      return passbooks.value.some(pb => {
        const passbookPatientId = pb.patient?.id || pb.patient
        return String(passbookPatientId) === patientId
      })
    })

    // Get patient's passbook
    const patientPassbook = computed(() => {
      if (!patient.value || !passbooks.value) return null
      
      const patientId = String(patient.value.id)
      
      return passbooks.value.find(pb => {
        const passbookPatientId = pb.patient?.id || pb.patient
        return String(passbookPatientId) === patientId
      })
    })

    const getPhotoUrl = (photo) => {
      if (!photo) return ''
      if (photo.startsWith('http')) return photo
      return `https://dogger2-backend.onrender.com${photo}`
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-IN', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
    }

    const fetchPatientData = async () => {
      try {
        loading.value = true
        error.value = null
        const patientId = route.params.id

        console.log('Fetching patient data for ID:', patientId)

        // Fetch all data in parallel
        const [
          patientRes,
          recordsRes,
          vaccinationsRes,
          paymentsRes,
          passbooksRes
        ] = await Promise.all([
          api.get(`/patients/${patientId}/`),
          api.get('/medical-records/'),
          api.get('/vaccinations/'),
          api.get('/payments/'),
          api.get('/passbooks/').catch(err => {
            console.log('Passbooks endpoint error:', err)
            return { data: [] }
          })
        ])

        patient.value = patientRes.data
        console.log('Patient loaded:', patient.value)

        // ✅ FIXED: Handle both array and paginated responses
        const allRecords = Array.isArray(recordsRes.data) ? recordsRes.data : (recordsRes.data.results || [])
        const allVaccinations = Array.isArray(vaccinationsRes.data) ? vaccinationsRes.data : (vaccinationsRes.data.results || [])
        const allPayments = Array.isArray(paymentsRes.data) ? paymentsRes.data : (paymentsRes.data.results || [])
        const allPassbooks = Array.isArray(passbooksRes.data) ? passbooksRes.data : (passbooksRes.data.results || [])

        // Filter records for this patient
        medicalRecords.value = allRecords.filter(r => {
          const recordPatientId = r.patient?.id || r.patient
          return String(recordPatientId) === String(patientId)
        })

        vaccinations.value = allVaccinations.filter(v => {
          const vaccinationPatientId = v.patient?.id || v.patient
          return String(vaccinationPatientId) === String(patientId)
        })

        payments.value = allPayments.filter(p => {
          const paymentPatientId = p.patient?.id || p.patient
          return String(paymentPatientId) === String(patientId)
        })

        passbooks.value = allPassbooks
        console.log('Passbooks loaded:', passbooks.value)
        console.log('Has passbook:', hasPassbook.value)

      } catch (err) {
        console.error('Error fetching patient data:', err)
        error.value = err.response?.data?.detail || err.message || 'Failed to load patient data'
      } finally {
        loading.value = false
      }
    }

    const createPassbook = async () => {
      if (!patient.value) return

      try {
        creatingPassbook.value = true
        console.log('Creating passbook for patient:', patient.value.id)

        const response = await api.post('/passbooks/', {
          patient: patient.value.id,
          is_active: true
        })

        console.log('Passbook created:', response.data)
        
        // Refresh passbooks list
        const passbooksRes = await api.get('/passbooks/')
        passbooks.value = Array.isArray(passbooksRes.data) ? passbooksRes.data : (passbooksRes.data.results || [])
        
        showPassbookModal.value = false
        alert('✅ Digital Passbook created successfully!')
        
      } catch (err) {
        console.error('Error creating passbook:', err)
        const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to create passbook'
        alert('❌ ' + errorMsg)
      } finally {
        creatingPassbook.value = false
      }
    }

    const viewPassbook = () => {
      if (patientPassbook.value) {
        // ✅ FIXED: Use correct backend endpoint with access_token
        const token = patientPassbook.value.access_token || patientPassbook.value.id
        console.log('Opening passbook with token:', token)
        // Use the correct public endpoint path
        window.open(`/passbook/public/${token}`, '_blank')
      } else {
        alert('Passbook not found')
      }
    }

    onMounted(() => {
      fetchPatientData()
    })

    return {
      patient,
      medicalRecords,
      vaccinations,
      payments,
      loading,
      error,
      hasPassbook,
      patientPassbook,
      showPassbookModal,
      creatingPassbook,
      getPhotoUrl,
      formatDate,
      createPassbook,
      viewPassbook
    }
  }
}
</script>

<style scoped>
.patient-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-state, .error-state {
  text-align: center;
  padding: 60px 20px;
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
  font-size: 60px;
  margin-bottom: 20px;
}

.detail-header {
  margin-bottom: 30px;
}

.detail-header h1 {
  font-size: 32px;
  color: #1a1a1a;
  margin: 10px 0;
}

.btn-back {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f3f4f6;
}

.card-header h2 {
  font-size: 20px;
  color: #1a1a1a;
  margin: 0;
}

.record-count {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.photo-section {
  text-align: center;
}

.patient-photo {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 16px;
  border: 4px solid #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.no-photo {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  border-radius: 16px;
  margin: 0 auto;
}

.info-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-row .label {
  font-weight: 600;
  color: #6b7280;
  min-width: 150px;
}

.detail-row .value {
  color: #1a1a1a;
  font-weight: 500;
}

.owner-section {
  padding-top: 24px;
  border-top: 2px solid #f3f4f6;
}

.owner-section h3 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #1a1a1a;
}

/* Passbook Section */
.passbook-section {
  background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
  border: 2px solid #06B6D4;
}

.passbook-create, .passbook-exists {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.passbook-info {
  color: #0c4a6e;
  line-height: 1.6;
  flex: 1;
}

.btn-create-passbook {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-create-passbook:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

.passbook-success {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #047857;
  font-weight: 600;
  font-size: 16px;
}

.success-icon {
  font-size: 24px;
}

.btn-view-passbook {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-view-passbook:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* Records Lists */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
  font-style: italic;
}

.records-list, .vaccination-list, .payment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item, .vaccination-item, .payment-item {
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
}

.record-item:hover, .vaccination-item:hover, .payment-item:hover {
  background: #f3f4f6;
  transform: translateX(4px);
}

.record-date, .vacc-date, .payment-date {
  font-weight: 600;
  color: #7C3AED;
  min-width: 100px;
}

.record-details {
  flex: 1;
}

.record-type {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.record-complaint {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.record-diagnosis {
  font-size: 14px;
  color: #6b7280;
}

.record-fee, .payment-amount {
  font-weight: 700;
  color: #10B981;
  font-size: 18px;
}

.payment-method {
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.payment-status {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.payment-status.completed {
  background: #d1fae5;
  color: #047857;
}

.payment-status.pending {
  background: #fef3c7;
  color: #92400e;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #f3f4f6;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #1a1a1a;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #1a1a1a;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  margin: 0 0 12px 0;
  color: #374151;
  line-height: 1.6;
}

.modal-info {
  color: #6b7280;
  font-size: 14px;
}

.modal-footer {
  padding: 24px;
  border-top: 2px solid #f3f4f6;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-confirm {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .passbook-create, .passbook-exists {
    flex-direction: column;
    text-align: center;
  }
  
  .record-item, .payment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>