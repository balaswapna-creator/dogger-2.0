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
          
          <!-- Replace the photo upload section in PatientsView.vue -->
<!-- Find the section starting with "<!-- Photo Upload Section -->" and replace with this: -->

<!-- Photo Upload Section -->
<div class="photo-upload-section">
  <label>Pet Photo</label>
  
  <!-- Camera View (shown when camera is active) -->
  <div v-if="showCamera" class="camera-container">
    <video ref="videoElement" autoplay playsinline class="camera-video"></video>
    <canvas ref="canvasElement" style="display: none;"></canvas>
    <div class="camera-controls">
      <button type="button" @click="captureFromCamera" class="btn-capture">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
        </svg>
        Capture
      </button>
      <button type="button" @click="stopCamera" class="btn-cancel-camera">
        Cancel
      </button>
    </div>
  </div>

  <!-- Photo Upload Area (shown when camera is off) -->
  <div v-else class="photo-upload-area" @click="triggerPhotoUpload">
    <div v-if="photoPreview" class="photo-preview">
      <img :src="photoPreview" alt="Pet photo preview" />
      <button type="button" @click.stop="removePhoto" class="btn-remove-photo">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    <div v-else class="photo-placeholder">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21 15 16 10 5 21"></polyline>
      </svg>
      <p>Click to upload or drag photo here</p>
    </div>
    <input
      ref="photoInput"
      type="file"
      accept="image/*"
      @change="handlePhotoSelect"
      class="photo-input-hidden"
    />
  </div>
  
  <div class="photo-buttons" v-if="!showCamera">
    <button type="button" @click="triggerPhotoUpload" class="btn-upload">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="17 8 12 3 7 8"></polyline>
        <line x1="12" y1="3" x2="12" y2="15"></line>
      </svg>
      Choose File
    </button>
    <button type="button" @click="openCamera" class="btn-camera">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
        <circle cx="12" cy="13" r="4"></circle>
      </svg>
      Take Photo
    </button>
  </div>
</div>

          <div class="form-grid">
            <div class="form-group full-width">
              <label>Pet Name *</label>
              <input v-model="formData.pet_name" type="text" required class="form-input" placeholder="Enter pet name" />
            </div>

            <div class="form-group">
              <label>Species *</label>
              <select v-model="formData.species" required class="form-input">
                <option value="">Select Species</option>
                <option value="dog">Dog</option>
                <option value="cat">Cat</option>
                <option value="bird">Bird</option>
                <option value="rabbit">Rabbit</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Breed</label>
              <input v-model="formData.breed" type="text" class="form-input" placeholder="Enter breed" />
            </div>

            <div class="form-group">
              <label>Date of Birth *</label>
              <input 
                v-model="formData.date_of_birth" 
                type="date" 
                required 
                class="form-input"
                :max="today"
              />
            </div>

            <div class="form-group">
              <label>Age (calculated)</label>
              <input 
                :value="calculatedAge" 
                type="text" 
                readonly 
                class="form-input readonly" 
                placeholder="Auto-calculated from DOB"
              />
            </div>

            <div class="form-group">
              <label>Gender *</label>
              <select v-model="formData.gender" required class="form-input">
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>

            <div class="form-group">
              <label>Color</label>
              <input v-model="formData.color" type="text" class="form-input" placeholder="e.g., Brown, White" />
            </div>

            <div class="form-group full-width">
              <label>Owner *</label>
              <select v-model="formData.owner" required class="form-input">
                <option value="">Select Owner</option>
                <option v-for="owner in owners" :key="owner.id" :value="owner.id">
                  {{ owner.name }} - {{ owner.phone }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Microchip ID</label>
              <input v-model="formData.microchip_id" type="text" class="form-input" placeholder="Optional" />
            </div>

            <div class="form-group">
              <label>Allergies</label>
              <input v-model="formData.allergies" type="text" class="form-input" placeholder="e.g., Penicillin" />
            </div>
          </div>

          <div class="modal-footer">
            <div class="footer-left">
              <button 
                v-if="showEditModal" 
                type="button" 
                @click="confirmDeleteFromModal" 
                class="btn-delete-modal"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
                Delete Patient
              </button>
            </div>
            <div class="footer-right">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" :disabled="saving" class="btn-save">
                {{ saving ? 'Saving...' : (showEditModal ? 'Update Patient' : 'Add Patient') }}
              </button>
            </div>
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
// Add these to the script setup section (after the existing ref declarations)

const videoElement = ref(null)
const canvasElement = ref(null)
const showCamera = ref(false)
const mediaStream = ref(null)

// ✅ NEW: Open camera
const openCamera = async () => {
  try {
    showCamera.value = true
    
    // Request camera access
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { 
        facingMode: 'environment', // Use back camera on mobile
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    })
    
    mediaStream.value = stream
    
    // Wait for video element to be ready
    await new Promise(resolve => setTimeout(resolve, 100))
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      console.log('Camera started successfully')
    }
  } catch (error) {
    console.error('Camera error:', error)
    showCamera.value = false
    
    let errorMsg = 'Cannot access camera. '
    if (error.name === 'NotAllowedError') {
      errorMsg += 'Please allow camera access in your browser settings.'
    } else if (error.name === 'NotFoundError') {
      errorMsg += 'No camera found on your device.'
    } else {
      errorMsg += error.message
    }
    
    alert(errorMsg)
  }
}

