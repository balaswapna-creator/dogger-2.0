// COMPLETE PRESCRIPTION VIEW UPDATE
// Replace your entire PrescriptionsView.vue <script setup> section with this:

import { ref, onMounted } from 'vue'
import api from '../services/api'

const prescriptions = ref([])
const consultations = ref([])
const loading = ref(true)
const showModal = ref(false)
const showViewModal = ref(false)
const searchQuery = ref('')
const selectedPrescription = ref(null)

const form = ref({
  medical_record: '',
  medicines: []
})

const createEmptyMedicine = () => ({
  medication_name: '',
  dosage: '',
  frequency: '',
  duration: '',
  instructions: ''
})

const fetchPrescriptions = async () => {
  try {
    loading.value = true
    const response = await api.get('/prescriptions/')
    prescriptions.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error fetching prescriptions:', error)
  } finally {
    loading.value = false
  }
}

const fetchConsultations = async () => {
  try {
    const response = await api.get('/medical-records/')
    consultations.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error fetching consultations:', error)
  }
}

const openModal = () => {
  form.value = {
    medical_record: '',
    medicines: [createEmptyMedicine()]
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const addMedicine = () => {
  form.value.medicines.push(createEmptyMedicine())
}

const removeMedicine = (index) => {
  if (form.value.medicines.length > 1) {
    if (confirm('Remove this medicine?')) {
      form.value.medicines.splice(index, 1)
    }
  } else {
    alert('At least one medicine is required')
  }
}

// ✅ FIXED: Send all medicines in ONE request
const savePrescription = async () => {
  try {
    if (form.value.medicines.length === 0) {
      alert('Please add at least one medicine')
      return
    }

    // Send ALL medicines in ONE API call
    const payload = {
      medical_record: form.value.medical_record || null,
      medicines: form.value.medicines
    }

    await api.post('/prescriptions/', payload)
    alert(`Prescription with ${form.value.medicines.length} medicine(s) created successfully!`)
    
    closeModal()
    fetchPrescriptions()
  } catch (error) {
    console.error('Error saving prescription:', error)
    alert('Failed to save prescription: ' + (error.response?.data?.detail || error.message))
  }
}

const deletePrescription = async (id) => {
  if (!confirm('Are you sure you want to delete this prescription?')) return
  
  try {
    await api.delete(`/prescriptions/${id}/`)
    alert('Prescription deleted successfully!')
    fetchPrescriptions()
  } catch (error) {
    console.error('Error deleting prescription:', error)
    alert('Failed to delete prescription')
  }
}

const viewPrescription = (prescription) => {
  selectedPrescription.value = prescription
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedPrescription.value = null
}

const printPrescription = (prescription) => {
  const medicines = prescription.medicines && prescription.medicines.length > 0
    ? prescription.medicines
    : [{
        medication_name: prescription.medication_name,
        dosage: prescription.dosage,
        frequency: prescription.frequency,
        duration: prescription.duration,
        instructions: prescription.instructions
      }]

  const medicinesHTML = medicines.map((med, idx) => `
    <div class="medication">
      <h3>${idx + 1}. ${med.medication_name}</h3>
      <p><span class="label">Dosage:</span> ${med.dosage}</p>
      <p><span class="label">Frequency:</span> ${med.frequency}</p>
      <p><span class="label">Duration:</span> ${med.duration}</p>
      ${med.instructions ? `<p><span class="label">Instructions:</span> ${med.instructions}</p>` : ''}
    </div>
  `).join('')

  const printWindow = window.open('', '_blank')
  printWindow.document.write(`
    <html>
      <head>
        <title>Prescription - ${prescription.patient_name}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; }
          .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
          .clinic-name { font-size: 24px; font-weight: bold; color: #6366F1; }
          .details { margin: 20px 0; }
          .label { font-weight: bold; color: #666; }
          .rx { font-size: 36px; font-weight: bold; color: #6366F1; margin: 20px 0; }
          .medication { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 15px 0; }
          .medication h3 { margin: 0 0 10px 0; color: #1F2937; }
          .footer { margin-top: 50px; border-top: 1px solid #ccc; padding-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="clinic-name">Sri Adithya Pet Clinic</div>
          <div>Dr. A. Balasubramanan, B.V.Sc, MBA</div>
          <div>Main Road, Cumbum, Tamil Nadu - 625516</div>
        </div>
        
        <div class="details">
          <div><span class="label">Date:</span> ${formatDate(prescription.created_at)}</div>
          <div><span class="label">Patient:</span> ${prescription.patient_name}</div>
        </div>
        
        <div class="rx">℞</div>
        
        ${medicinesHTML}
        
        <div class="footer">
          <p>_________________________</p>
          <p>Dr. A. Balasubramanan</p>
          <p>B.V.Sc, MBA</p>
        </div>
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.print()
}

const searchPrescriptions = async () => {
  if (!searchQuery.value.trim()) {
    fetchPrescriptions()
    return
  }
  
  try {
    loading.value = true
    const response = await api.get(`/prescriptions/?search=${searchQuery.value}`)
    prescriptions.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error searching prescriptions:', error)
  } finally {
    loading.value = false
  }
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

onMounted(() => {
  fetchPrescriptions()
  fetchConsultations()
})

// ============================================
// UPDATE THE TABLE DISPLAY SECTION
// ============================================

// Replace the table body with this:
/*
<tbody>
  <tr v-for="prescription in prescriptions" :key="prescription.id">
    <td>
      <div class="date-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        {{ formatDate(prescription.created_at) }}
      </div>
    </td>
    <td>
      <div class="patient-info">
        <div class="patient-avatar">{{ prescription.patient_name.charAt(0) }}</div>
        <span>{{ prescription.patient_name }}</span>
      </div>
    </td>
    <td>
      <!-- Show medicine count badge -->
      <span class="medicine-count-badge">
        {{ prescription.medicine_count || prescription.medicines?.length || 1 }} Medicine(s)
      </span>
    </td>
    <td colspan="3">
      <!-- Show first medicine or summary -->
      <div v-if="prescription.medicines && prescription.medicines.length > 0" class="medicine-summary">
        <strong>{{ prescription.medicines[0].medication_name }}</strong>
        <span v-if="prescription.medicines.length > 1" class="more-medicines">
          + {{ prescription.medicines.length - 1 }} more
        </span>
      </div>
      <div v-else class="medicine-summary">
        {{ prescription.medication_name || 'No medicines' }}
      </div>
    </td>
    <td>
      <div class="action-buttons">
        <button @click="viewPrescription(prescription)" class="btn-view" title="View All Medicines">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
        <button @click="printPrescription(prescription)" class="btn-print" title="Print">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9"></polyline>
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
            <rect x="6" y="14" width="12" height="8"></rect>
          </svg>
        </button>
        <button @click="deletePrescription(prescription.id)" class="btn-delete" title="Delete Prescription">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </td>
  </tr>
</tbody>
*/

// ============================================
// UPDATE THE VIEW MODAL TO SHOW ALL MEDICINES
// ============================================

// Replace the view modal body with this:
/*
<div class="view-body" v-if="selectedPrescription">
  <div class="detail-section">
    <div class="detail-row">
      <span class="detail-label">Patient:</span>
      <span class="detail-value">{{ selectedPrescription.patient_name }}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Date:</span>
      <span class="detail-value">{{ formatDate(selectedPrescription.created_at) }}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Total Medicines:</span>
      <span class="detail-value">{{ selectedPrescription.medicines?.length || 1 }}</span>
    </div>
  </div>
  
  <!-- ALL MEDICINES LIST -->
  <div class="all-medicines-section">
    <h3>💊 Prescribed Medicines</h3>
    
    <div v-if="selectedPrescription.medicines && selectedPrescription.medicines.length > 0" class="medicines-cards">
      <div v-for="(medicine, index) in selectedPrescription.medicines" :key="index" class="medicine-display-card">
        <div class="medicine-number-badge">Medicine #{{ index + 1 }}</div>
        
        <div class="medication-name-large">{{ medicine.medication_name }}</div>
        
        <div class="medicine-details-grid">
          <div class="detail-item">
            <span class="detail-icon">💊</span>
            <div>
              <div class="detail-label-small">Dosage</div>
              <div class="detail-value-large">{{ medicine.dosage }}</div>
            </div>
          </div>
          
          <div class="detail-item">
            <span class="detail-icon">⏰</span>
            <div>
              <div class="detail-label-small">Frequency</div>
              <div class="detail-value-large">{{ medicine.frequency }}</div>
            </div>
          </div>
          
          <div class="detail-item">
            <span class="detail-icon">📅</span>
            <div>
              <div class="detail-label-small">Duration</div>
              <div class="detail-value-large">{{ medicine.duration }}</div>
            </div>
          </div>
        </div>
        
        <div v-if="medicine.instructions" class="medicine-instructions">
          <strong>Instructions:</strong> {{ medicine.instructions }}
        </div>
      </div>
    </div>
    
    <!-- Fallback for old format -->
    <div v-else class="medicine-display-card">
      <div class="medication-name-large">{{ selectedPrescription.medication_name }}</div>
      <div class="medicine-details-grid">
        <div class="detail-item">
          <span class="detail-icon">💊</span>
          <div>
            <div class="detail-label-small">Dosage</div>
            <div class="detail-value-large">{{ selectedPrescription.dosage }}</div>
          </div>
        </div>
        <div class="detail-item">
          <span class="detail-icon">⏰</span>
          <div>
            <div class="detail-label-small">Frequency</div>
            <div class="detail-value-large">{{ selectedPrescription.frequency }}</div>
          </div>
        </div>
        <div class="detail-item">
          <span class="detail-icon">📅</span>
          <div>
            <div class="detail-label-small">Duration</div>
            <div class="detail-value-large">{{ selectedPrescription.duration }}</div>
          </div>
        </div>
      </div>
      <div v-if="selectedPrescription.instructions" class="medicine-instructions">
        <strong>Instructions:</strong> {{ selectedPrescription.instructions }}
      </div>
    </div>
  </div>

  <div class="view-actions">
    <button @click="printPrescription(selectedPrescription)" class="btn-print-action">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 6 2 18 2 18 9"></polyline>
        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
        <rect x="6" y="14" width="12" height="8"></rect>
      </svg>
      Print All Medicines
    </button>
  </div>
</div>
*/

// ============================================
// UPDATE THE PRINT FUNCTION
// ============================================

const printPrescription = (prescription) => {
  const medicines = prescription.medicines && prescription.medicines.length > 0
    ? prescription.medicines
    : [{
        medication_name: prescription.medication_name,
        dosage: prescription.dosage,
        frequency: prescription.frequency,
        duration: prescription.duration,
        instructions: prescription.instructions
      }]

  const medicinesHTML = medicines.map((med, idx) => `
    <div class="medication">
      <h3>${idx + 1}. ${med.medication_name}</h3>
      <p><span class="label">Dosage:</span> ${med.dosage}</p>
      <p><span class="label">Frequency:</span> ${med.frequency}</p>
      <p><span class="label">Duration:</span> ${med.duration}</p>
      ${med.instructions ? `<p><span class="label">Instructions:</span> ${med.instructions}</p>` : ''}
    </div>
  `).join('')

  const printWindow = window.open('', '_blank')
  printWindow.document.write(`
    <html>
      <head>
        <title>Prescription - ${prescription.patient_name}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; }
          .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
          .clinic-name { font-size: 24px; font-weight: bold; color: #6366F1; }
          .details { margin: 20px 0; }
          .label { font-weight: bold; color: #666; }
          .rx { font-size: 36px; font-weight: bold; color: #6366F1; margin: 20px 0; }
          .medication { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 15px 0; }
          .medication h3 { margin: 0 0 10px 0; color: #1F2937; }
          .footer { margin-top: 50px; border-top: 1px solid #ccc; padding-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="clinic-name">Sri Adithya Pet Clinic</div>
          <div>Dr. A. Balasubramanan, B.V.Sc, MBA</div>
          <div>Main Road, Cumbum, Tamil Nadu - 625516</div>
        </div>
        
        <div class="details">
          <div><span class="label">Date:</span> ${formatDate(prescription.created_at)}</div>
          <div><span class="label">Patient:</span> ${prescription.patient_name}</div>
        </div>
        
        <div class="rx">℞</div>
        
        ${medicinesHTML}
        
        <div class="footer">
          <p>_________________________</p>
          <p>Dr. A. Balasubramanan</p>
          <p>B.V.Sc, MBA</p>
        </div>
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.print()
}

// ============================================
// ADD THESE NEW STYLES
// ============================================

/*
.medicine-count-badge {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  display: inline-block;
}

.medicine-summary {
  color: #374151;
  font-size: 14px;
}

.medicine-summary strong {
  color: #1F2937;
}

.more-medicines {
  color: #6366F1;
  font-weight: 600;
  margin-left: 8px;
}

.all-medicines-section {
  margin: 20px 0;
}

.all-medicines-section h3 {
  margin: 0 0 16px 0;
  color: #1F2937;
  font-size: 18px;
  font-weight: 700;
}

.medicines-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.medicine-display-card {
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  border: 2px solid #C7D2FE;
  border-radius: 12px;
  padding: 20px;
}

.medicine-number-badge {
  display: inline-block;
  background: #6366F1;
  color: white;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 12px;
}

.medication-name-large {
  font-size: 20px;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 16px;
}

.medicine-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.detail-icon {
  font-size: 24px;
}

.detail-label-small {
  font-size: 12px;
  color: #6B7280;
  font-weight: 600;
  margin-bottom: 4px;
}

.detail-value-large {
  font-size: 15px;
  color: #1F2937;
  font-weight: 600;
}

.medicine-instructions {
  background: #FFFBEB;
  border-left: 4px solid #F59E0B;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  color: #78350F;
  margin-top: 12px;
}

.medicine-instructions strong {
  color: #92400E;
}
*/