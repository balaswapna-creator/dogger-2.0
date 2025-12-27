<template>
  <div class="prescriptions-wrapper">
    <!-- Header Card -->
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

    <!-- Search Card -->
    <div class="search-card">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <input 
        v-model="searchQuery"
        @input="searchPrescriptions"
        type="text" 
        placeholder="Search by medication, patient name, or instructions..."
        class="search-input"
      />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading prescriptions...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="prescriptions.length === 0" class="empty-state-card">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
      </svg>
      <h3>No Prescriptions Found</h3>
      <p>Create your first prescription to get started</p>
      <button @click="openModal()" class="btn-empty-action">Create Prescription</button>
    </div>

    <!-- Prescriptions Table -->
    <div v-else class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient</th>
              <th>Medication</th>
              <th>Dosage</th>
              <th>Frequency</th>
              <th>Duration</th>
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
                <span class="medication-badge">{{ prescription.medication_name }}</span>
              </td>
              <td>{{ prescription.dosage }}</td>
              <td>
                <span class="frequency-badge">{{ prescription.frequency }}</span>
              </td>
              <td>{{ prescription.duration }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="viewPrescription(prescription)" class="btn-view" title="View">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>
                  <button @click="openModal(prescription)" class="btn-edit" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
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

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ editMode ? 'Edit Prescription' : 'New Prescription' }}</h2>
          <button @click="closeModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="savePrescription">
            <div class="form-grid">
              <div class="form-group full-width">
                <label>Select Consultation *</label>
                <select v-model="form.medical_record" required>
                  <option value="">Choose Consultation</option>
                  <option v-for="consultation in consultations" :key="consultation.id" :value="consultation.id">
                    {{ consultation.patient_name }} - {{ formatDate(consultation.visit_date) }} - {{ consultation.diagnosis || consultation.chief_complaint }}
                  </option>
                </select>
                <p class="field-hint">Prescription will be linked to this consultation</p>
              </div>

              <div class="form-group full-width">
                <label>Medication Name *</label>
                <input v-model="form.medication_name" type="text" required placeholder="e.g., Amoxicillin"/>
              </div>

              <div class="form-group">
                <label>Dosage *</label>
                <input v-model="form.dosage" type="text" required placeholder="e.g., 250mg, 1 tablet"/>
              </div>

              <div class="form-group">
                <label>Frequency *</label>
                <select v-model="form.frequency" required>
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

              <div class="form-group full-width">
                <label>Duration *</label>
                <input v-model="form.duration" type="text" required placeholder="e.g., 7 days, 2 weeks"/>
              </div>

              <div class="form-group full-width">
                <label>Instructions</label>
                <textarea v-model="form.instructions" rows="3" placeholder="Additional instructions for pet owner..."></textarea>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-save">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                {{ editMode ? 'Update' : 'Create' }} Prescription
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Modal -->
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
          
          <div class="medication-section">
            <h3>Medication</h3>
            <div class="medication-name">{{ selectedPrescription.medication_name }}</div>
          </div>
          
          <div class="dosage-section">
            <div class="dosage-item">
              <span class="dosage-label">Dosage:</span>
              <span class="dosage-value">{{ selectedPrescription.dosage }}</span>
            </div>
            <div class="dosage-item">
              <span class="dosage-label">Frequency:</span>
              <span class="dosage-value">{{ selectedPrescription.frequency }}</span>
            </div>
            <div class="dosage-item">
              <span class="dosage-label">Duration:</span>
              <span class="dosage-value">{{ selectedPrescription.duration }}</span>
            </div>
          </div>
          
          <div v-if="selectedPrescription.instructions" class="instructions-section">
            <h3>Instructions</h3>
            <p>{{ selectedPrescription.instructions }}</p>
          </div>
          
          <div class="doctor-section">
            <span class="doctor-label">Prescribed by:</span>
            <span class="doctor-name">Dr. {{ selectedPrescription.doctor_name }}</span>
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
const editMode = ref(false)
const searchQuery = ref('')
const selectedPrescription = ref(null)

const form = ref({
  medical_record: '',
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

const openModal = (prescription = null) => {
  if (prescription) {
    editMode.value = true
    form.value = {
      id: prescription.id,
      medical_record: prescription.medical_record,
      medication_name: prescription.medication_name,
      dosage: prescription.dosage,
      frequency: prescription.frequency,
      duration: prescription.duration,
      instructions: prescription.instructions || ''
    }
  } else {
    editMode.value = false
    form.value = {
      medical_record: '',
      medication_name: '',
      dosage: '',
      frequency: '',
      duration: '',
      instructions: ''
    }
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const savePrescription = async () => {
  try {
    const payload = {
      ...form.value,
      medical_record: form.value.medical_record || null
    }
    
    if (editMode.value) {
      await api.put(`/prescriptions/${form.value.id}/`, payload)
      alert('Prescription updated successfully!')
    } else {
      await api.post('/prescriptions/', payload)
      alert('Prescription created successfully!')
    }
    
    closeModal()
    fetchPrescriptions()
  } catch (error) {
    console.error('Error saving prescription:', error)
    alert('Failed to save prescription')
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
          .medication { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0; }
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
        
        <div class="medication">
          <h3>${prescription.medication_name}</h3>
          <p><span class="label">Dosage:</span> ${prescription.dosage}</p>
          <p><span class="label">Frequency:</span> ${prescription.frequency}</p>
          <p><span class="label">Duration:</span> ${prescription.duration}</p>
          ${prescription.instructions ? `<p><span class="label">Instructions:</span> ${prescription.instructions}</p>` : ''}
        </div>
        
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
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
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
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
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
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.empty-state-card svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-state-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.empty-state-card p {
  color: #6B7280;
  margin: 0 0 24px 0;
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
  transition: all 0.3s;
}

.btn-empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
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
  white-space: nowrap;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #E5E7EB;
  font-size: 14px;
  color: #374151;
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
  white-space: nowrap;
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
  font-size: 16px;
}

.medication-badge {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.frequency-badge {
  background: #D1FAE5;
  color: #065F46;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-view, .btn-edit, .btn-print, .btn-delete {
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

.btn-edit {
  color: #F59E0B;
}

.btn-edit:hover {
  background: #FEF3C7;
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

.no-data {
  text-align: center;
  padding: 60px 20px !important;
}

/* Modal Styles */
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
  max-width: 700px;
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
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
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 15px;
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

.doctor-section {
  text-align: center;
  padding-top: 20px;
  border-top: 2px solid #E5E7EB;
  margin-top: 20px;
}

.doctor-label {
  display: block;
  font-size: 14px;
  color: #6B7280;
  margin-bottom: 4px;
}

.doctor-name {
  font-size: 18px;
  font-weight: 700;
  color: #1F2937;
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
  
  .form-grid {
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