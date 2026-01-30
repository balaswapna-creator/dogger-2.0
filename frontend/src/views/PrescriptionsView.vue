<template>
  <div class="prescriptions-wrapper">
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          <h1>Prescriptions</h1>
        </div>
        <button @click="openModal()" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>New Prescription</span>
        </button>
      </div>
    </div>

    <div class="search-card">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <input 
        v-model="searchQuery"
        @input="searchPrescriptions"
        type="text" 
        placeholder="Search prescriptions..."
        class="search-input"
      />
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading prescriptions...</p>
    </div>

    <div v-else-if="prescriptions.length === 0" class="empty-state-card">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
      </svg>
      <h3>No Prescriptions Found</h3>
      <p>Create your first prescription</p>
      <button @click="openModal()" class="btn-empty-action">Create Prescription</button>
    </div>

    <div v-else class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient</th>
              <th>Medicines</th>
              <th>Details</th>
              <th>Actions</th>
            </tr>
          </thead>
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
                <span class="medicine-count-badge">
                  {{ prescription.medicine_count || 0 }} Medicine(s)
                </span>
              </td>
              <td>
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
                  <button @click="viewPrescription(prescription)" class="btn-view" title="View">
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
                  <button @click="deletePrescription(prescription.id)" class="btn-delete" title="Delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>New Prescription</h2>
          <button @click="closeModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="savePrescription">
            <div class="form-group full-width">
              <label>Select Consultation *</label>
              <select v-model="form.medical_record" required>
                <option value="">Choose Consultation</option>
                <option v-for="consultation in consultations" :key="consultation.id" :value="consultation.id">
                  {{ consultation.patient_name }} - {{ formatDate(consultation.visit_date) }}
                </option>
              </select>
            </div>

            <div class="medicines-section">
              <div class="medicines-header">
                <h3>💊 Medicines</h3>
                <button type="button" class="btn-add-medicine" @click="addMedicine">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="16"></line>
                    <line x1="8" y1="12" x2="16" y2="12"></line>
                  </svg>
                  Add Medicine
                </button>
              </div>

              <div class="medicines-list">
                <div v-for="(medicine, index) in form.medicines" :key="index" class="medicine-card">
                  <div class="medicine-card-header">
                    <span class="medicine-number">Medicine #{{ index + 1 }}</span>
                    <button v-if="form.medicines.length > 1" type="button" class="btn-remove-medicine" @click="removeMedicine(index)">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>

                  <div class="medicine-fields">
                    <div class="form-group">
                      <label>Medication Name *</label>
                      <input v-model="medicine.medication_name" type="text" required placeholder="e.g., Amoxicillin" />
                    </div>

                    <div class="form-group">
                      <label>Dosage *</label>
                      <input v-model="medicine.dosage" type="text" required placeholder="e.g., 250mg" />
                    </div>

                    <div class="form-group">
                      <label>Frequency *</label>
                      <select v-model="medicine.frequency" required>
                        <option value="">Select Frequency</option>
                        <option value="Once daily">Once daily</option>
                        <option value="Twice daily">Twice daily</option>
                        <option value="Three times daily">Three times daily</option>
                        <option value="Four times daily">Four times daily</option>
                        <option value="Every 8 hours">Every 8 hours</option>
                        <option value="Every 12 hours">Every 12 hours</option>
                        <option value="As needed">As needed</option>
                        <option value="Before meals">Before meals</option>
                        <option value="After meals">After meals</option>
                      </select>
                    </div>

                    <div class="form-group">
                      <label>Duration *</label>
                      <input v-model="medicine.duration" type="text" required placeholder="e.g., 7 days" />
                    </div>

                    <div class="form-group full-width">
                      <label>Instructions</label>
                      <textarea v-model="medicine.instructions" rows="2" placeholder="Instructions..."></textarea>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-save">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                </svg>
                Create Prescription
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showViewModal" class="modal-overlay" @click.self="closeViewModal">
      <div class="view-modal">
        <div class="view-header">
          <h2>Prescription Details</h2>
          <button @click="closeViewModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
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
          </div>
          
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
          </div>

          <div class="view-actions">
            <button @click="printPrescription(selectedPrescription)" class="btn-print-action">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                <rect x="6" y="14" width="12" height="8"></rect>
              </svg>
              Print
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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