// ✅ NEW: Stop camera
const stopCamera = () => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => {
      track.stop()
      console.log('Camera track stopped')
    })
    mediaStream.value = null
  }
  showCamera.value = false
}

// ✅ NEW: Capture photo from camera
const captureFromCamera = () => {
  if (!videoElement.value || !canvasElement.value) {
    console.error('Video or canvas element not found')
    return
  }
  
  const video = videoElement.value
  const canvas = canvasElement.value
  
  // Set canvas size to video size
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  // Draw video frame to canvas
  const context = canvas.getContext('2d')
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  
  // Convert canvas to blob then to file
  canvas.toBlob((blob) => {
    if (!blob) {
      alert('Failed to capture photo')
      return
    }
    
    const timestamp = new Date().getTime()
    const file = new File([blob], `pet-photo-${timestamp}.jpg`, { type: 'image/jpeg' })
    
    // Set photo file
    photoFile.value = file
    
    // Create preview
    photoPreview.value = canvas.toDataURL('image/jpeg', 0.9)
    
    console.log('Photo captured:', file.name, file.size, 'bytes')
    
    // Stop camera
    stopCamera()
  }, 'image/jpeg', 0.9)
}

// ✅ UPDATED: Close modal cleanup
// Find the existing closeModal function and UPDATE it to include camera cleanup:
const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  photoFile.value = null
  photoPreview.value = null
  
  // Stop camera if running
  stopCamera()
  
  formData.value = {
    pet_name: '',
    species: '',
    breed: '',
    date_of_birth: '',
    gender: '',
    color: '',
    owner: '',
    microchip_id: '',
    allergies: '',
    chronic_conditions: '',
    current_medications: ''
  }
  if (photoInput.value) {
    photoInput.value.value = ''
  }
}

// ✅ UPDATE: Keep existing capturePhoto function but rename/replace it
// Remove or comment out the old capturePhoto function and keep this new one

// The triggerPhotoUpload, handlePhotoSelect, and removePhoto functions stay the same

const formData = ref({
  pet_name: '',
  species: '',
  breed: '',
  date_of_birth: '',
  gender: '',
  color: '',
  owner: '',
  microchip_id: '',
  allergies: '',
  chronic_conditions: '',
  current_medications: ''
})

const photoInput = ref(null)
const photoPreview = ref(null)
const photoFile = ref(null)

const today = computed(() => new Date().toISOString().split('T')[0])

const calculatedAge = computed(() => {
  if (!formData.value.date_of_birth) return ''
  
  const dob = new Date(formData.value.date_of_birth)
  const today = new Date()
  
  let years = today.getFullYear() - dob.getFullYear()
  let months = today.getMonth() - dob.getMonth()
  
  if (months < 0) {
    years--
    months += 12
  }
  
  if (years > 0) {
    return `${years} year${years > 1 ? 's' : ''}${months > 0 ? ` ${months} month${months > 1 ? 's' : ''}` : ''}`
  } else {
    return `${months} month${months > 1 ? 's' : ''}`
  }
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
    
    // Use FormData for file uploads
    const submitData = new FormData()
    
    // Add all text fields
    submitData.append('pet_name', formData.value.pet_name)
    submitData.append('species', formData.value.species)
    submitData.append('breed', formData.value.breed || '')
    submitData.append('date_of_birth', formData.value.date_of_birth)
    submitData.append('gender', formData.value.gender)
    submitData.append('color', formData.value.color || '')
    submitData.append('owner', formData.value.owner)
    
    if (formData.value.microchip_id) {
      submitData.append('microchip_id', formData.value.microchip_id)
    }
    if (formData.value.allergies) {
      submitData.append('allergies', formData.value.allergies)
    }
    if (formData.value.chronic_conditions) {
      submitData.append('chronic_conditions', formData.value.chronic_conditions)
    }
    if (formData.value.current_medications) {
      submitData.append('current_medications', formData.value.current_medications)
    }
    
    // Add photo file if selected
    if (photoFile.value) {
      submitData.append('photo', photoFile.value)
      console.log('Photo file added:', photoFile.value.name)
    }
    
    console.log('Saving patient with FormData')
    
    if (showEditModal.value) {
      await api.updatePatient(formData.value.id, submitData)
      console.log('Patient updated successfully')
    } else {
      await api.createPatient(submitData)
      console.log('Patient created successfully')
    }
    
    closeModal()
    await fetchPatients()
  } catch (err) {
    console.error('Error saving patient:', err)
    console.error('Error response:', err.response?.data)
    
    let errorMsg = 'Failed to save patient'
    
    if (err.response?.data) {
      const errors = err.response.data
      if (typeof errors === 'object') {
        errorMsg = Object.entries(errors)
          .map(([field, messages]) => {
            const msgArray = Array.isArray(messages) ? messages : [messages]
            return `${field}: ${msgArray.join(', ')}`
          })
          .join('\n')
      } else if (errors.detail) {
        errorMsg = errors.detail
      } else if (errors.error) {
        errorMsg = errors.error
      }
    }
    
    alert('Error saving patient:\n\n' + errorMsg)
  } finally {
    saving.value = false
  }
}

