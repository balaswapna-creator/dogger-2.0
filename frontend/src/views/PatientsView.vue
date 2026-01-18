<template>
  <div class="patients-container">
    <div class="patients-header">
      <div class="header-left">
        <div class="header-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </div>
        <div>
          <h1>Patients (Pets)</h1>
          <p class="subtitle">Manage all your pet patients</p>
        </div>
      </div>
      <button @click="showAddModal = true" class="btn-add">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Add New Pet
      </button>
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search pets by name, species, or owner..."
        class="search-input"
      />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading patients...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Error Loading Patients</h2>
      <p>{{ error }}</p>
      <button @click="fetchPatients" class="btn-retry">Retry</button>
    </div>

    <!-- Patients Table -->
    <div v-else-if="filteredPatients.length > 0" class="table-container">
      <table class="patients-table">
        <thead>
          <tr>
            <th>Photo</th>
            <th>Pet Name</th>
            <th>Species</th>
            <th>Breed</th>
            <th>Age</th>
            <th>Owner</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in filteredPatients" :key="patient.id">
            <td>
              <div class="patient-photo">
                <img v-if="patient.photo" :src="getPhotoUrl(patient.photo)" :alt="patient.pet_name" />
                <div v-else class="no-photo">{{ getFirstChar(patient.pet_name) }}</div>
              </div>
            </td>
            <td>
              <div class="patient-name">
                <strong>{{ patient.pet_name }}</strong>
              </div>
            </td>
            <td>{{ patient.species }}</td>
            <td>{{ patient.breed || 'N/A' }}</td>
            <td>{{ patient.age }} years</td>
            <td>{{ patient.owner_name || 'N/A' }}</td>
            <td>{{ patient.owner_phone || 'N/A' }}</td>
            <td>
              <div class="action-buttons">
                <button @click="viewPatient(patient)" class="btn-icon btn-view" title="View">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
                <button @click="editPatient(patient)" class="btn-icon btn-edit" title="Edit">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button @click="confirmDelete(patient)" class="btn-icon btn-delete" title="Delete">
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

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">🐕</div>
      <h2>No Patients Found</h2>
      <p v-if="searchQuery">Try a different search term</p>
      <p v-else>Add your first patient to get started!</p>
      <button v-if="!searchQuery" @click="showAddModal = true" class="btn-add-large">
        Add Your First Patient
      </button>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ showEditModal ? 'Edit Patient' : 'Add New Patient' }}</h2>
          <button @click="closeModal" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="savePatient" class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Pet Name *</label>
              <input v-model="formData.pet_name" type="text" required class="form-input" />
            </div>

            <div class="form-group">
              <label>Species *</label>
              <select v-model="formData.species" required class="form-input">
                <option value="">Select Species</option>
                <option value="Dog">Dog</option>
                <option value="Cat">Cat</option>
                <option value="Bird">Bird</option>
                <option value="Rabbit">Rabbit</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Breed</label>
              <input v-model="formData.breed" type="text" class="form-input" />
            </div>

            <div class="form-group">
              <label>Age (years) *</label>
              <input v-model.number="formData.age" type="number" min="0" step="0.1" required class="form-input" />
            </div>

            <div class="form-group">
              <label>Gender *</label>
              <select v-model="formData.gender" required class="form-input">
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>

            <div class="form-group">
              <label>Color</label>
              <input v-model="formData.color" type="text" class="form-input" />
            </div>

            <div class="form-group">
              <label>Owner *</label>
              <select v-model="formData.owner" required class="form-input">
                <option value="">Select Owner</option>
                <option v-for="owner in owners" :key="owner.id" :value="owner.id">
                  {{ owner.name }} - {{ owner.phone }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Microchip Number</label>
              <input v-model="formData.microchip_number" type="text" class="form-input" />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
            <button type="submit" :disabled="saving" class="btn-save">
              {{ saving ? 'Saving...' : (showEditModal ? 'Update' : 'Add Patient') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content small" @click.stop>
        <div class="modal-header">
          <h2>Confirm Delete</h2>
          <button @click="showDeleteModal = false" class="btn-close">✕</button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete <strong>{{ patientToDelete?.pet_name }}</strong>?</p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancel</button>
          <button @click="deletePatient" :disabled="deleting" class="btn-delete-confirm">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const patients = ref([])
const owners = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const saving = ref(false)
const deleting = ref(false)
const patientToDelete = ref(null)

const formData = ref({
  pet_name: '',
  species: '',
  breed: '',
  age: '',
  gender: '',
  color: '',
  owner: '',
  microchip_number: ''
})

const filteredPatients = computed(() => {
  if (!searchQuery.value) return patients.value
  
  const query = searchQuery.value.toLowerCase()
  return patients.value.filter(p => 
    p.pet_name?.toLowerCase().includes(query) ||
    p.species?.toLowerCase().includes(query) ||
    p.breed?.toLowerCase().includes(query) ||
    p.owner_name?.toLowerCase().includes(query) ||
    p.owner_phone?.includes(query)
  )
})

const fetchPatients = async () => {
  try {
    loading.value = true
    error.value = null
    
    console.log('Fetching patients...')
    const response = await api.getPatients()
    console.log('Patients response:', response.data)
    
    // Handle both array and paginated responses
    if (Array.isArray(response.data)) {
      patients.value = response.data
    } else if (response.data.results) {
      patients.value = response.data.results
    } else {
      patients.value = []
    }
    
    console.log(`Loaded ${patients.value.length} patients`)
  } catch (err) {
    console.error('Error fetching patients:', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load patients'
    
    if (err.response?.status === 401) {
      localStorage.clear()
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

const fetchOwners = async () => {
  try {
    console.log('Fetching owners...')
    const response = await api.getOwners()
    console.log('Owners response:', response.data)
    
    // Handle both array and paginated responses
    if (Array.isArray(response.data)) {
      owners.value = response.data
    } else if (response.data.results) {
      owners.value = response.data.results
    } else {
      owners.value = []
    }
    
    console.log(`Loaded ${owners.value.length} owners`)
  } catch (err) {
    console.error('Error fetching owners:', err)
  }
}

const savePatient = async () => {
  try {
    saving.value = true
    
    if (showEditModal.value) {
      await api.updatePatient(formData.value.id, formData.value)
      console.log('Patient updated successfully')
    } else {
      await api.createPatient(formData.value)
      console.log('Patient created successfully')
    }
    
    closeModal()
    await fetchPatients()
  } catch (err) {
    console.error('Error saving patient:', err)
    alert(err.response?.data?.detail || 'Failed to save patient')
  } finally {
    saving.value = false
  }
}

const editPatient = (patient) => {
  formData.value = { ...patient }
  showEditModal.value = true
}

const viewPatient = (patient) => {
  router.push(`/patients/${patient.id}`)
}

const confirmDelete = (patient) => {
  patientToDelete.value = patient
  showDeleteModal.value = true
}

const deletePatient = async () => {
  try {
    deleting.value = true
    await api.deletePatient(patientToDelete.value.id)
    console.log('Patient deleted successfully')
    showDeleteModal.value = false
    await fetchPatients()
  } catch (err) {
    console.error('Error deleting patient:', err)
    alert(err.response?.data?.detail || 'Failed to delete patient')
  } finally {
    deleting.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  formData.value = {
    pet_name: '',
    species: '',
    breed: '',
    age: '',
    gender: '',
    color: '',
    owner: '',
    microchip_number: ''
  }
}

const getPhotoUrl = (photo) => {
  if (!photo) return ''
  if (photo.startsWith('http')) return photo
  return `https://dogger2-backend.onrender.com${photo}`
}

const getFirstChar = (str) => {
  if (!str || typeof str !== 'string') return '?'
  return str.charAt(0).toUpperCase()
}

onMounted(() => {
  fetchPatients()
  fetchOwners()
})
</script>

<style scoped>
.patients-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.patients-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.patients-header h1 {
  margin: 0;
  font-size: 28px;
  color: #1a1a1a;
}

.subtitle {
  margin: 4px 0 0 0;
  color: #6b7280;
  font-size: 14px;
}

.btn-add {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.search-bar {
  background: white;
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.search-bar svg {
  color: #9ca3af;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #1a1a1a;
}

.search-input::placeholder {
  color: #9ca3af;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
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

.error-icon, .empty-icon {
  font-size: 60px;
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

.table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.patients-table {
  width: 100%;
  border-collapse: collapse;
}

.patients-table thead {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
}

.patients-table th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.patients-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
  color: #374151;
}

.patients-table tbody tr:hover {
  background: #f9fafb;
}

.patient-photo {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  overflow: hidden;
}

.patient-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-photo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  border-radius: 10px;
}

.patient-name strong {
  color: #1a1a1a;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-view {
  background: #e0f2fe;
  color: #0369a1;
}

.btn-view:hover {
  background: #0ea5e9;
  color: white;
}

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-edit:hover {
  background: #f59e0b;
  color: white;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #ef4444;
  color: white;
}

/* Modal Styles */
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
  max-width: 700px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

.modal-content.small {
  max-width: 450px;
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  font-size: 14px;
  color: #374151;
}

.form-input {
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 24px;
  border-top: 2px solid #f3f4f6;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-save {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-delete-confirm {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-delete-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.warning-text {
  color: #dc2626;
  font-weight: 600;
  margin-top: 8px;
}

.btn-add-large {
  margin-top: 24px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .patients-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>