const patients = ref([])

const fetchPatients = async () => {
  try {
    const response = await api.get('/patients/')
    patients.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error fetching patients:', error)
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
  }
}

const savePrescription = async () => {
  try {
    // Validate that we have at least one medication
    if (!form.value.items || form.value.items.length === 0) {
      alert('Please add at least one medicine')
      return
    }

    // Validate all medicines have required fields
    for (let i = 0; i < form.value.items.length; i++) {
      const item = form.value.items[i]
      if (!item.medication_name || !item.dosage || !item.frequency || !item.duration) {
        alert(`Please fill all required fields for Medicine #${i + 1}`)
        return
      }
    }

    // Validate we have a patient
    if (!form.value.patient_id) {
      alert('Please select a patient')
      return
    }

    // ✅ NEW FORMAT: Build payload matching backend expectations
    const payload = {
      patient_id: form.value.patient_id,                          // Required
      medical_record_id: form.value.medical_record_id || null,    // Optional
      notes: form.value.notes || '',                              // General prescription notes
      items: form.value.items                                     // Array of medications
    }
    
    console.log('📤 Sending prescription data:', payload)
    
    if (editMode.value) {
      // Update existing prescription
      await api.put(`/prescriptions/${form.value.id}/`, payload)
      alert('Prescription updated successfully!')
    } else {
      // Create new prescription
      const response = await api.post('/prescriptions/', payload)
      console.log('✅ Prescription created:', response.data)
      alert(`Prescription created with ${form.value.items.length} medication(s)!`)
    }
    
    closeModal()
    fetchPrescriptions()
  } catch (error) {
    console.error('❌ Error saving prescription:', error)
    console.error('Error response:', error.response?.data)
    
    // Show detailed error message
    if (error.response?.data) {
      const errorDetail = JSON.stringify(error.response.data, null, 2)
      alert(`Failed to save prescription:\n\n${errorDetail}`)
    } else {
      alert('Failed to save prescription: ' + error.message)
    }
  }
}

// Also UPDATE the openModal function to use patient_id instead of medical_record
const openModal = (prescription = null) => {
  if (prescription) {
    editMode.value = true
    form.value = {
      id: prescription.id,
      patient_id: prescription.patient?.id || '',
      medical_record_id: prescription.medical_record?.id || null,
      notes: prescription.notes || '',
      items: prescription.items || []
    }
  } else {
    editMode.value = false
    form.value = {
      patient_id: '',
      medical_record_id: null,
      notes: '',
      items: [createEmptyMedicine()]
    }
  }
  showModal.value = true
}

// UPDATE the form ref at the top of the script
const form = ref({
  patient_id: '',           // ✅ Changed from 'medical_record'
  medical_record_id: null,  // ✅ Added as optional
  notes: '',                // ✅ General prescription notes
  items: []                 // ✅ Array of medications (was 'medicines')
})

const deletePrescription = async (id) => {
  if (!confirm('Delete this prescription?')) return
  
  try {
    await api.delete(`/prescriptions/${id}/`)
    alert('Prescription deleted!')
    fetchPrescriptions()
  } catch (error) {
    console.error('Error deleting:', error)
  }
}