const calculateAge = () => {
  // Age is auto-calculated via computed property
  console.log('DOB changed:', formData.value.date_of_birth)
}

const triggerPhotoUpload = () => {
  photoInput.value?.click()
}

const capturePhoto = () => {
  // Trigger file input with camera
  const input = photoInput.value
  if (input) {
    input.setAttribute('capture', 'camera')
    input.click()
  }
}

const handlePhotoSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    photoFile.value = file
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target?.result
    }
    reader.readAsDataURL(file)
  }
}

const removePhoto = () => {
  photoFile.value = null
  photoPreview.value = null
  if (photoInput.value) {
    photoInput.value.value = ''
  }
}

const editPatient = (patient) => {
  formData.value = { ...patient }
  
  // Load photo preview if exists
  if (patient.photo) {
    photoPreview.value = getPhotoUrl(patient.photo)
  }
  
  showEditModal.value = true
}

const confirmDeleteFromModal = () => {
  if (confirm(`Are you sure you want to delete ${formData.value.pet_name}?`)) {
    deletePatientById(formData.value.id)
  }
}

const deletePatientById = async (id) => {
  try {
    deleting.value = true
    await api.deletePatient(id)
    console.log('Patient deleted successfully')
    closeModal()
    await fetchPatients()
  } catch (err) {
    console.error('Error deleting patient:', err)
    alert(err.response?.data?.detail || 'Failed to delete patient')
  } finally {
    deleting.value = false
  }
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
  photoFile.value = null
  photoPreview.value = null
  formData.value = {
    pet_name: '',
    species: '',
    breed: '',
    date_of_birth: '',
    gender: '',
    color: '',
    owner: '',
    microchip_id: '',
    allergies: '',
    chronic_conditions: '',
    current_medications: ''
  }
  if (photoInput.value) {
    photoInput.value.value = ''
  }
}

const getPhotoUrl = (photo) => {
  if (!photo) return ''
  // If photo is already a full URL, return it
  if (photo.startsWith('http://') || photo.startsWith('https://')) {
    return photo
  }
  // If photo is a relative path, prepend the backend URL
  if (photo.startsWith('/')) {
    return `https://dogger2-backend.onrender.com${photo}`
  }
  // Otherwise, assume it's a path without leading slash
  return `https://dogger2-backend.onrender.com/${photo}`
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

.photo-upload-section {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f3f4f6;
}

.photo-upload-section > label {
  display: block;
  font-weight: 600;
  font-size: 14px;
  color: #374151;
  margin-bottom: 12px;
}

.photo-upload-area {
  position: relative;
  width: 100%;
  height: 200px;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
}

.photo-upload-area:hover {
  border-color: #7C3AED;
  background: #f9fafb;
}

.photo-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #9ca3af;
}

.photo-placeholder svg {
  margin-bottom: 12px;
}

.photo-placeholder p {
  margin: 0;
  font-size: 14px;
}

.photo-preview {
  position: relative;
  width: 100%;
  height: 100%;
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-remove-photo {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-remove-photo:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.photo-input-hidden {
  display: none;
}

.photo-buttons {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.btn-upload,
.btn-camera {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  transition: all 0.3s;
}

.btn-upload:hover,
.btn-camera:hover {
  border-color: #7C3AED;
  color: #7C3AED;
  background: #f9fafb;
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

.form-group.full-width {
  grid-column: 1 / -1;
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

.form-input.readonly {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-top: 2px solid #f3f4f6;
}

.footer-left {
  flex: 1;
}

.footer-right {
  display: flex;
  gap: 12px;
}

.btn-delete-modal {
  background: transparent;
  color: #ef4444;
  border: 2px solid #ef4444;
  padding: 12px 20px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.btn-delete-modal:hover {
  background: #ef4444;
  color: white;
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
/* Add these to the existing <style scoped> section */

.camera-container {
  margin-bottom: 16px;
}

.camera-video {
  width: 100%;
  max-height: 400px;
  border-radius: 12px;
  border: 3px solid #7C3AED;
  background: #000;
  object-fit: cover;
}

.camera-controls {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.btn-capture {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-capture:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.btn-cancel-camera {
  padding: 14px 24px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel-camera:hover {
  background: #e5e7eb;
}

}
</style>