const viewPrescription = (prescription) => {
  selectedPrescription.value = prescription
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
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
          body { font-family: Arial; padding: 40px; }
          .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
          .clinic-name { font-size: 24px; font-weight: bold; color: #6366F1; }
          .details { margin: 20px 0; }
          .label { font-weight: bold; color: #666; }
          .rx { font-size: 36px; font-weight: bold; color: #6366F1; margin: 20px 0; }
          .medication { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 15px 0; }
          .medication h3 { margin: 0 0 10px 0; }
          .footer { margin-top: 50px; border-top: 1px solid #ccc; padding-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="clinic-name">Sri Adithya Pet Clinic</div>
          <div>Dr. A. Balasubramanan, B.V.Sc, MBA</div>
          <div>Main Road, Cumbum, Tamil Nadu</div>
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
    console.error('Error searching:', error)
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
  fetchPatients()        // ← Add this!
  fetchConsultations()
})
</script>

<style scoped>
.prescriptions-wrapper {
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
  color: #6366F1;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #6366F1, #4F46E5);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-add:hover {
  transform: translateY(-2px);
}

.search-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.search-icon {
  color: #9CA3AF;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
}

.loading-state {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #6366F1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state-card {
  background: white;
  border-radius: 16px;
  padding: 80px 24px;
  text-align: center;
}

.empty-state-card svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-state-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
}

.btn-empty-action {
  background: linear-gradient(135deg, #6366F1, #4F46E5);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 20px;
}

.table-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: linear-gradient(135deg, #6366F1, #4F46E5);
  color: white;
}

.data-table th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #E5E7EB;
  font-size: 14px;
}

.data-table tbody tr:hover {
  background: #F9FAFB;
}

.date-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #EEF2FF;
  color: #4338CA;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.patient-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366F1, #4F46E5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.medicine-count-badge {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
}

.medicine-summary strong {
  color: #1F2937;
}

.more-medicines {
  color: #6366F1;
  font-weight: 600;
  margin-left: 8px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-view, .btn-print, .btn-delete {
  background: #F3F4F6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-view {
  color: #6366F1;
}

.btn-view:hover {
  background: #EEF2FF;
}

.btn-print {
  color: #14B8A6;
}

.btn-print:hover {
  background: #CCFBF1;
}

.btn-delete {
  color: #EF4444;
}

.btn-delete:hover {
  background: #FEE2E2;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}
.modal-container, .view-modal {
background: white;
border-radius: 20px;
max-width: 800px;
width: 100%;
max-height: 90vh;
display: flex;
flex-direction: column;
box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.modal-header, .view-header {
background: linear-gradient(135deg, #6366F1, #4F46E5);
color: white;
padding: 24px;
display: flex;
justify-content: space-between;
align-items: center;
border-radius: 20px 20px 0 0;
}
.modal-header h2, .view-header h2 {
margin: 0;
font-size: 24px;
font-weight: 700;
}
.btn-close {
background: rgba(255, 255, 255, 0.2);
border: none;
color: white;
width: 36px;
height: 36px;
border-radius: 8px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: all 0.3s;
}
.btn-close:hover {
background: rgba(255, 255, 255, 0.3);
}
.modal-body, .view-body {
padding: 24px;
overflow-y: auto;
}
/* Multiple Medicines Section */
.medicines-section {
background: #F9FAFB;
border-radius: 12px;
padding: 20px;
margin: 20px 0;
}
.medicines-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 20px;
}
.medicines-header h3 {
margin: 0;
font-size: 18px;
font-weight: 700;
color: #1F2937;
}
.btn-add-medicine {
display: flex;
align-items: center;
gap: 6px;
padding: 8px 16px;
background: #10B981;
color: white;
border: none;
border-radius: 8px;
font-size: 14px;
font-weight: 600;
cursor: pointer;
transition: all 0.2s;
}
.btn-add-medicine:hover {
background: #059669;
transform: translateY(-1px);
box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.medicines-list {
display: flex;
flex-direction: column;
gap: 16px;
}
.medicine-card {
background: white;
border: 2px solid #E5E7EB;
border-radius: 12px;
padding: 16px;
transition: all 0.2s;
}
.medicine-card:hover {
border-color: #6366F1;
box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
}
.medicine-card-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 16px;
padding-bottom: 12px;
border-bottom: 1px solid #E5E7EB;
}
.medicine-number {
font-weight: 700;
color: #6366F1;
font-size: 14px;
}
.btn-remove-medicine {
background: #FEE2E2;
color: #EF4444;
border: none;
width: 28px;
height: 28px;
border-radius: 6px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: all 0.2s;
}
.btn-remove-medicine:hover {
background: #FECACA;
transform: scale(1.1);
}
.medicine-fields {
display: grid;
grid-template-columns: repeat(2, 1fr);
gap: 16px;
}
.form-group {
display: flex;
flex-direction: column;
}
.form-group.full-width {
grid-column: 1 / -1;
}
.form-group label {
font-size: 14px;
font-weight: 600;
color: #374151;
margin-bottom: 8px;
}
.form-group input,
.form-group select,
.form-group textarea {
padding: 10px 14px;
border: 2px solid #E5E7EB;
border-radius: 8px;
font-size: 14px;
color: #1F2937;
transition: all 0.3s;
font-family: inherit;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
outline: none;
border-color: #6366F1;
box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
.form-group textarea {
resize: vertical;
}
.field-hint {
margin: 4px 0 0 0;
font-size: 12px;
color: #6B7280;
}
.modal-actions {
display: flex;
gap: 12px;
margin-top: 24px;
padding-top: 24px;
border-top: 1px solid #E5E7EB;
}
.btn-cancel {
flex: 1;
background: #F3F4F6;
color: #4B5563;
border: none;
padding: 14px 24px;
border-radius: 12px;
font-size: 15px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s;
}
.btn-cancel:hover {
background: #E5E7EB;
}
.btn-save {
flex: 2;
background: linear-gradient(135deg, #6366F1, #4F46E5);
color: white;
border: none;
padding: 14px 24px;
border-radius: 12px;
font-size: 15px;
font-weight: 600;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
gap: 8px;
transition: all 0.3s;
box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}
.btn-save:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}
/* View Modal Styles */
.detail-section {
background: #F9FAFB;
border-radius: 12px;
padding: 16px;
margin-bottom: 20px;
}
.detail-row {
display: flex;
justify-content: space-between;
padding: 8px 0;
}
.detail-label {
font-weight: 600;
color: #6B7280;
}
.detail-value {
color: #1F2937;
}
.medication-section {
margin-bottom: 20px;
}
.medication-section h3 {
margin: 0 0 12px 0;
color: #6366F1;
font-size: 16px;
}
.medication-name {
background: linear-gradient(135deg, #6366F1, #4F46E5);
color: white;
padding: 16px 20px;
border-radius: 12px;
font-size: 20px;
font-weight: 700;
}
.dosage-section {
background: #EEF2FF;
border-radius: 12px;
padding: 20px;
margin-bottom: 20px;
}
.dosage-item {
display: flex;
justify-content: space-between;
padding: 8px 0;
border-bottom: 1px solid #C7D2FE;
}
.dosage-item:last-child {
border-bottom: none;
}
.dosage-label {
font-weight: 600;
color: #4338CA;
}
.dosage-value {
color: #1F2937;
font-weight: 500;
}
.instructions-section {
background: #FFFBEB;
border-radius: 12px;
padding: 20px;
margin-bottom: 20px;
border-left: 4px solid #F59E0B;
}
.instructions-section h3 {
margin: 0 0 12px 0;
color: #92400E;
font-size: 16px;
}
.instructions-section p {
margin: 0;
color: #374151;
line-height: 1.6;
}
.view-actions {
margin-top: 24px;
padding-top: 24px;
border-top: 1px solid #E5E7EB;
}
.btn-print-action {
width: 100%;
background: linear-gradient(135deg, #14B8A6, #0D9488);
color: white;
border: none;
padding: 14px 24px;
border-radius: 12px;
font-size: 15px;
font-weight: 600;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
gap: 8px;
transition: all 0.3s;
}
.btn-print-action:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4);
}
@media (max-width: 768px) {
.prescriptions-wrapper {
padding: 16px;
}
.medicine-fields {
grid-template-columns: 1fr;
}
.header-content {
flex-direction: column;
gap: 16px;
align-items: stretch;
}
.btn-add {
width: 100%;
justify-content: center;
}
}
</style>